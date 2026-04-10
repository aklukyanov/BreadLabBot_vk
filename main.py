
from vkbottle import Bot
import bot.handlers
from config import api, global_labeler, state_dispenser


bot = Bot(
     api=api,
     labeler=global_labeler,
     state_dispenser=state_dispenser,

)

if __name__ == "__main__":
    bot.run_forever()

