import factory

from checks_test_task.conf.constants import PaymentType
from checks_test_task.models import Payment


class PaymentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Payment
        sqlalchemy_session_persistence = "commit"

    payment_type = factory.Faker("enum", enum_cls=PaymentType)
    amount = factory.Faker("pydecimal", left_digits=2, right_digits=2)
