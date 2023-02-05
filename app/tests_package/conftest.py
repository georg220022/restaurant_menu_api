import asyncio

import pytest
from httpx import AsyncClient

from api.v1.apps import app as app_fastapi

clients = AsyncClient(app=app_fastapi)


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_app_client():
    async with AsyncClient(app=app_fastapi) as client:
        yield client
