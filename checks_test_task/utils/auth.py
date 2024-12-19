from datetime import timedelta, datetime, timezone

import jwt

from checks_test_task.conf.settings import settings
from checks_test_task.models import User
from checks_test_task.services.user import UserService
from checks_test_task.utils.password import verify_password


async def authenticate_user(
    username: str,
    password: str,
    user_service: UserService,
) -> User | bool:
    user = await user_service.get_user_by_email(username)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
