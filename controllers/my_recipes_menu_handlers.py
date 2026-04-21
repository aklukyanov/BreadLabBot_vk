import aiohttp
import base64
from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.my_recipes_list_handler import BaseMyRecipesListStateHandler
from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import step_back_or_cancel_keyboard, error_keyboard
from utils.messages import waiting_user_recipe_default_message, photo_parsing_error_message


class MyRecipesListStateHandler(BaseMyRecipesListStateHandler):
    """Список рецептов в режиме 'Мои рецепты'. Наследует всю логику из базового класса."""
    pass


class WaitingUserRecipeStateHandler(BaseStateHandler):
    """
    Ожидание текстового или фото рецепта от пользователя.

    Отправляет текст или фото в LLM для распознавания, при успехе переходит в редактирование.
    При ошибке показывает клавиатуру с кнопкой повтора.
    """

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}\n\n{waiting_user_recipe_default_message}"

        return waiting_user_recipe_default_message

    def get_keyboard(self, session_data: dict):
        error = session_data["context"].get("error")
        recipe_to_add = session_data["context"].get("recipe_to_add", None)

        if error and recipe_to_add:
            return error_keyboard("send_recipe_to_llm")

        return step_back_or_cancel_keyboard("back", "to_main")

    async def _process_llm_request(self, event, session_data: dict, text: str):
        """
        Отправляет текст в LLM и обрабатывает ответ.

        Returns:
            Имя команды для перехода или None.
        """
        result, error = await BreadlabAPIClient.recognize_recipe_text(text)

        if error:
            session_data["context"]["error"] = error
            await self.show_screen(event, session_data)
            return None

        if result["status"] == "ok":
            session_data["context"]["recipe_to_edit"] = result["data"]
            session_data["context"].pop("error", None)
            return "open_edit_added_recipe"

        if result["status"] == "error":
            session_data["context"]["error"] = result["message"]
            await self.show_screen(event, session_data)
            return None

    async def handle_message(self, message: Message, session_data: dict):
        """Обрабатывает текстовое сообщение с рецептом."""
        text = self.get_text_from_message(message)
        session_data["context"]["recipe_to_add"] = text
        session_data["context"].pop("error", None)

        cmd = await self._process_llm_request(message, session_data, text)
        if cmd:
            return cmd, session_data
        return None, session_data

    async def handle_photo(self, message: Message, session_data: dict):
        """
        Обрабатывает фотографию рецепта: конвертирует в base64 и отправляет в LLM.
        """
        # 1. Получаем фото из сообщения
        if not message.attachments or not message.attachments[0].photo:
            session_data["context"]["error"] = photo_parsing_error_message
            await self.show_screen(message, session_data)
            return None, session_data

        photo = message.attachments[0].photo
        photo_url = photo.sizes[-1].url  # Самое большое разрешение

        # 2. Скачиваем и конвертируем в base64
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(photo_url) as resp:
                    image_bytes = await resp.read()
                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            session_data["context"]["error"] = f"Ошибка загрузки фото: {e}"
            await self.show_screen(message, session_data)
            return None, session_data

        # 3. Сохраняем фото в контекст (для возможного повтора)
        session_data["context"]["recipe_photo"] = image_base64
        session_data["context"].pop("error", None)

        # 4. Отправляем в LLM
        result, error = await BreadlabAPIClient.recognize_photo(image_base64)

        if error:
            session_data["context"]["error"] = error
            await self.show_screen(message, session_data)
            return None, session_data

        if result["status"] == "ok":
            session_data["context"]["recipe_to_edit"] = result["data"]
            session_data["context"].pop("error", None)
            return "open_edit_added_recipe", session_data

        if result["status"] == "error":
            session_data["context"]["error"] = result["message"]
            await self.show_screen(message, session_data)
            return None, session_data

    async def handle_event(self, event: MessageEvent, session_data: dict):
        """Обрабатывает нажатия кнопок (например, повторная отправка)."""
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "send_recipe_to_llm":
            recipe = session_data["context"].get("recipe_to_add")
            cmd = await self._process_llm_request(event, session_data, recipe)
            if cmd:
                return cmd, session_data
            return None, session_data

        if cmd in ("back", "to_main", "open_edit_added_recipe"):
            session_data["context"].pop("error", None)
            session_data["context"].pop("recipe_to_add", None)
            session_data["context"].pop("recipe_photo", None)

        return await super().handle_event(event, session_data)