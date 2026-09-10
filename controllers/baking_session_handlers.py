from typing import Tuple, Optional

from vkbottle.bot import MessageEvent, Message

from controllers.base_state_handler import BaseStateHandler
from controllers.my_recipes_list_handler import BaseMyRecipesListStateHandler
from controllers.view_recipe_handlers import BaseViewRecipeStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import error_keyboard, view_recipe_keyboard


class ChooseRecipeStateHandler(BaseMyRecipesListStateHandler):
    mode = "baking_session"

    def get_message(self, session_data: dict) -> str:
        base = super().get_message(session_data)
        return f'Выберите рецепт для выпечки\n\n{base}'

class ChooseSessionStateHandler(BaseViewRecipeStateHandler):
    mode = 'baking_session'

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        await self._load_sessions(session_data)
        await super().show_screen(event, session_data)

    async def _load_sessions(self, session_data: dict):
        recipe_id = session_data["context"].get("recipe_id")
        if not recipe_id:
            return

        external_id = str(session_data["peer_id"])
        page = session_data["context"].get("sessions_page", 1)
        result, error = await BreadlabAPIClient.get_unfinished_baking_sessions(
            external_id, int(recipe_id), page=page
        )
        if error:
            session_data["context"]["error"] = error
            return

        session_data["context"].update({
            "sessions": result["baking_sessions"],
            "sessions_page": result["page"],
            "sessions_has_prev": result["has_prev"],
            "sessions_has_next": result["has_next"],
            "total_pages": result["total_pages"],
            "error": None,
        })

    def get_keyboard(self, session_data: dict) -> str | None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard(self._get_retry_command())

        return view_recipe_keyboard(
            self.mode,
            sessions=session_data["context"].get("sessions") or [],
            current_page=session_data["context"].get("sessions_page", 1),
            has_prev=session_data["context"].get("sessions_has_prev", False),
            has_next=session_data["context"].get("sessions_has_next", False),
        )

    def _get_retry_command(self) -> str:
        """Команда для кнопки 'Отправить заново'. Переопределяется в наследниках."""
        return "open_choose_session"

    async def handle_event(self, event: MessageEvent, session_data: dict) -> Tuple[Optional[str], dict]:
        """Обработка нажатий на кнопки. По умолчанию возвращает cmd из payload."""
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "show_sessions":
            page = self.get_payload_from_event(event, "page", 1)
            session_data["context"]["sessions_page"] = int(page)
            await self.show_screen(event, session_data)
            return None, session_data
        if cmd in ("start_session", "continue_session"):
            cmd = 'open_baking_session'
            return cmd, session_data

        return cmd, session_data

class BakingSessionStateHandler(BaseStateHandler):
    pass