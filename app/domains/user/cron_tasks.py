from dramatiq import actor
from periodiq import cron

from app.domains.user.tasks import simple_task


@actor(periodic=cron("* * * * *"))
def cron_task() -> None:
    simple_task.send("task done", 5)
    print("cron done")  # noqa
