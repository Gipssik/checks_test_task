import datetime
from typing import Generic, TypeVar, Type, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from checks_test_task.models import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseService(Generic[ModelT]):
    MODEL: Type[ModelT] = Base

    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_one(self, filters: Sequence, options: Sequence = ()) -> ModelT | None:
        """Fetch one obj from database"""

        query = select(self.MODEL).filter(*filters).options(*options).limit(1)
        return await self.session.scalar(query)

    async def insert_obj(self, obj: Base, commit: bool = True) -> Base:
        """Insert new obj to DB"""

        now = datetime.datetime.now(tz=None)
        obj.created_at = now
        self.session.add(obj)
        if commit:
            await self.session.commit()
        return obj
