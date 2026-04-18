from abc import ABC, abstractmethod
from typing import Tuple, Optional

from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

class BaseStateHandler(ABC):
    def get_text_from_message(self, message:Message) -> str | None:
        """Платформонезависимое получение текста сообщения."""
        return message.text

    def get_payload_from_event(self, event: MessageEvent | Message, key: str, default=None):
        """Платформонезависимое получение параметра из payload/data"""
        # VK MessageEvent (нажатие на кнопку)
        if isinstance(event, MessageEvent):
            return event.object.payload.get(key, default)
        # VK Message (текстовое сообщение)
        elif isinstance(event, Message):
            # У текстовых сообщений нет payload, возвращаем default (None)
            return default

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
    def get_message(self, session_data: dict) -> str:
        """Текст, для сообщения"""
        pass

    @abstractmethod
    def get_keyboard(self, session_data:dict) -> str|None:
        """Клавиатура для этого состояния (или None)"""
        pass

    async def handle_event(self, event: MessageEvent, session_data: dict) -> Tuple[Optional[str], dict]:
            cmd=event.object.payload["cmd"]
            return cmd, session_data

    async def handle_message(self, message:Message, session_data: dict) -> Tuple[Optional[str], dict]:
        await message.reply("⚠️ В этом меню нельзя отправлять сообщения. Используйте кнопки.")

        await message.answer(
            message=self.get_message(session_data),
            keyboard=self.get_keyboard(session_data))

        return None, session_data