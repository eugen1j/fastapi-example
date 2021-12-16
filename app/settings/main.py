import os

import dramatiq
import sentry_sdk
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.brokers.stub import StubBroker
from dramatiq.middleware import AgeLimit, Callbacks, Prometheus, Retries, TimeLimit
from periodiq import PeriodiqMiddleware
from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.patches.main import patch

patch()


class Settings(BaseSettings):
    DOMAIN: str = "localhost"

    PROJECT_NAME: str = "App"
    SECRET_KEY: str = "123456"

    SENTRY_DSN: str = ""
    POSTGRES_DSN: str = "postgresql://postgres:password@postgres:5432/postgres"
    AMQP_BROKER: str = "amqp://guest:guest@rabbitmq:5672"

    SQLALCHEMY_ENGINE_POOL_SIZE: int = 20
    SQLALCHEMY_ENGINE_MAX_OVERFLOW: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

if os.getenv("UNIT_TESTS", None) is None:
    broker = RabbitmqBroker(
        url=settings.AMQP_BROKER,
        middleware=[
            Prometheus(),
            AgeLimit(),
            TimeLimit(),
            Callbacks(),
            Retries(),
            PeriodiqMiddleware(),
        ],
    )
else:
    broker = StubBroker()
    broker.emit_after("process_boot")

dramatiq.set_broker(broker)
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

engine = create_engine(
    settings.POSTGRES_DSN,
    pool_pre_ping=True,
    pool_size=settings.SQLALCHEMY_ENGINE_POOL_SIZE,
    max_overflow=settings.SQLALCHEMY_ENGINE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(bind=engine)
