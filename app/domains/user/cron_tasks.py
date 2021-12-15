import random
import traceback

from dramatiq import actor
from periodiq import cron

from app.common.dramatiq import db
from app.domains.user.models import UserDb
from app.domains.user.tasks import simple_task


@actor(periodic=cron("* * * * *"))
def cron_task() -> None:
    print("cron done")
    try:
        with db.session.begin():
            user = UserDb(
                username=str(random.randint(100000, 1111111111)),
                hashedPassword="1344",
            )
            db.session.add(user)
    except Exception as e:
        print(e)
        traceback.format_exc()

    simple_task.send("task done", 5)
    print("cron done")  # noqa
