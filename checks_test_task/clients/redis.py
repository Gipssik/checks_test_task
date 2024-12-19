from redis.asyncio import Redis

from checks_test_task.conf.settings import settings, Env
from checks_test_task.exceptions import SetupException
from checks_test_task.tests.redis_mock import AsyncRedisMock


class RedisClient:
    def __init__(self):
        self._client: Redis | None = None

    def __getattr__(self, name: str) -> Redis:
        # check if the attribute is in the class dictionary
        # if it is, return it
        # otherwise - call the client attribute
        # use example: redis_client.get("key") instead of redis_client.client.get("key")
        return self.__dict__[name] if name in self.__dict__ else getattr(self.client, name)

    @property
    def client(self) -> Redis:
        if not self._client:
            raise SetupException("Redis client not configured")
        return self._client

    async def configure(self) -> None:
        if settings.ENV == Env.TESTING:
            self._client = AsyncRedisMock({})
            return

        self._client = Redis(host=settings.REDIS_HOST, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB)

    async def close(self) -> None:
        await self._client.close()


redis_client = RedisClient()
