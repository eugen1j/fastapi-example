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
app.add_middleware(DBSessionMiddleware, custom_engine=main.engine)
app.include_router(url.api_router)
