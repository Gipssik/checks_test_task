from checks_test_task.tests.factories.check import CheckFactory
from checks_test_task.tests.factories.payment import PaymentFactory
from checks_test_task.tests.factories.product import ProductFactory
from checks_test_task.tests.factories.user import UserFactory

FACTORIES = [
    UserFactory,
    PaymentFactory,
    ProductFactory,
    CheckFactory,
]
