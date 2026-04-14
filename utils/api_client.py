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
                    timeout=10
            ) as response:
                api_client_logger.info(f"API response [{cls.BASE_URL}{endpoint}]: {response}")
                if response.status == 200:
                    return await response.json(), None
                else:
                    return None, "Ошибка сервера. Попробуйте еще раз!"
        except Exception as e:
            api_client_logger.error(f"API error [{cls.BASE_URL}{endpoint}]: {e}")
            return None, f"Сервер недоступен. Попробуйте еще раз!"

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
                    return None, "Ошибка сервера. Попробуйте еще раз!"
        except Exception as e:
            api_client_logger.error(f"API error [{cls.BASE_URL}{endpoint}]: {e}")
            return None, f"Сервер недоступен. Попробуйте еще раз!"







