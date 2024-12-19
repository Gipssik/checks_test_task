from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from checks_test_task.conf.database import async_session


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get a database session"""

    async with async_session() as session:
        yield session
