from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import error_keyboard, view_recipe_keyboard
from utils.messages import recipe_not_found_message, waiting_multiplier_default_message, wrong_multiplier_message


class BaseViewRecipeStateHandler(BaseStateHandler):
    """
    Базовый класс для просмотра рецепта.

    Умеет работать с двумя источниками:
    - Существующий рецепт (по recipe_id из API)
    - Новый/загруженный рецепт (из контекста recipe_to_save / recipe_to_edit)
    """
    mode = None  # переопределим в наследниках

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        # 1. Пытаемся получить recipe_id
        recipe_id = session_data["context"].get("recipe_id")

        if recipe_id:
            # Случай А: Сохранённый рецепт — загружаем с сервера
            result, error = await BreadlabAPIClient.get_recipe(recipe_id=recipe_id)
            if error:
                session_data["context"]["error"] = error
            else:
                session_data["context"]["recipe"] = result['recipe']["data"]
                session_data["context"]["error"] = None
        else:
            # Случай Б: Новый/загруженный рецепт — берём из контекста
            recipe = (
                    session_data["context"].get("recipe_to_save") or
                    session_data["context"].get("recipe_to_edit") or
                    session_data["context"].get("recipe")
            )
            if recipe:
                # Убедимся, что он лежит в едином ключе `recipe`
                session_data["context"]["recipe"] = recipe
                session_data["context"]["error"] = None
            else:
                session_data["context"]["error"] = recipe_not_found_message

        # 2. Вызываем родительский show_screen, который возьмёт данные из `recipe` и `error`
        await super().show_screen(event, session_data)

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}"

        recipe = session_data["context"]["recipe"]
        message = convert_dict_to_pretty_print(recipe)
        return message

    def get_keyboard(self, session_data: dict) -> str | None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard(self._get_retry_command())

        return view_recipe_keyboard(self.mode)

    def _get_retry_command(self) -> str:
        """Команда для кнопки 'Отправить заново'. Переопределяется в наследниках."""
        return "open_view_recipe"


class WaitingMultiplierStateHandler(BaseViewRecipeStateHandler):
    """Просмотр рецепта перед умножением. Запрашивает множитель."""
    mode = "proportions_calc"

    def _get_retry_command(self) -> str:
        return "enter_multiplier"

    def get_message(self, session_data: dict) -> str:
        # Берём базовое сообщение (рецепт)
        base_message = super().get_message(session_data)
        # редактируем
        return f"{base_message}\n\n{waiting_multiplier_default_message}"

    async def handle_message(self, message: Message, session_data: dict):
        text = self.get_text_from_message(message)
        try:
            multiplier = int(text.strip())
            if multiplier <= 0:
                session_data["context"]["error"] = wrong_multiplier_message
                await self.show_screen(message, session_data)
                return None, session_data

            # Успех — сохраняем и делаем запрос
            session_data["context"]["multiplier"] = multiplier
            session_data["context"]["error"] = None
            recipe = session_data["context"]["recipe"]
            # Запрос к API
            result, error = await BreadlabAPIClient.multiply_recipe(multiplier, recipe)

            if error:
                session_data["context"]["error"] = error
                await self.show_screen(message, session_data)
                return None, session_data

            # Сохраняем результат
            session_data["context"]["result_recipe"] = result['recipe']
            return "enter_multiplier", session_data

        except ValueError:
            session_data["context"]["error"] = "Введите целое число"
            await self.show_screen(message, session_data)
            return None, session_data


class EditRecipeStateHandler(BaseViewRecipeStateHandler):
    """Просмотр рецепта в режиме редактирования (с кнопками Редактировать/Удалить)."""
    mode = "edit_recipe"