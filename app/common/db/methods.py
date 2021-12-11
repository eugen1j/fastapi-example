from typing import TypeVar

from app.common.db import SQLModel

T = TypeVar("T", bound=SQLModel)
