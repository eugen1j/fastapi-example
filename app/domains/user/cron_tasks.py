import random

from dramatiq import actor
from periodiq import cron

from app.common.dramatiq import db
from app.domains.user.models import UserDb
from app.domains.user.tasks import simple_task


@actor(periodic=cron("* * * * *"))
def cron_task() -> None:
    with db.session.begin():
        user = UserDb(
            username=str(random.randint(100000, 1111111111)),
            hashed_password="1344",
        )
        db.session.add(user)

    simple_task.send("task done", 5)
    print("cron done")  # noqa
