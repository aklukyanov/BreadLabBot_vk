from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.my_recipes_list_handler import BaseMyRecipesListStateHandler
from controllers.base_state_handler import BaseStateHandler
from utils.formatters import convert_dict_to_pretty_print

from utils.keyboards import load_recipe_keyboard, recipes_keyboard_proportions_calc, error_keyboard, \
    step_back_or_cancel_keyboard
from utils.messages import proportions_calc_description


class LoadRecipeProportionsCalcStateHandler(BaseStateHandler):

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        session_data["context"].clear()
        return await super().show_screen(event, session_data)

    def get_message(self, session_data: dict) -> str:
        return proportions_calc_description

    def get_keyboard(self, session_data: dict) -> str:
        return load_recipe_keyboard

class ChooseRecipeProportionsCalcStateHandler(BaseMyRecipesListStateHandler):
    def get_keyboard(self, session_data: dict) -> str|None:

        error = session_data["context"].get("error")
        if error:
            return error_keyboard("show_recipes_list")

        recipes = session_data["context"]["recipes"]
        page = session_data["context"]["current_page"]
        has_prev = session_data["context"]["has_prev"]
        has_next = session_data["context"]["has_next"]

        return recipes_keyboard_proportions_calc(recipes, page, has_prev, has_next)

    async def handle_event(self, event, session_data):
        cmd = self.get_payload_from_event(event, "cmd")

        if cmd == "enter_recipe":
            # Сохраняем recipe_id
            recipe_id = self.get_payload_from_event(event, "recipe_id")
            session_data["context"]["recipe_id"] = recipe_id
            return "enter_recipe", session_data
        return await super().handle_event(event, session_data)


class ShowResultProportionsCalcStateHandler(BaseStateHandler):
    def get_message(self, session_data: dict) -> str:
        recipe = session_data["context"]["result_recipe"]
        multiplier = session_data["context"]["multiplier"]
        return convert_dict_to_pretty_print(recipe, multiplier=multiplier)

    def get_keyboard(self, session_data: dict) -> str:
        return step_back_or_cancel_keyboard('back', 'to_main')

    async def show_screen(self, event, session_data):
        await super().show_screen(event, session_data)

