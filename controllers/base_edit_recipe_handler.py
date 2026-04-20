from vkbottle.bot import Message, MessageEvent
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import error_keyboard, approving_edit_keyboard, update_existing_recipe_keyboard


class BaseEditRecipeStateHandler(BaseStateHandler):

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error")
        if error:
            return f"❌ {error}"

        exists = session_data["context"].get("exists", None)
        if exists:
            message = "Рецепт с таким названием уже существует.\nВведите уникальное название."
            return message

        # Приоритет: recipe_to_save -> recipe_to_edit -> recipe
        recipe = (
                session_data["context"].get("recipe_to_save") or # при редактировании
                session_data["context"].get("recipe_to_edit") or # когда вошли в первый раз
                session_data["context"].get("recipe") # когда пришли из просмотра рецепта: уже существующий рецепт (который есть в базе)
        )

        recipe=convert_dict_to_pretty_print(recipe)
        comment='Режим редактирования.\nПроверьте правильность названий ингредиентов и пропорций.\nМожно вносить правки. Например: "Добавь 2 г соли", или "замени ржаную муку на пшеничную"'
        message=f'{recipe}\n\n{comment}'
        return message

    def get_keyboard(self, session_data: dict):
        return None

    async def handle_message(self, message: Message, session_data: dict):
        session_data["context"].pop("error", None)
        session_data["context"].pop("exists", None)
        instruction = self.get_text_from_message(message)
        recipe_to_edit = (session_data["context"].get("recipe_to_save", None) or
                          session_data["context"].get("recipe_to_edit", None) or
                          session_data["context"].get("recipe", None))

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
            recipe = (
                    session_data["context"].get("recipe_to_save") or
                    session_data["context"].get("recipe_to_edit") or
                    session_data["context"].get("recipe"))

            instruction = session_data["context"].get("instruction", None)
            request = {"recipe": recipe,
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

        if cmd in ("back", "to_main"):
            session_data["context"].pop("error",None)
            session_data["context"].pop("exists", None)
            session_data["context"].pop("recipe_to_save", None)
            session_data["context"].pop("recipe_to_edit", None)
        return await super().handle_event(event, session_data)

class EditAddedRecipeStateHandler(BaseEditRecipeStateHandler):
    def get_keyboard(self, session_data: dict):
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("edit_recipe_with_llm")
        exists=session_data["context"].get("exists")
        if exists:
            return error_keyboard("edit_recipe_with_llm")
        return approving_edit_keyboard("open_save_added_recipe", "rerun_edit_added_recipe")

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "rerun_edit_added_recipe":
            session_data["context"].pop("recipe_to_save",None)
            await self.show_screen(event, session_data)
            return None, session_data

        if cmd == "open_save_added_recipe":
            recipe_to_check = (
                    session_data["context"].get("recipe_to_save") or
                    session_data["context"].get("recipe_to_edit") or
                    session_data["context"].get("recipe")
            )
            user_id=session_data["peer_id"]

            title=recipe_to_check.get("title")

            exists, error = await BreadlabAPIClient.check_recipe_exists(user_id, title)
            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            elif exists:
                session_data["context"]["exists"] = True
                await self.show_screen(event, session_data)
                return None, session_data
            else:
                session_data["context"].pop("error", None)
                session_data["context"].pop("exists", None)
                return cmd, session_data
        return await super().handle_event(event, session_data)


class EditExistingRecipeStateHandler(BaseEditRecipeStateHandler):

    def get_keyboard(self, session_data: dict):
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("edit_recipe_with_llm")

        exists = session_data["context"].get("exists")

        if exists:
            return update_existing_recipe_keyboard

        return approving_edit_keyboard("open_save_edited_existing_recipe", "rerun_edit_existing_recipe")

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "rerun_edit_existing_recipe":
            session_data["context"].pop("recipe_to_save",None)
            await self.show_screen(event, session_data)
            return None, session_data

        if cmd == "open_save_edited_existing_recipe":
            # проверяем на уникальность. если не уникальный, то предлагаем либо изменить имя либо обновить имеющийся
            recipe_to_check = (
                    session_data["context"].get("recipe_to_save") or
                    session_data["context"].get("recipe_to_edit") or
                    session_data["context"].get("recipe")
            )
            user_id = session_data["peer_id"]

            title = recipe_to_check.get("title")

            exists, error = await BreadlabAPIClient.check_recipe_exists(user_id, title)
            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            elif exists:
                session_data["context"]["exists"] = True
                await self.show_screen(event, session_data)
                return None, session_data
            else:
                session_data["context"].pop("error", None)
                session_data["context"].pop("exists", None)
                return cmd, session_data

        return await super().handle_event(event, session_data)
