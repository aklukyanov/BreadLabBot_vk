from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import error_keyboard, save_or_cancel_keyboard, save_choice_keyboard, \
    to_my_recipes_or_main_keyboard, confirm_update_existing_recipe_keyboard
from utils.messages import save_edited_recipe_warning_message, save_as_version_success_message, \
    update_existing_recipe_success_message, save_as_new_success_message


class BaseSaveRecipeStateHandler(BaseStateHandler):
    """
    Базовый класс для экранов сохранения рецепта.

    Содержит общую логику:
    - Отображение рецепта и ошибок
    - Отправка запроса на сохранение
    - Очистка временных данных при уходе
    """

    def get_message(self, session_data: dict) -> str:
        error = session_data["context"].get("error", None)
        if error:
            return f"❌ {error}"

        recipe_to_save = (session_data["context"].get("recipe_to_save") or
                          session_data["context"].get("recipe_to_edit") or
                          session_data["context"].get("recipe"))
        return convert_dict_to_pretty_print(recipe_to_save)

    def get_keyboard(self, session_data: dict) -> str | None:
        error = session_data["context"].get("error")
        if error:
            return error_keyboard("confirm_save")
        return save_or_cancel_keyboard

    async def _save_recipe(self, event, session_data: dict, user_id: str, recipe: dict, parent_id: str = None):
        """
        Сохраняет рецепт и обрабатывает ответ.

        Returns:
            (result, error) — результат запроса.
        """
        result, error = await BreadlabAPIClient.save_recipe(user_id, recipe, parent_id)
        if error:
            session_data["context"]["error"] = error
            await self.show_screen(event, session_data)
            return None, error
        return result, None

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd in ("confirm_save", "save_as_version"):
            recipe_to_save = session_data["context"].get("recipe_to_save") or session_data["context"].get(
                "recipe_to_edit")
            user_id = session_data["peer_id"]
            recipe_id = session_data["context"].get("recipe_id")

            result, error = await self._save_recipe(event, session_data, user_id, recipe_to_save, recipe_id)
            if error:
                return None, session_data

            session_data["context"].pop("error", None)
            session_data["context"].pop("save_as_new", None)
            session_data["context"].pop("save_as_version", None)
            session_data["context"].pop("update_existing_recipe", None)
            if cmd == "save_as_version":
                session_data["context"]["save_as_version"] = True
            return cmd, session_data

        if cmd in ("back", "to_main"):
            session_data["context"].pop("error", None)
            session_data["context"].pop("exists", None)
            session_data["context"].pop("update_existing_recipe", None)
            session_data["context"].pop("save_as_version", None)
            session_data["context"].pop("save_as_new", None)

        return await super().handle_event(event, session_data)


class SaveAddedRecipeStateHandler(BaseSaveRecipeStateHandler):
    """Сохранение нового (добавленного) рецепта."""

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "confirm_save":
            recipe_to_save = session_data["context"].get("recipe_to_save") or session_data["context"].get(
                "recipe_to_edit")
            user_id = session_data["peer_id"]

            result, error = await self._save_recipe(event, session_data, user_id, recipe_to_save)
            if error:
                return None, session_data

            session_data["context"].pop("error", None)
            return cmd, session_data
        return await super().handle_event(event, session_data)


class SaveEditedExistingRecipesStateHandler(BaseSaveRecipeStateHandler):
    """
    Сохранение отредактированного существующего рецепта.

    Предлагает выбор: сохранить как новый, как версию или обновить существующий.
    """

    def get_keyboard(self, session_data: dict) -> str | None:
        error = session_data["context"].get("error")
        exists = session_data["context"].get("exists", None)
        if error:
            return error_keyboard("confirm_save")
        if exists:
            return confirm_update_existing_recipe_keyboard
        return save_choice_keyboard

    def get_message(self, session_data: dict) -> str:
        exists = session_data["context"].get("exists", None)
        error = session_data["context"].get("error")
        if exists and not error:
            base_message = super().get_message(session_data)
            warning = save_edited_recipe_warning_message
            message = f"{base_message}\n{warning}"
            return message
        return super().get_message(session_data)

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "confirm_update_existing_recipe":
            recipe_id = session_data["context"].get("recipe_id")
            recipe_to_update = (session_data["context"].get("recipe_to_save") or
                                session_data["context"].get("recipe_to_edit") or
                                session_data["context"].get("recipe"))
            result, error = await BreadlabAPIClient.patch_recipe(recipe_id, recipe_to_update)
            if error:
                session_data["context"]["error"] = error
                await self.show_screen(event, session_data)
                return None, session_data
            session_data["context"].pop("error", None)
            session_data["context"].pop("save_as_new", None)
            session_data["context"].pop("save_as_version", None)
            session_data["context"]["update_existing_recipe"] = True
            return cmd, session_data

        if cmd == "save_as_new":
            recipe_to_save = session_data["context"].get("recipe_to_save") or session_data["context"].get(
                "recipe_to_edit")
            user_id = session_data["peer_id"]
            result, error = await self._save_recipe(event, session_data, user_id, recipe_to_save)
            if error:
                return None, session_data
            session_data["context"].pop("save_as_new", None)
            session_data["context"].pop("save_as_version", None)
            session_data["context"].pop("update_existing_recipe", None)
            session_data["context"].pop("error", None)
            session_data["context"]["save_as_new"] = True
            return cmd, session_data

        return await super().handle_event(event, session_data)


class SaveSuccessStateHandler(BaseStateHandler):
    """Экран успешного сохранения рецепта. Показывает сообщение и кнопки навигации."""

    def get_message(self, session_data: dict) -> str:
        recipe = (
                session_data["context"].get("recipe_to_save") or
                session_data["context"].get("recipe_to_edit") or
                session_data["context"].get("recipe")
        )
        update_existing_recipe = session_data["context"].get("update_existing_recipe")
        save_as_new = session_data["context"].get("save_as_new")
        save_as_version = session_data["context"].get("save_as_version")

        new_recipe_title = recipe.get("title")

        if save_as_version:
            parent_recipe = session_data["context"].get("recipe")
            parent_recipe_title = parent_recipe.get("title")
            message = save_as_version_success_message.format(new_recipe_title=new_recipe_title, parent_recipe_title=parent_recipe_title)
        elif update_existing_recipe:
            message = update_existing_recipe_success_message.format(new_recipe_title=new_recipe_title)
        elif save_as_new:
            message = save_as_new_success_message.format(new_recipe_title=new_recipe_title)
        else:
            message = "✅ Рецепт сохранён!"
        return message

    def get_keyboard(self, session_data: dict) -> str:
        return to_my_recipes_or_main_keyboard

    async def handle_event(self, event: MessageEvent, session_data: dict):
        cmd = self.get_payload_from_event(event, "cmd")
        if cmd == "back":
            temp_keys = [
                "error", "exists", "update_existing_recipe",
                "save_as_version", "save_as_new", "recipe_to_save", "recipe_to_edit",
                "parent_title"
            ]
            for key in temp_keys:
                session_data["context"].pop(key, None)

        return await super().handle_event(event, session_data)