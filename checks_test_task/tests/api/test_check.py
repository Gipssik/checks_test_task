from http import HTTPStatus

import sqlalchemy as sa
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.models import Check
from checks_test_task.tests.auth_test_client import AuthenticatedTestClient


async def test_create_check(auth_client: AuthenticatedTestClient, session: AsyncSession):
    """Test creating a check. Success."""

    response = await auth_client.post(
        "/checks",
        json={
            "products": [
                {"name": "product 1", "description": "description 1", "price_per_unit": 123.1, "quantity": 3},
                {"name": "product 2", "price_per_unit": 321, "quantity": 2},
            ],
            "payment": {"payment_type": "CASH", "amount": 1500},
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json == {
        "id": 1,
        "products": [
            {
                "name": "product 1",
                "description": "description 1",
                "price_per_unit": 123.1,
                "quantity": 3,
                "total_price": 369.3,
            },
            {
                "name": "product 2",
                "description": None,
                "price_per_unit": 321.0,
                "quantity": 2,
                "total_price": 642.0,
            },
        ],
        "payment": {"payment_type": "CASH", "amount": 1500.0},
        "total_price": 1011.3,
        "rest": 488.7,
    }

    check = await session.scalar(sa.select(Check).where(Check.id == response_json["id"]))
    assert float(check.total_price) == 1011.3
    assert float(check.rest) == 488.7


async def test_create_check_with_invalid_payment_amount(auth_client: AuthenticatedTestClient, session: AsyncSession):
    """Test creating a check with invalid payment amount. Fail."""

    response = await auth_client.post(
        "/checks",
        json={
            "products": [
                {"name": "product 1", "description": "description 1", "price_per_unit": 123.1, "quantity": 3},
                {"name": "product 2", "price_per_unit": 321, "quantity": 2},
            ],
            "payment": {"payment_type": "CASH", "amount": 150},
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": ErrorMessages.CHECK_AMOUNT_EXCEEDED}


async def test_get_text_check_without_auth(
    auth_client: AuthenticatedTestClient,
    client: AsyncClient,
    session: AsyncSession,
):
    """Test getting a text check without authentication. Success."""

    response = await auth_client.post(
        "/checks",
        json={
            "products": [
                {"name": "product 1", "description": "description 1", "price_per_unit": 123.1, "quantity": 3},
                {"name": "product 2", "price_per_unit": 321, "quantity": 2},
            ],
            "payment": {"payment_type": "CASH", "amount": 1500},
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    response = await client.get(f"/checks/{response.json()['id']}")
    assert type(response.text) is str


async def test_get_user_checks(auth_client: AuthenticatedTestClient, session: AsyncSession):
    """Test getting user checks. Success."""

    for i in range(3):
        await auth_client.post(
            "/checks",
            json={
                "products": [
                    {
                        "name": f"{i} product 1",
                        "description": f"{i} description 1",
                        "price_per_unit": 123.1,
                        "quantity": 3,
                    },
                    {
                        "name": f"{i} product 2",
                        "price_per_unit": 321 + i,
                        "quantity": 2,
                    },
                ],
                "payment": {"payment_type": "CASH", "amount": 1500},
            },
        )

    response = await auth_client.get("/checks")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["items"]
    assert len(response_json) == 3
    assert response_json[0]["products"][0]["name"] == "0 product 1"
    assert response_json[1]["products"][0]["name"] == "1 product 1"
    assert response_json[2]["products"][0]["name"] == "2 product 1"

    response = await auth_client.get("/checks", params={"total_price__gte": 1012})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["items"]
    assert len(response_json) == 2
    assert response_json[0]["products"][0]["name"] == "1 product 1"
    assert response_json[1]["products"][0]["name"] == "2 product 1"

    response = await auth_client.get("/checks", params={"total_price__lte": 1012})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["items"]
    assert len(response_json) == 1
    assert response_json[0]["products"][0]["name"] == "0 product 1"

    response = await auth_client.get("/checks", params={"payment_type": "CASH"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["items"]
    assert len(response_json) == 3
    assert response_json[0]["products"][0]["name"] == "0 product 1"
    assert response_json[1]["products"][0]["name"] == "1 product 1"
    assert response_json[2]["products"][0]["name"] == "2 product 1"

    response = await auth_client.get("/checks", params={"payment_type": "CASHLESS"})
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()["items"]
    assert len(response_json) == 0
