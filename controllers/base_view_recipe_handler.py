from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.base_state_handler import BaseStateHandler
from utils.api_client import BreadlabAPIClient
from utils.formatters import convert_dict_to_pretty_print
from utils.keyboards import error_keyboard, view_recipe_keyboard


class BaseViewRecipeStateHandler(BaseStateHandler):
    mode=None #переопределим в наследниках

    async def show_screen(self, event: MessageEvent | Message, session_data: dict):
        # 1. Пытаемся получить recipe_id
        recipe_id = session_data["context"].get("recipe_id")

        if recipe_id:
            # Случай А: Сохранённый рецепт — загружаем с сервера
            result, error = await BreadlabAPIClient.get_recipe(recipe_id=recipe_id)
            if error:
                session_data["context"]["error"] = error
            else:
                session_data["context"]["recipe"] = result['recipe']["data"]
                session_data["context"]["error"] = None
        else:
            # Случай Б: Новый/загруженный рецепт — берём из контекста
            recipe = (
                    session_data["context"].get("recipe_to_save") or
                    session_data["context"].get("recipe_to_edit") or
                    session_data["context"].get("recipe")
            )
            if recipe:
                # Убедимся, что он лежит в едином ключе `recipe`
                session_data["context"]["recipe"] = recipe
                session_data["context"]["error"] = None
            else:
                session_data["context"]["error"] = "Рецепт не найден"

        # 2. Вызываем родительский show_screen, который возьмёт данные из `recipe` и `error`
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
            return error_keyboard(self._get_retry_command())

        return view_recipe_keyboard(self.mode)

    def _get_retry_command(self) -> str:
        """Команда для кнопки 'Отправить заново'. Переопределяется в наследниках."""
        return "open_view_recipe"