from vkbottle_types.events.bot_events import MessageEvent
from controllers.base_state_handler import BaseStateHandler
from utils.keyboards import main_menu_keyboard, tools_menu_keyboard, step_back_or_cancel_keyboard, back_only_keyboard
from utils.messages import about_breadlab


class MainMenuStateHandler(BaseStateHandler):
    async def show_screen(self, event, session_data):
        # Очищаем контекст при каждом показе главного меню
        session_data["context"].clear()
        await super().show_screen(event, session_data)

    def get_message(self, context: dict) -> str:
        return "🏠 Главное меню"

    def get_keyboard(self, context: dict) -> str:
        return main_menu_keyboard

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd=self.get_payload_from_event(event,"cmd")

        if cmd == "tools":
            return "open_tools", session_data
        if cmd == "my_recipes_menu":
            return "open_my_recipes_menu", session_data
        return await super().handle_event(event, session_data)


class ToolsMenuStateHandler(BaseStateHandler):

    def get_message(self, session_data: dict) -> str:
        return "🔧 Инструменты"
    def get_keyboard(self, session_data: dict) -> str:
        return tools_menu_keyboard

class AboutBreadLabStateHandler(BaseStateHandler):
    def get_message(self, session_data: dict) -> str:
        return about_breadlab

    def get_keyboard(self, session_data: dict) -> str:
        return back_only_keyboard