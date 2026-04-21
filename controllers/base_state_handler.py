from abc import ABC, abstractmethod
from typing import Tuple, Optional

from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from utils.messages import default_text_warning


class BaseStateHandler(ABC):

    def get_text_from_message(self, message: Message) -> str | None:
        """Платформонезависимое получение текста сообщения."""
        return message.text

    def get_payload_from_event(self, event: MessageEvent | Message, key: str, default=None):
        """Платформонезависимое получение параметра из payload/data."""
        if isinstance(event, MessageEvent):
            return event.object.payload.get(key, default)
        elif isinstance(event, Message):
            return default

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        """Универсальная отрисовка экрана."""
        message_text = self.get_message(session_data)
        keyboard = self.get_keyboard(session_data)

        # Защита от пустого сообщения: если нет ни текста, ни клавиатуры — ничего не отправляем
        if not message_text and not keyboard:
            return

        if isinstance(event, MessageEvent):
            await event.ctx_api.messages.send(
                peer_id=event.object.peer_id,
                message=message_text or " ",  # Защита от None
                keyboard=keyboard,
                random_id=0
            )
        else:
            await event.answer(
                message=message_text or " ",
                keyboard=keyboard
            )

    @abstractmethod
    def get_message(self, session_data: dict) -> str:
        """Текст сообщения для этого состояния."""
        pass

    @abstractmethod
    def get_keyboard(self, session_data: dict) -> str | None:
        """Клавиатура для этого состояния (или None)."""
        pass

    async def handle_event(self, event: MessageEvent, session_data: dict) -> Tuple[Optional[str], dict]:
        """Обработка нажатий на кнопки. По умолчанию возвращает cmd из payload."""
        cmd = self.get_payload_from_event(event, "cmd")
        return cmd, session_data

    async def handle_message(self, message: Message, session_data: dict) -> Tuple[Optional[str], dict]:
        """Обработка текстовых сообщений. По умолчанию — защита от текста."""
        await message.reply(default_text_warning)
        await message.answer(
            message=self.get_message(session_data),
            keyboard=self.get_keyboard(session_data)
        )
        return None, session_data

    async def handle_photo(self, message: Message, session_data: dict) -> Tuple[Optional[str], dict]:
        """Обработка фотографий. По умолчанию — защита от фото."""
        await message.reply(default_text_warning)
        await message.answer(
            message=self.get_message(session_data),
            keyboard=self.get_keyboard(session_data)
        )
        return None, session_data