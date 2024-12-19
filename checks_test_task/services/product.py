from checks_test_task.models import Product, Check
from checks_test_task.schemas.check import ProductBaseSchema
from checks_test_task.services.base import BaseService


class ProductService(BaseService[Product]):
    MODEL = Product

    async def create_products(
        self,
        products: list[ProductBaseSchema],
        check: Check,
        commit: bool = True,
    ) -> list[Product]:
        product_objs = []
        for product in products:
            product_obj = Product(
                name=product.name,
                description=product.description,
                price_per_unit=product.price_per_unit,
                quantity=product.quantity,
                total_price=product.price_per_unit * product.quantity,
                check=check,  # type: ignore
            )
            await self.insert_obj(product_obj, commit=False)
            product_objs.append(product_obj)

        if commit:
            await self.session.commit()
        return product_objs
