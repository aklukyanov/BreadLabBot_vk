import asyncio
from vkbottle import Bot
import bot.handlers
from config import api, global_labeler, state_dispenser
from utils.api_client import BreadlabAPIClient

bot = Bot(
     api=api,
     labeler=global_labeler,
     state_dispenser=state_dispenser,

)

async def shutdown():
    """Корректное завершение всех асинхронных ресурсов"""
    await BreadlabAPIClient.close()
    # Даём время на закрытие соединений
    await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        bot.run_forever()
    except KeyboardInterrupt:
        print("\n🛑 Завершение...")
    finally:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(shutdown())
        loop.close()