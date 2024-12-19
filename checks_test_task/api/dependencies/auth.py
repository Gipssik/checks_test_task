import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer

from checks_test_task.api.dependencies.service import get_user_service
from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.conf.settings import settings
from checks_test_task.exceptions import UnauthorizedException
from checks_test_task.models import User
from checks_test_task.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token", scheme_name="ServiceAuthHTTPBearer", auto_error=False)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Dependency to get the current user from the token"""

    if not token:
        raise UnauthorizedException(ErrorMessages.USER_NOT_AUTHORIZED)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email = payload.get("sub")
    except jwt.InvalidTokenError:
        raise UnauthorizedException(ErrorMessages.USER_NOT_AUTHORIZED)

    user = await user_service.get_user_by_email(user_email)
    if not user:
        raise UnauthorizedException(ErrorMessages.USER_NOT_AUTHORIZED)

    return user
