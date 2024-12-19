from datetime import timedelta
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from checks_test_task.api.dependencies.service import get_user_service
from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.conf.settings import settings
from checks_test_task.exceptions import UnauthorizedException
from checks_test_task.schemas.common import OKResponse, Token
from checks_test_task.schemas.user import UserCreateSchema
from checks_test_task.services.user import UserService
from checks_test_task.utils.auth import authenticate_user, create_access_token

router = APIRouter()


@router.post(
    "/register",
    summary="Register user",
    status_code=HTTPStatus.CREATED,
    response_model=OKResponse,
)
async def register_user(
    create_user_data: UserCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> OKResponse:
    await user_service.create_user(create_user_data)
    return OKResponse(OK=True)


@router.post(
    "/token",
    summary="Login user for access token",
    status_code=HTTPStatus.OK,
    response_model=Token,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, user_service)
    if not user:
        raise UnauthorizedException(ErrorMessages.INVALID_CREDENTIALS)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
