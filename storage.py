from typing import Hashable, Any

from vkbottle import ABCStorage, CtxStorage
import json
import redis.asyncio as aioredis

from settings import CURRENT_STORAGE


class RedisStorage(ABCStorage):
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, ttl: int = 1800):
        self.redis = aioredis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.ttl = ttl

    async def get(self, key: str) -> dict | None:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict) -> None:
        await self.redis.set(key, json.dumps(value), ex=self.ttl)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def contains(self, key: str) -> bool:
        return await self.redis.exists(key)


class AsyncCtxStorage:
    """
    Асинхронная обёртка над CtxStorage.
    Позволяет использовать await с методами get/set/delete/contains.
    """

    def __init__(self, default: dict[str, Any] | None = None):
        # Создаём синхронный CtxStorage
        self._storage = CtxStorage(default=default or {})

    async def get(self, key: Hashable) -> Any:
        """Асинхронная обёртка для get"""
        # Просто вызываем синхронный метод
        return self._storage.get(key)

    async def set(self, key: Hashable, value: Any) -> None:
        """Асинхронная обёртка для set"""
        self._storage.set(key, value)

    async def delete(self, key: Hashable) -> None:
        """Асинхронная обёртка для delete"""
        self._storage.delete(key)

    async def contains(self, key: Hashable) -> bool:
        """Асинхронная обёртка для contains"""
        return self._storage.contains(key)


if CURRENT_STORAGE == 'prod':
    storage = RedisStorage(host="breadlab-redis", port=6379)
elif CURRENT_STORAGE == 'dev':
    storage = AsyncCtxStorage()