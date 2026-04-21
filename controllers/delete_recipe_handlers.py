from vkbottle_types.events.bot_events import MessageEvent
from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import approve_keyboard, error_keyboard, back_to_recipes_keyboard
from utils.messages import delete_recipe_approve_message, success_delete_message


class DeleteRecipeStateHandler(BaseStateHandler):
    """
    Экран подтверждения удаления рецепта.

    Состояния:
    - Показ подтверждения (кнопки Да/Нет)
    - Показ ошибки (кнопка Повторить)
    - Показ успеха (кнопка В мои рецепты)
    """

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        deleted = session_data["context"].get("deleted")
        if error:
            return f"❌ {error}"
        if deleted:
            return success_delete_message

        return delete_recipe_approve_message

    def get_keyboard(self, session_data: dict) -> str | None:
        error = session_data["context"].get("error")
        deleted = session_data["context"].get("deleted")
        if error:
            return error_keyboard("delete_recipe_approve")
        if deleted:
            return back_to_recipes_keyboard

        return approve_keyboard("delete_recipe_approve", "back")

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "delete_recipe_approve":
            recipe_id = session_data["context"].get("recipe_id")
            result, error = await BreadlabAPIClient.delete_recipe(recipe_id)
            if error:
                session_data["context"]["error"] = error
            if result:
                session_data["context"]["deleted"] = recipe_id
                session_data["context"].pop("error", None)  # Очищаем старую ошибку при успехе
            await self.show_screen(event, session_data)
            return None, session_data
        if cmd == "back":
            session_data["context"].pop("deleted", None)
            session_data["context"].pop("error", None)
            return "back", session_data
        if cmd == "open_my_recipes_list":
            session_data["context"].pop("deleted", None)
            session_data["context"].pop("error", None)
            return "open_my_recipes_list", session_data
        return await super().handle_event(event, session_data)