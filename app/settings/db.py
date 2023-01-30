from .settings import db_async_session, cache_redis
from typing import AsyncGenerator


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
