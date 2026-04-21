from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import recipes_keyboard, error_keyboard

class BaseMyRecipesListStateHandler(BaseStateHandler):
    async def show_screen(self, event, session_data, custom_message=None, custom_keyboard=None):
        page = session_data["context"].get("page", 1)
        user_id = session_data["peer_id"]

        result, error = await BreadlabAPIClient.get_user_recipes(user_id, page=page)
        if error:
            session_data["context"]["error"] = error
            session_data["context"]["recipes"] = []
        else:
            # 👇 Парсим и сохраняем в context
            session_data["context"]["error"] = None
            session_data["context"]["recipes"] = result['recipes']
            session_data["context"]["current_page"] = result['page']
            session_data["context"]["has_next"] = result['has_next']
            session_data["context"]["has_prev"] = result['has_prev']
            session_data["context"]["total_pages"] = result['total_pages']

        await super().show_screen(event, session_data)

    def get_keyboard(self, session_data: dict) -> str|None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("show_recipes_list")

        recipes = session_data["context"]["recipes"]
        page = session_data["context"]["current_page"]
        has_prev = session_data["context"]["has_prev"]
        has_next = session_data["context"]["has_next"]

        return recipes_keyboard(recipes, page, has_prev, has_next)


    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}"
        page = session_data["context"]["current_page"]
        total = session_data["context"]["total_pages"]
        return f"📋 Рецепты — страница {page} из {total}"

    async def handle_event(self, event, session_data):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "show_recipes_list":
            page = self.get_payload_from_event(event, "page", 1)
            session_data["context"]["page"] = page
            await self.show_screen(event, session_data)
            return None, session_data
        if cmd == "open_view_recipe":
            recipe_id = self.get_payload_from_event(event, "recipe_id")
            session_data["context"]["recipe_id"] = recipe_id

        return await super().handle_event(event, session_data)