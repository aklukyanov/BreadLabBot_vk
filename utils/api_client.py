from typing import Tuple, Optional

import aiohttp

from logger import api_client_logger


class BreadlabAPIClient:
    BASE_URL = "http://127.0.0.1:8000/api"

    http_session=None

    @classmethod
    def get_or_create_session(cls):
        if cls.http_session is None or cls.http_session.closed:
            cls.http_session = aiohttp.ClientSession()
        return cls.http_session

    @classmethod
    async def close(cls):
        """Закрывает сессию (вызывается при остановке бота)"""
        if cls.http_session and not cls.http_session.closed:
            await cls.http_session.close()
            cls.http_session = None

    @classmethod
    async def post(cls, endpoint: str, request_data: dict):
        session=cls.get_or_create_session()
        api_client_logger.info(f"POST [{cls.BASE_URL}{endpoint}]: {request_data}")
        try:
            async with session.post(
                    f"{cls.BASE_URL}{endpoint}",
                    json=request_data,
                    timeout=60
            ) as response:
                response_data = await response.json()
                api_client_logger.info(
                    f"API response [{cls.BASE_URL}{endpoint}]: status={response.status}, body={response_data}")
                if response.status == 200:
                    return response_data, None
                elif response.status == 201:
                    return await response.json(), None
                else:
                    return None, "Ошибка сервера."
        except Exception as e:
            api_client_logger.error(f"API error [{cls.BASE_URL}{endpoint}]: {type(e).__name__}: {e}")
            return None, f"Сервер недоступен."

    @classmethod
    async def get(cls, endpoint: str, params: dict=None):
        session = cls.get_or_create_session()
        try:
            api_client_logger.info(f"GET [{cls.BASE_URL}{endpoint}]")
            async with session.get(
                    f"{cls.BASE_URL}{endpoint}",
                    params=params,
                    timeout=10
            ) as response:
                api_client_logger.info(f"API response [{cls.BASE_URL}{endpoint}]: {response}")
                if response.status == 200:
                    return await response.json(), None
                else:
                    return None, "Ошибка сервера."
        except Exception as e:
            api_client_logger.error(f"API error [{cls.BASE_URL}{endpoint}]: {e}")
            return None, f"Сервер недоступен."

    @classmethod
    async def patch(cls, endpoint: str, request_data: dict):
        """PATCH-запрос к API."""
        session = cls.get_or_create_session()
        try:
            api_client_logger.info(f"PATCH [{cls.BASE_URL}{endpoint}]: {request_data}")
            async with session.patch(
                    f"{cls.BASE_URL}{endpoint}",
                    json=request_data,
                    timeout=10
            ) as response:
                response_data = await response.json()
                api_client_logger.info(
                    f"API response [{cls.BASE_URL}{endpoint}]: status={response.status}, body={response_data}"
                )
                if response.status in (200, 201):
                    return response_data, None
                else:
                    return None, f"Ошибка сервера (код {response.status})"
        except Exception as e:
            api_client_logger.error(f"API error [PATCH {endpoint}]: {type(e).__name__}: {e}")
            return None, "Сервер недоступен."

    @classmethod
    async def patch_recipe(cls, recipe_id: str, recipe_data: dict):
        """Обновить существующий рецепт (PATCH)."""
        request_data = {
            "recipe": {
                "data": recipe_data
            }
        }
        return await cls.patch(f"/recipes/{recipe_id}/update/", request_data)

    @classmethod
    async def get_user_recipes(cls, external_id: str, page: int = 1):
        """Получить рецепты пользователя с пагинацией"""
        return await cls.get(
            f"/users/{external_id}/recipes/",
            params={"page": page}
        )
    @classmethod
    async def get_recipe(cls, recipe_id: str):
        """Получить один рецепт по ID"""
        return await cls.get(f"/recipes/{recipe_id}/")

    @classmethod
    async def delete_recipe(cls, recipe_id: str):
        """Удалить рецепт по ID."""
        session = cls.get_or_create_session()
        try:
            api_client_logger.info(f"DELETE [{cls.BASE_URL}/recipes/{recipe_id}/delete/]")
            async with session.delete(
                    f"{cls.BASE_URL}/recipes/{recipe_id}/delete/",
                    timeout=10
            ) as response:
                api_client_logger.info(f"API response [{cls.BASE_URL}/recipes/{recipe_id}/delete/]: {response}")
                if response.status == 200:
                    return await response.json(), None
                else:
                    return None, "Ошибка сервера."

        except Exception as e:
            api_client_logger.error(f"API error [{cls.BASE_URL}/recipes/{recipe_id}/delete/]: {e}")
            return None, f"Сервер недоступен."

    @classmethod
    async def multiply_recipe(cls, multiplier: int, recipe: dict) -> Tuple[Optional[dict], Optional[str]]:
        """Умножить рецепт на множитель."""
        return await cls.post(
            "/recipe_multiply/",
            {"multiplier": multiplier, "recipe": recipe}
        )
    @classmethod
    async def recognize_recipe_text(cls, recipe:str):
        request={"recipe": recipe}
        return await cls.post(
            "/recognize_text/",
            request)

    @classmethod
    async def save_recipe(cls, user_id: str, recipe_data: dict, parent_id: int = None):
        """Сохранить рецепт. Возвращает (data, error)."""
        request_data = {
            "user_id": user_id,
            "parent_id": parent_id,
            "recipe": {"data": recipe_data}
        }
        return await cls.post("/recipes/", request_data)

    @classmethod
    async def check_recipe_exists(cls, user_id: str, title: str) -> Tuple[bool, Optional[str]]:
        result, error = await cls.get(
            "/recipe_check_exists/",
            params={"user_id": user_id, "title": title}
        )
        if error:
            return False, error
        return result.get("exists", False), None

