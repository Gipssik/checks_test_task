from http import HTTPStatus

from httpx import AsyncClient
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.models import User
from checks_test_task.tests.factories import UserFactory
from checks_test_task.utils.password import verify_password


async def test_register_user(client: AsyncClient, session: AsyncSession):
    """Test register user. Success."""

    response = await client.post(
        "/users/register", json={"email": "test@gmail.com", "password": "test", "name": "Test"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"OK": True}

    user = await session.scalar(sa.select(User).where(User.email == "test@gmail.com"))
    assert user.email == "test@gmail.com"
    assert user.name == "Test"
    assert verify_password("test", user.password)


async def test_register_user_with_existing_email(client: AsyncClient, session: AsyncSession):
    """Test register user with existing email. Fail."""

    UserFactory.create(email="test@gmail.com")
    await session.commit()

    response = await client.post(
        "/users/register", json={"email": "test@gmail.com", "password": "test", "name": "Test"}
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": ErrorMessages.USER_ALREADY_EXISTS}


async def test_get_access_token(client: AsyncClient):
    """Test get access token. Success."""

    response = await client.post(
        "/users/register", json={"email": "test@gmail.com", "password": "test", "name": "Test"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"OK": True}

    response = await client.post("/users/token", data={"username": "test@gmail.com", "password": "test"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["access_token"]
    assert response_json["token_type"] == "bearer"


async def test_get_access_token_with_invalid_password(client: AsyncClient):
    """Test get access token with invalid password. Fail."""

    response = await client.post(
        "/users/register", json={"email": "test@gmail.com", "password": "test", "name": "Test"}
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"OK": True}

    response = await client.post("/users/token", data={"username": "test@gmail.com", "password": "wrong"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": ErrorMessages.INVALID_CREDENTIALS}
