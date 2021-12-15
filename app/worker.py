# Import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.common.dramatiq import DbSessionMiddleware
from app.settings import main  # noqa

main.broker.add_middleware(
    DbSessionMiddleware(
        engine=create_engine(main.settings.POSTGRES_DSN, pool_pre_ping=True)
    )
)


# Import tasks

from app.domains.user.cron_tasks import *  # noqa
from app.domains.user.tasks import *  # noqa
