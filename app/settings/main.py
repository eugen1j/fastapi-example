import dramatiq
import sentry_sdk
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import AgeLimit, Callbacks, Prometheus, Retries, TimeLimit
from periodiq import PeriodiqMiddleware
from pydantic import BaseSettings

from app.patches.main import patch

patch()


class Settings(BaseSettings):
    DOMAIN: str = "localhost"

    PROJECT_NAME: str = "App"
    SECRET_KEY: str = "123456"

    SENTRY_DSN: str = ""
    POSTGRES_DSN: str = "postgresql://postgres:password@postgres:5432/postgres"
    AMQP_BROKER: str = "amqp://guest:guest@rabbitmq:5672"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
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
dramatiq.set_broker(broker)
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )