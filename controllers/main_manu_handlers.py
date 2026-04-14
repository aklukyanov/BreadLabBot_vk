from vkbottle_types.events.bot_events import MessageEvent
from controllers.base_state_handler import BaseStateHandler
from utils.keyboards import main_menu_keyboard, tools_menu_keyboard


class MainMenuState(BaseStateHandler):
    async def show_screen(self, event, session_data, custom_message=None, custom_keyboard=None):
        # Очищаем контекст при каждом показе главного меню
        session_data["context"].clear()
        await super().show_screen(event, session_data, custom_message, custom_keyboard)

    def get_message(self, context: dict) -> str:
        return "🏠 Главное меню"

    def get_keyboard(self, context: dict) -> str:
        return main_menu_keyboard

    async def handle_event(self, event: MessageEvent, session_data: dict):
        if event.object.payload["cmd"]=="tools":
            session_data["context"].clear()
            return "open_tools", session_data

class ToolsMenuState(BaseStateHandler):

    def get_message(self, context: dict) -> str:
        return "🔧 Инструменты"
    def get_keyboard(self, context: dict) -> str:
        return tools_menu_keyboard

