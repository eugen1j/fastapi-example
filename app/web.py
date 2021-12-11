from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.services.webapi import url
from app.settings import main  # noqa

app = FastAPI(
    title=main.settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)
app.add_middleware(SentryAsgiMiddleware)
app.add_middleware(
    DBSessionMiddleware,
    db_url=main.settings.POSTGRES_DSN,
    commit_on_exit=True,
    engine_args={"pool_pre_ping": True},
)
app.include_router(url.api_router)
