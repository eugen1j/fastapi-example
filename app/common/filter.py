"""
Module for Declarative filtering DbModels like Django's ListView + filter_backends.
"""
from typing import TypeVar

from sqlalchemy import Column
from sqlalchemy.orm import Query

from app.common.db import SQLModel
from app.common.strings import is_int

TDB = TypeVar("TDB", bound=SQLModel)
TDB2 = TypeVar("TDB2", bound=SQLModel)


class BaseFilter:
    def filter(self, query: Query) -> Query:
        pass


class Pagination:
    pass


def int_key_filter(
    query: Query,
    column: Column,
    value: str,
    separator: str = ",",
) -> Query:
    values = [int(x) for x in value.split(separator) if is_int(x)]
    return query.filter(column.in_(values))


def str_key_filter(
    query: Query,
    column: Column,
    value: str,
    separator: str = ",",
) -> Query:
    values = [x for x in value.split(separator)]
    return query.filter(column.in_(values))
