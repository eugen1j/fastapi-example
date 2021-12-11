import time

from dramatiq import actor


@actor()
def simple_task(msg: str, delay: int = 10) -> None:
    time.sleep(delay)
    print(msg)  # noqa
