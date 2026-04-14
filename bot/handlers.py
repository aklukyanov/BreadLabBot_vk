from aiohttp import ClientSession
from vkbottle.bot import Message
from vkbottle_types import GroupEventType
from vkbottle_types.events.bot_events import MessageEvent

from config import global_labeler, manager
from storage import storage
from utils.keyboards import main_menu_keyboard
from utils.messages import greeting


@global_labeler.message(text="Начать")
async def hello_handler(message: Message):
    # Получаем информацию о пользователе
    user_info = await message.ctx_api.users.get(user_ids=message.from_id)
    user = user_info[0]
    await message.answer(message=greeting.format(user.first_name))
    await message.answer('Главное меню', keyboard=main_menu_keyboard)

    # Сохраняем пользователя в бд
    async with ClientSession() as session:
        try:
            async with session.post(
                "http://127.0.0.1:8000/api/users/",
                json={
                    "external_id": str(user.id),
                    "channel": "vk",
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "gender": user.sex,
                    "username": user.screen_name
                },
                timeout=5
            ) as response:
                if response.status in [200,201]:
                    result = await response.json()
                    print("User saved:", result)
                else:
                    print("Error status:", response.status)
                    print("Error text:", await response.text())
        except Exception as e:
            print(f"Ошибка сохранения пользователя: {e}")

        storage.set(key=message.peer_id,
                    value={
                        "state_config": ["main"],
                        "context": {}
                    })
        test_data=storage.get(key=message.peer_id)

        print(f"Сохранили в storage {test_data}")


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
async def message_handler(message:Message):
    await manager.handle_message(message)


