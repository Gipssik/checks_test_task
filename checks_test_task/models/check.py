from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

from .base import BaseModel


class Check(BaseModel):
    __tablename__ = "checks"

    total_price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    rest = Column(DECIMAL(precision=10, scale=2), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="checks")
    payment = relationship("Payment", uselist=False, back_populates="check", lazy="joined")
    products = relationship("Product", back_populates="check", lazy="joined", order_by="Product.id")
