from aiohttp import ClientSession
from vkbottle.bot import Message
from vkbottle_types import GroupEventType
from vkbottle_types.events.bot_events import MessageEvent

from config import global_labeler, manager
from logger import handler_logger
from settings import CURRENT_URL
from storage import storage
from utils.keyboards import main_menu_keyboard
from utils.messages import greeting

'ТОЧКА ВХОДА'
@global_labeler.message(text="Начать")
async def hello_handler(message: Message):
    try:
        user_info = await message.ctx_api.users.get(user_ids=message.from_id)
        user = user_info[0]

        async with ClientSession() as session:
            async with session.post(
                url=f"{CURRENT_URL}/api/users/",
                json={
                    "external_id": str(user.id),
                    "channel": "vk",
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": user.sex,
                    "username": user.screen_name
                },
                timeout=1
            ) as response:
                if response.status not in [200, 201]:
                    error_body = await response.text()
                    handler_logger.warning(f"Error status: {response.status}, body: {error_body}")
                    await message.answer(message='Сервис временно недоступен. Попробуйте позже.')
                    return
                result = await response.json()
                handler_logger.info(f"User saved: {result}")

        await message.answer(message=greeting.format(user.first_name))
        await message.answer('Главное меню', keyboard=main_menu_keyboard)

        await storage.set(key=message.peer_id,
                    value={
                        "peer_id": message.peer_id,
                        "state_config": ["main"],
                        "context": {}
                    })
    except Exception as e:
        handler_logger.error(f"Ошибка hello_handler: {e}", exc_info=True)
        await message.answer(message='Сервис временно недоступен. Попробуйте позже.')



@global_labeler.raw_event(event=GroupEventType.MESSAGE_EVENT, dataclass=MessageEvent, blocking=False)
async def events_handler(event: MessageEvent):
    # Убираем кручение кнопки
    await event.ctx_api.messages.send_message_event_answer(
        event_id=str(event.object.event_id),
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
    )
    await manager.handle_event(event)

@global_labeler.message(blocking=False)
async def message_handler(message: Message):
    """Обработчик всех сообщений (текст и фото)."""
    # Проверяем, есть ли фото во вложениях
    if message.attachments and message.attachments[0].photo:
        await manager.handle_photo(message)
    else:
        await manager.handle_message(message)