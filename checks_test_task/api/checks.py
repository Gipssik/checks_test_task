from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from starlette.responses import Response

from checks_test_task.api.dependencies.auth import get_current_user
from checks_test_task.api.dependencies.service import get_check_service
from checks_test_task.clients.redis import redis_client
from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.exceptions import DoesNotExistException
from checks_test_task.filters.check import CheckFilter
from checks_test_task.models import User
from checks_test_task.schemas.check import CheckCreateSchema, CheckGetSchema
from checks_test_task.services.check import CheckService

router = APIRouter()


@router.post(
    "",
    summary="Create a new check",
    status_code=HTTPStatus.OK,
    response_model=CheckGetSchema,
)
async def create_check(
    create_check_data: CheckCreateSchema,
    check_service: CheckService = Depends(get_check_service),
    current_user: User = Depends(get_current_user),
) -> CheckGetSchema:
    new_check = await check_service.create_check(create_check_data, current_user.id)
    return CheckGetSchema.from_orm(new_check)


@router.get(
    "",
    summary="Get user's checks",
    status_code=HTTPStatus.OK,
    response_model=Page[CheckGetSchema],
)
async def get_checks(
    check_filter: CheckFilter = FilterDepends(CheckFilter),
    check_service: CheckService = Depends(get_check_service),
    current_user: User = Depends(get_current_user),
) -> Page[CheckGetSchema]:
    return await check_service.get_checks(check_filter, current_user.id)


@router.get(
    "/{check_id}",
    summary="Get text representation of a check",
    status_code=HTTPStatus.OK,
)
async def get_formatted_check(
    check_id: int,
    check_service: CheckService = Depends(get_check_service),
):
    cache_key = f"check:{check_id}"
    if cached_response := (await redis_client.get(cache_key)):
        return Response(content=cached_response, media_type="text/plain")

    check = await check_service.get_check(check_id)

    if check is None:
        raise DoesNotExistException(ErrorMessages.CHECK_DOES_NOT_EXIST)

    check_str = await check_service.get_formatted_check(check)

    await redis_client.set(cache_key, check_str)

    return Response(content=check_str, media_type="text/plain")
