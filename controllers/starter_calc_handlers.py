from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent
from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.keyboards import choose_direction_keyboard, step_back_or_cancel_keyboard, \
    choosing_starter_proportions_50to100_keyboard, choosing_starter_proportions_100to50_keyboard, error_keyboard

from utils.messages import starter_calc_description, original_proportions_query50, original_proportions_query100, \
    wrong_proportions, target_proportions_query, water_msg50to100, water_msg100to50, starter_calc_result_message


class ChooseDirectionStateHandler(BaseStateHandler):
    """Экран выбора направления пересчёта закваски (50→100 или 100→50)."""

    def get_message(self, context: dict) -> str:
        return starter_calc_description

    def get_keyboard(self, context: dict) -> str:
        return choose_direction_keyboard

    async def handle_event(self, event: MessageEvent, session_data):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "enter_direction":
            direction = self.get_payload_from_event(event, "direction")
            session_data["context"]["direction"] = direction
            return "enter_direction", session_data
        if cmd in ("back", "to_main"):
            session_data["context"].clear()
            return cmd, session_data


class WaitingSourdoughWeightStateHandler(BaseStateHandler):
    """Экран ввода веса закваски, воды и муки."""

    def get_message(self, session_data: dict) -> str:
        if session_data["context"]["direction"] == "50to100":
            return original_proportions_query50
        if session_data["context"]["direction"] == "100to50":
            return original_proportions_query100

    def get_keyboard(self, context: dict) -> str:
        return step_back_or_cancel_keyboard("back", "to_main")

    async def handle_event(self, event: MessageEvent, session_data):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd in ("back", "to_main"):
            # Очищаем только временные данные калькулятора
            temp_keys = ["direction", "original_starter", "original_water", "original_flour"]
            for key in temp_keys:
                session_data["context"].pop(key, None)
            return cmd, session_data

    async def handle_message(self, message: Message, session_data):
        text = self.get_text_from_message(message)
        try:
            ingredients = [int(ingredient) for ingredient in text.split() if int(ingredient) > 0]
            starter, water, flour = ingredients

            session_data["context"]["original_starter"] = starter
            session_data["context"]["original_water"] = water
            session_data["context"]["original_flour"] = flour
            return "enter_weight", session_data
        except (ValueError, TypeError):
            await message.answer(
                wrong_proportions,
                keyboard=step_back_or_cancel_keyboard("back", "to_main")
            )
            return None, session_data


class ChoosingStarterProportionsStateHandler(BaseStateHandler):
    """Экран выбора пропорций закваски для расчёта."""

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}"
        if session_data["context"]["direction"] == "50to100":
            return target_proportions_query.format("100% влажности")
        if session_data["context"]["direction"] == "100to50":
            return target_proportions_query.format("50% влажности")

    def get_keyboard(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("calculate")

        if session_data["context"]["direction"] == "50to100":
            return choosing_starter_proportions_50to100_keyboard
        if session_data["context"]["direction"] == "100to50":
            return choosing_starter_proportions_100to50_keyboard

    async def handle_event(self, event: MessageEvent, session_data):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "calculate":
            starter_proportions = self.get_payload_from_event(event, "starter_proportions")
            parts = [float(x) for x in starter_proportions.split(':')]
            starter, water, flour = parts

            request_data = {
                "direction": session_data["context"]["direction"],
                "original_starter": session_data["context"]["original_starter"],
                "original_water": session_data["context"]["original_water"],
                "original_flour": session_data["context"]["original_flour"],
                "starter_part": starter,
                "water_part": water,
                "flour_part": flour
            }

            result, error = await BreadlabAPIClient.post("/starter_calc/", request_data)

            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            if result:
                session_data["context"]["result"] = result
                session_data["context"].pop("error", None)
                return "calculate", session_data

        return await super().handle_event(event, session_data)


class ShowResultStarterCalcStateHandler(BaseStateHandler):
    """Экран показа результата расчёта закваски."""

    def get_message(self, context: dict) -> str:
        direction = context["context"]["direction"]
        if direction == "50to100":
            water_msg = water_msg50to100.format(water_to_remove=context["context"]["result"]['water_to_remove'])
            hydro = 100
        if direction == "100to50":
            water_msg = water_msg100to50.format(water_to_add=context["context"]["result"]['water_to_add'])
            hydro = 50

        message = starter_calc_result_message.format(
            hydro=hydro,
            starter=context["context"]["result"]['starter'],
            water=context["context"]["result"]['water'],
            flour=context["context"]["result"]['flour'],
            total_weight=context["context"]["result"]['total_weight'],
            water_msg=water_msg
        )
        return message

    def get_keyboard(self, context: dict) -> str:
        return step_back_or_cancel_keyboard("back", "to_main")