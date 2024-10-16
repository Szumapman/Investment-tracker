from redis.asyncio import Redis

from src.database.db import get_db
from src.repositories.abstract import AbstractUserRepo, AbstractTokenRepo, AbstractAccountRepo
from src.repositories.users import PostgresUserRepo
from src.repositories.tokens import PostgresTokenRepo
from src.repositories.accounts import PostgresAccountRepo
from src.database.abstract import AbstractCache
from src.database.cache import RedisCache
from src.config.config import settings


def get_redis(**kwargs) -> Redis:
    """
    Function to get Redis.

    Args:
        **kwargs: redis connection parameters - except: host, port and password
    Returns:
        Redis instance
    """
    redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        **kwargs,
    )
    return redis


def get_cache() -> AbstractCache:
    """
    Function to get cache.
    Returns:
        Cache instance
    """
    return RedisCache()


def get_user_repo() -> AbstractUserRepo:
    return PostgresUserRepo(next(get_db()))


def get_token_repo() -> AbstractTokenRepo:
    return PostgresTokenRepo(next(get_db()))

def get_account_repo() -> AbstractAccountRepo:
    return PostgresAccountRepo(next(get_db()))