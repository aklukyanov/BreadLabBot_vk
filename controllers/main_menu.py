from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.keyboards import main_menu_keyboard, tools_menu_keyboard


class MainMenuState(BaseStateHandler):

    def get_message(self, context: dict) -> str:
        return "Главное меню"

    def get_keyboard(self, context: dict) -> str:
        return main_menu_keyboard

    async def handle_event(self, event: MessageEvent, session_data: dict):
        if event.object.payload["cmd"]=="tools":
            session_data["context"].clear()
            return "open_tools", session_data

    async def handle_message(self, message: Message, session_data: dict):
        await message.answer(
                message="В главном меню нельзя отправлять сообщения. Нажимайте на кнопки.",
                keyboard=main_menu_keyboard
            )

class ToolsMenuState(BaseStateHandler):

    def get_message(self, context: dict) -> str:
        return "Инструменты"
    def get_keyboard(self, context: dict) -> str:
        return tools_menu_keyboard

    async def handle_message(self, message: Message, session_data: dict):
        await message.answer(
            message="В меню инструментов нельзя отправлять сообщения. Нажимайте на кнопки.",
            keyboard=tools_menu_keyboard
        )