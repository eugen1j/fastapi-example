from typing import Any, Optional

import sqlalchemy as sa
import sqlmodel as sm
from humps import camelize
from sqlalchemy import Integer
from sqlmodel import Field


class Column(sa.Column):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("nullable", False)
        super().__init__(*args, **kwargs)


class SQLModel(sm.SQLModel, table=False):
    id: Optional[int] = Field(sa_column=Column(Integer, primary_key=True))

    class Config:
        alias_generator = camelize
