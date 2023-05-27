import asyncio
import aiohttp
from typing import Any, Generator

import pytest

from tests.functional.settings import test_settings


@pytest.fixture(scope="session", name="event_loop")
def fixture_event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def make_get_request():
    async with aiohttp.ClientSession() as session:
        async def _make_get_request(endpoint: str, params: dict | None = None,
                                    headers: dict | None = None):
            url = test_settings.service_url + endpoint
            params = params if params else {}
            async with session.get(url, params=params,
                                   headers=headers) as response:
                body = await response.json()
                status = response.status
            return {'status': status, 'body': body}

        yield _make_get_request


@pytest.fixture
async def make_post_request():
    async with aiohttp.ClientSession() as session:
        async def _make_post_request(endpoint: str, params: dict | None = None,
                                     headers: dict | None = None):
            url = test_settings.service_url + endpoint
            params = params or {}
            async with session.post(url, json=params,
                                    headers=headers) as response:
                status = response.status
                body = await response.json()
            return {'status': status, 'body': body}

        yield _make_post_request


@pytest.fixture
async def make_delete_request():
    async with aiohttp.ClientSession() as session:
        async def _make_delete_request(endpoint: str):
            url = test_settings.service_url + endpoint
            async with session.delete(url) as response:
                status = response.status
                body = await response.json()
            return {'status': status, 'body': body}

        yield _make_delete_request
