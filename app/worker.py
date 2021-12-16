# Import settings

from app.common.dramatiq import DbSessionMiddleware
from app.settings import main  # noqa

main.broker.add_middleware(DbSessionMiddleware(engine=main.engine))

# Import tasks

from app.domains.user.cron_tasks import *  # noqa
from app.domains.user.tasks import *  # noqa
