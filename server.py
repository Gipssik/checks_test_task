import uvicorn

from checks_test_task.app import create_app
from checks_test_task.conf.settings import settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
        loop="uvloop",
    )
