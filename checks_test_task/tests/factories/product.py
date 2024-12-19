import factory

from checks_test_task.models import Product


class ProductFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("pystr")
    description = factory.Faker("pystr")
    price_per_unit = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    quantity = factory.Faker("pydecimal", left_digits=1, right_digits=2)
    total_price = factory.LazyAttribute(lambda o: o.price_per_unit * o.quantity)
