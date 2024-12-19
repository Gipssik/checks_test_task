import factory

from checks_test_task.models import Check
from checks_test_task.tests.factories.payment import PaymentFactory
from checks_test_task.tests.factories.user import UserFactory


class CheckFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Check
        sqlalchemy_session_persistence = "commit"

    total_price = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    rest = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    user = factory.SubFactory(UserFactory)
    payment = factory.SubFactory(PaymentFactory)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.products.append(product)
