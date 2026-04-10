from abc import ABC, abstractmethod
from typing import Tuple, Optional

from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent


class BaseStateHandler(ABC):

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        """Универсальная отрисовка экрана"""
        message_text = self.get_message(session_data)
        keyboard = self.get_keyboard(session_data)

        if isinstance(event, MessageEvent):
            await event.ctx_api.messages.send(
                peer_id=event.object.peer_id,
                message=message_text,
                keyboard=keyboard,
                random_id=0
            )
        else:  # Message
            await event.answer(
                message=message_text,
                keyboard=keyboard
            )
    @abstractmethod
    def get_message(self, context: dict) -> str:
        """Текст, для сообщения"""
        pass

    @abstractmethod
    def get_keyboard(self, context:dict) -> str:
        """Клавиатура для этого состояния (или None)"""
        pass

    async def handle_event(self, event: MessageEvent, session_data: dict) -> Tuple[Optional[str], dict]:
            cmd=event.object.payload["cmd"]
            return cmd, session_data