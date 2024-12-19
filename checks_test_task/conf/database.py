from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from checks_test_task.conf.settings import settings

engine = create_async_engine(settings.sqlalchemy_database_uri, pool_size=15, max_overflow=30, pool_pre_ping=True)
async_session = sessionmaker(None, expire_on_commit=False, class_=AsyncSession)
