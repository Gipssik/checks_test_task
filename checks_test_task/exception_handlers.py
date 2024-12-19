import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from checks_test_task.exceptions import (
    DoesNotExistException,
    UnauthorizedException,
    HTTPClientException,
    AlreadyExistsException,
    ValidationException,
)

logger = logging.getLogger(__name__)


def http_client_exception_handler(request: Request, exc: HTTPClientException) -> Response:
    logger.error({"message": str(exc)})
    return JSONResponse(
        status_code=HTTPStatus.BAD_GATEWAY,
        content=HTTPStatus.BAD_GATEWAY.phrase,
    )


async def does_not_exist_exception_handler(request: Request, exc: DoesNotExistException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(exc)),
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(exc)),
    )


async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(exc)),
    )


async def validation_exception_handler(request: Request, exc: ValidationException) -> Response:
    return await http_exception_handler(
        request=request,
        exc=HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(exc)),
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(HTTPClientException)(http_client_exception_handler)
    app.exception_handler(DoesNotExistException)(does_not_exist_exception_handler)
    app.exception_handler(UnauthorizedException)(unauthorized_exception_handler)
    app.exception_handler(AlreadyExistsException)(already_exists_exception_handler)
    app.exception_handler(ValidationException)(validation_exception_handler)
