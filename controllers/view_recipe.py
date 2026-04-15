from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import edit_recipe_keyboard, error_keyboard


class ViewRecipeStateHandler(BaseStateHandler):
    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        recipe_id = session_data["context"]["recipe_id"]

        result, error = await BreadlabAPIClient.get_recipe(recipe_id=recipe_id)
        if error:
            session_data["context"]["error"] = error
            session_data["context"]["recipes"] = []
        else:
            # 👇 Парсим и сохраняем в context
            session_data["context"]["error"] = None
            session_data["context"]["recipe"] = result['recipe']["data"]
            session_data["context"]["recipe_id"] = recipe_id

        await super().show_screen(event, session_data)

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}"

        recipe=session_data["context"]["recipe"]
        message=convert_dict_to_pretty_print(recipe)
        return message

    def get_keyboard(self, session_data:dict) -> str|None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("open_view_recipe")

        recipe_id=session_data["context"]["recipe_id"]
        return edit_recipe_keyboard(recipe_id)

