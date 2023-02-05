import asyncio

import pytest
from httpx import AsyncClient

from app.api.v1.apps import app as apps

clients = AsyncClient(app=apps)


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_app_client():
    async with AsyncClient(app=apps) as client:
        yield client
