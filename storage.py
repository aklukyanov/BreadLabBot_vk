from vkbottle import ABCStorage
import json
import redis.asyncio as aioredis


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

storage = RedisStorage(host="breadlab-redis", port=6379)