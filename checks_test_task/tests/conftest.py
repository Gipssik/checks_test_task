import asyncio
import time
from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Generator

import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession

from checks_test_task.app import create_app
from checks_test_task.clients.redis import redis_client
from checks_test_task.conf.database import async_session
from checks_test_task.conf.settings import Settings, Env, settings
from checks_test_task.models.base import metadata
from checks_test_task.tests.auth_test_client import AuthenticatedTestClient
from checks_test_task.tests.factories import FACTORIES, UserFactory


async def _create_test_db(engine: AsyncEngine, new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(sa.text("DROP DATABASE IF EXISTS %s" % new_db_name))
        await conn.execute(sa.text("CREATE DATABASE %s" % new_db_name))


async def _drop_test_db(engine: AsyncEngine, new_db_name: str):
    async with engine.connect() as conn:
        conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
        await conn.execute(sa.text("DROP DATABASE %s" % new_db_name))


@pytest.fixture(scope="session")
def test_db_name() -> str:
    return f"checks_tests_{int(time.time())}"


@pytest.fixture(scope="session")
def test_settings(test_db_name: str):
    return Settings(DB_NAME=test_db_name, ENV=Env.TESTING)


@pytest.fixture(scope="session", autouse=True)
async def init_test_db(
    test_settings: Settings,
    test_db_name: str,
) -> AsyncGenerator[None, None]:
    conn_url = settings.sqlalchemy_database_uri
    engine = create_async_engine(conn_url)
    await _create_test_db(engine, test_db_name)
    test_engine = create_async_engine(test_settings.sqlalchemy_database_uri)
    async with test_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    yield

    await test_engine.dispose()
    if metadata.bind:
        await metadata.bind.dispose()
    await _drop_test_db(engine, test_db_name)


@pytest.fixture(scope="session")
async def app(test_settings: Settings) -> FastAPI:
    fastapi_app = create_app(test_settings)
    await redis_client.configure(test_settings)
    return fastapi_app


@pytest.fixture(scope="session")
async def session(app: FastAPI) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        for factory_ in FACTORIES:
            factory_._meta.sqlalchemy_session = session

        yield session


@pytest.fixture(scope="function", autouse=True)
async def clear_db(session: AsyncSession, test_settings: Settings) -> AsyncGenerator[None, None]:
    yield

    await session.execute(sa.text("TRUNCATE {};".format(",".join(table.name for table in metadata.tables.values()))))
    await session.commit()


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client(app: FastAPI, test_settings: Settings) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def auth_client(
    app: "FastAPI",
    client: "AsyncClient",
    mocker: MockerFixture,
    test_settings: "Settings",
    session: "AsyncSession",
) -> AsyncGenerator[AuthenticatedTestClient, None]:
    user = UserFactory()
    await session.commit()
    mocker.patch("checks_test_task.api.dependencies.auth.jwt.decode", return_value={"sub": user.email})
    async with AuthenticatedTestClient(transport=ASGITransport(app=app), base_url="http://test", user=user) as client:
        yield client
