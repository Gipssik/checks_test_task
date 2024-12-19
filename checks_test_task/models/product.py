from sqlalchemy import String, Column, DECIMAL, Integer, ForeignKey
from sqlalchemy.orm import relationship

from checks_test_task.models import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String(128), nullable=False)
    description = Column(String(512), nullable=True)
    price_per_unit = Column(DECIMAL(precision=10, scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(precision=10, scale=2), nullable=False)

    check_id = Column(Integer, ForeignKey("checks.id"), nullable=False)

    check = relationship("Check", back_populates="products")
