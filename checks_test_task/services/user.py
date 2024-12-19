from checks_test_task.conf.constants import ErrorMessages
from checks_test_task.exceptions import AlreadyExistsException
from checks_test_task.models import User
from checks_test_task.schemas.user import UserCreateSchema
from checks_test_task.services.base import BaseService
from checks_test_task.utils.password import get_password_hash


class UserService(BaseService[User]):
    MODEL = User

    async def get_user_by_email(self, email: str) -> User | None:
        """Fetch one user by email"""

        return await self.fetch_one(filters=(self.MODEL.email == email,))

    async def create_user(self, user_data: UserCreateSchema):
        """Create a new user"""

        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise AlreadyExistsException(ErrorMessages.USER_ALREADY_EXISTS)

        user_data.password = get_password_hash(user_data.password)

        user = User(**user_data.dict())
        return await self.insert_obj(user)
