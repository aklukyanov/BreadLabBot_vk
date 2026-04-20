from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_my_recipes_list_handler import BaseMyRecipesListStateHandler
from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import step_back_or_cancel_keyboard, error_keyboard


class MyRecipesListStateHandler(BaseMyRecipesListStateHandler):
    pass

class WaitingUserRecipeStateHandler(BaseStateHandler):

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}\n\nПришлите сообщение с текстом или фото рецепта."

        return "Пришлите сообщение с текстом или фото рецепта."

    def get_keyboard(self, session_data: dict):
        error = session_data["context"].get("error")
        recipe_to_add = session_data["context"].get("recipe_to_add", None)

        if error and recipe_to_add:
            return error_keyboard("send_recipe_to_llm")

        return step_back_or_cancel_keyboard("back", "to_main")


    async def handle_message(self, message:Message, session_data: dict):

        text= self.get_text_from_message(message)
        session_data["context"]["recipe_to_add"] = text
        session_data["context"].pop("error", None)

        result, error = await BreadlabAPIClient.recognize_recipe_text(text)
        if error:
            session_data["context"]["error"] = error
            await self.show_screen(message, session_data)
            return None, session_data
        else:
            if result["status"] == "ok":
                session_data["context"]["recipe_to_edit"]= result["data"]
                session_data["context"].pop("error", None)
                return "open_edit_added_recipe", session_data
            if result["status"] == "error":
                session_data["context"]["error"] = result["message"]
                await self.show_screen(message, session_data)
                return None, session_data

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd=self.get_payload_from_event(event, "cmd")
        if cmd=="send_recipe_to_llm":
            recipe=session_data["context"].get("recipe_to_add")
            result, error = await BreadlabAPIClient.recognize_recipe_text(recipe)

            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data

            if result["status"] == "ok":
                session_data["context"]["recipe_to_edit"] = result["data"]
                session_data["context"].pop("error", None)
                return "open_edit_added_recipe", session_data

            if result["status"] == "error":
                session_data["context"]["error"] = result["message"]
                await self.show_screen(event, session_data)
                return None, session_data
        if cmd in ("back", "to_main", "open_edit_added_recipe"):
            session_data["context"].pop("error",None)

        return await super().handle_event(event, session_data)









