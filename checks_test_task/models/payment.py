from sqlalchemy import Column, Enum, DECIMAL, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel
from ..conf.constants import PaymentType


class Payment(BaseModel):
    __tablename__ = "payments"

    payment_type = Column(Enum(PaymentType), nullable=False)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)

    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)

    check = relationship("Check", back_populates="payment")
