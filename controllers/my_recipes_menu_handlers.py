from typing import Tuple, Optional

from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_my_recipes_list_handler import BaseMyRecipesListStateHandler
from controllers.base_state_handler import BaseStateHandler
from controllers.base_view_recipe_handler import BaseViewRecipeStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import step_back_or_cancel_keyboard, error_keyboard, view_recipe_keyboard, approving_keyboard, \
    save_or_cancel_keyboard, to_my_recipes_or_main_keyboard


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
                return "open_edit_recipe", session_data
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
                return "open_edit_recipe", session_data

            if result["status"] == "error":
                session_data["context"]["error"] = result["message"]
                await self.show_screen(event, session_data)
                return None, session_data
        if cmd in ("back", "to_main", "open_edit_recipe"):
            session_data["context"].pop("error",None)

        return await super().handle_event(event, session_data)

class EditUserRecipeStateHandler(BaseStateHandler):

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        recipe_to_save = session_data["context"].get("recipe_to_save", None) # при редактировании
        recipe_to_edit = session_data["context"]["recipe_to_edit"] # когда вошли в первый раз
        if error:
            return f"❌ {error}"

        if recipe_to_save:
            recipe=recipe_to_save
        else:
            recipe=recipe_to_edit

        recipe=convert_dict_to_pretty_print(recipe)
        comment='Режим редактирования.\nПроверьте правильность названий ингредиентов и пропорций.\nМожно вносить правки. Например: "Добавь 2 г соли", или "замени ржаную муку на пшеничную"'
        message=f'{recipe}\n\n{comment}'
        return message

    def get_keyboard(self, session_data: dict):
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("edit_recipe_with_llm")

        return approving_keyboard("open_save_user_recipe", "rerun_edit_recipe","back", "to_main")

    async def handle_message(self, message: Message, session_data: dict):
        session_data["context"].pop("error", None)
        instruction = self.get_text_from_message(message)
        recipe_to_edit = session_data["context"].get("recipe_to_edit", None)
        session_data["context"]["instruction"]= instruction


        request={"recipe":recipe_to_edit,
                "instruction":instruction}

        result, error = await BreadlabAPIClient.post("/recipe_edit/",request)
        if error:
            session_data["context"]["error"] = error
            await self.show_screen(message, session_data)
            return None, session_data
        else:
            if result["status"] == "ok":
                session_data["context"]["recipe_to_save"]= result["data"]
                session_data["context"].pop("error", None)
                await self.show_screen(message, session_data)
                return None, session_data
            if result["status"] == "error":
                session_data["context"]["error"] = result["message"]
                await self.show_screen(message, session_data)
                return None, session_data

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "edit_recipe_with_llm":
            recipe_to_save = session_data["context"].get("recipe_to_save", None)
            recipe_to_edit = session_data["context"].get("recipe_to_edit", None)
            instruction = session_data["context"].get("instruction", None)
            if recipe_to_save:
                request = {"recipe": recipe_to_save,
                           "instruction": instruction}
            else:
                request = {"recipe": recipe_to_edit,
                           "instruction": instruction}
            result, error = await BreadlabAPIClient.post("/recipe_edit/", request)
            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            else:
                if result["status"] == "ok":
                    session_data["context"]["recipe_to_save"] = result["data"]
                    session_data["context"].pop("error", None)
                    await self.show_screen(event, session_data)
                    return None, session_data
                if result["status"] == "error":
                    session_data["context"]["error"] = result["message"]
                    await self.show_screen(event, session_data)
                    return None, session_data
        if cmd == "rerun_edit_recipe":
            session_data["context"].pop("recipe_to_save",None)
            await self.show_screen(event, session_data)

        if cmd == "open_save_user_recipe":

            recipe_to_save = session_data["context"].get("recipe_to_save", None)
            recipe_to_edit = session_data["context"].get("recipe_to_edit", None)
            user_id=session_data["peer_id"]

            if recipe_to_save:
                recipe_to_check=recipe_to_save
            else:
                recipe_to_check=recipe_to_edit

            title=recipe_to_check.get("title")

            exists, error = await BreadlabAPIClient.check_recipe_exists(user_id, title)
            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            elif exists:
                session_data["context"]["error"] = "Рецепт с таким названием уже существует.\nВведите уникальное название."
                await self.show_screen(event, session_data)
                return None, session_data
            else:
                session_data["context"].pop("error", None)
                return "open_save_user_recipe", session_data

        if cmd in ("back", "to_main"):
            session_data["context"].pop("error",None)
        return await super().handle_event(event, session_data)


class SaveUserRecipeStateHandler(BaseStateHandler):
    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error", None)
        if error:
            return f"❌ {error}"

        recipe_to_save=session_data["context"].get("recipe_to_save") or session_data["context"].get("recipe_to_edit")
        return convert_dict_to_pretty_print(recipe_to_save)

    def get_keyboard(self, session_data:dict) -> str|None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("confirm_save")
        return save_or_cancel_keyboard

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")

        if cmd == "confirm_save":
            recipe_to_save = session_data["context"].get("recipe_to_save") or session_data["context"].get("recipe_to_edit")
            user_id = session_data["peer_id"]

            result, error = await BreadlabAPIClient.save_recipe(user_id, recipe_to_save)

            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            session_data["context"].pop("error", None)
            return "confirm_save", session_data

        if cmd in ("back", "to_main"):
            session_data["context"].pop("error", None)

        return await super().handle_event(event, session_data)


class SaveSuccessStateHandler(BaseStateHandler):
    def get_message(self, session_data: dict) -> str:
        return  "✅ Рецепт сохранён!"

    def get_keyboard(self, session_data: dict) -> str:
        return to_my_recipes_or_main_keyboard









