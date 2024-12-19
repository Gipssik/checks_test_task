from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer

from checks_test_task.conf.constants import PaymentType


FloatDecimal = Annotated[Decimal, PlainSerializer(lambda x: float(x), return_type=float, when_used="json")]


class ProductBaseSchema(BaseModel):
    name: str
    description: str | None = None
    price_per_unit: FloatDecimal
    quantity: int


class ProductSchema(ProductBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    total_price: FloatDecimal


class PaymentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_type: PaymentType
    amount: FloatDecimal


class CheckCreateSchema(BaseModel):
    products: list[ProductBaseSchema]
    payment: PaymentSchema


class CheckGetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    products: list[ProductSchema]
    payment: PaymentSchema
    total_price: FloatDecimal
    rest: FloatDecimal
