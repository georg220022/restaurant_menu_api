from collections.abc import AsyncGenerator

from .settings import cache_redis, db_async_session


async def get_db() -> AsyncGenerator:
    asyn_db = db_async_session()
    try:
        yield asyn_db
    finally:
        await asyn_db.close()


async def get_cache():
    try:
        yield cache_redis
    finally:
        await cache_redis.close()
