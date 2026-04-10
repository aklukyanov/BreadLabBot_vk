from dotenv import load_dotenv
import os

from vkbottle import API, BuiltinStateDispenser, CtxStorage
from vkbottle.framework.labeler import BotLabeler

from core.session_manager import SessionManager

load_dotenv()
vk_token=os.getenv("bot_token")
api=API(vk_token)
state_dispenser = BuiltinStateDispenser()
global_labeler = BotLabeler()
manager=SessionManager()

