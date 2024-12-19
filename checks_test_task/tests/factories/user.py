import factory

from checks_test_task.models import User
from checks_test_task.utils.password import get_password_hash


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: get_password_hash("password"))
