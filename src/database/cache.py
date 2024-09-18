import pickle

from redis.asyncio import Redis

from src.database.abstract import AbstractCache
from src.config.config import settings


class RedisCache(AbstractCache):
    def __init__(self):
        self.redis_connection = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            password=settings.redis_password,
            db=0,
        )

    async def get_from_cache(self, key: str) -> bytes | None:
        return await self.redis_connection.get(key)

    async def set_to_cache(self, key: str, value: object, expire: int) -> None:
        await self.redis_connection.set(key, pickle.dumps(value))
        await self.redis_connection.expire(key, expire)

    async def delete_from_cache(self, key: str) -> None:
        await self.redis_connection.delete(key)
