from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from checks_test_task.api.dependencies.db import get_db_session
from checks_test_task.services.check import CheckService
from checks_test_task.services.user import UserService


async def get_user_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    """Dependency to get the user service."""
    return UserService(session)


async def get_check_service(session: AsyncSession = Depends(get_db_session)) -> CheckService:
    """Dependency to get the check service."""
    return CheckService(session)
