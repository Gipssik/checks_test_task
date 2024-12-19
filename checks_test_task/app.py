from fastapi import FastAPI
from fastapi_pagination import add_pagination

from checks_test_task import __version__
from checks_test_task.api import users, checks
from checks_test_task.clients.redis import redis_client
from checks_test_task.conf.database import async_session, engine
from checks_test_task.conf.settings import Settings, settings
from checks_test_task.exception_handlers import init_exception_handlers
from checks_test_task.middlewares import init_middlewares
from checks_test_task.models.base import metadata


def init_routes(app: FastAPI) -> None:
    """Connect routes to app"""
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(checks.router, prefix="/checks", tags=["checks"])


def init_db():
    """Init database"""
    async_session.configure(bind=engine)
    metadata.bind = engine


def create_app(app_settings: Settings = settings):
    """Create app with including configurations"""
    init_db()
    app = FastAPI(
        title="Checks Test Task",
        version=__version__,
    )
    init_middlewares(app, app_settings)
    init_exception_handlers(app)
    init_routes(app)
    add_pagination(app)

    @app.on_event("startup")
    async def startup():
        await redis_client.configure()

    @app.on_event("shutdown")
    async def shutdown():
        await redis_client.close()

    return app
