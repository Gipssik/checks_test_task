from httpx import AsyncClient, Response

from checks_test_task.models import User


class AuthenticatedTestClient(AsyncClient):
    def __init__(self, user: User, *args, **kwargs):
        super(AuthenticatedTestClient, self).__init__(*args, **kwargs)
        self.user = user

    async def request(self, *args, **kwargs) -> Response:
        headers = kwargs.get("headers") or {}
        headers["Authorization"] = "Bearer secure_token"
        kwargs["headers"] = headers
        return await super(AuthenticatedTestClient, self).request(*args, **kwargs)
