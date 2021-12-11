from typing import Sequence, cast

import sqlalchemy as sa
import sqlmodel
from pydantic.fields import ModelField, Undefined
from sqlalchemy import ForeignKey
from sqlmodel.main import get_sqlachemy_type

from app.common.db import Column


def get_column_from_field(field: ModelField) -> sa.Column:  # noqa
    sa_column = getattr(field.field_info, "sa_column", Undefined)
    if isinstance(sa_column, sa.Column):
        return sa_column
    sa_type = get_sqlachemy_type(field)
    primary_key = getattr(field.field_info, "primary_key", False)
    nullable = not field.required
    index = getattr(field.field_info, "index", Undefined)
    if index is Undefined:
        # https://github.com/tiangolo/sqlmodel/pull/11/files
        index = False
    if hasattr(field.field_info, "nullable"):
        field_nullable = getattr(field.field_info, "nullable")  # noqa
        if field_nullable != Undefined:
            nullable = field_nullable
    args = []
    foreign_key = getattr(field.field_info, "foreign_key", None)
    if foreign_key:
        args.append(ForeignKey(foreign_key))
    kwargs = {
        "primary_key": primary_key,
        "nullable": nullable,
        "index": index,
    }
    sa_default = Undefined
    if field.field_info.default_factory:
        sa_default = field.field_info.default_factory
    elif field.field_info.default is not Undefined:
        sa_default = field.field_info.default
    if sa_default is not Undefined:
        kwargs["default"] = sa_default
    sa_column_args = getattr(field.field_info, "sa_column_args", Undefined)
    if sa_column_args is not Undefined:
        args.extend(list(cast(Sequence, sa_column_args)))
    sa_column_kwargs = getattr(field.field_info, "sa_column_kwargs", Undefined)
    if sa_column_kwargs is not Undefined:
        kwargs.update(cast(dict, sa_column_kwargs))
    # Custom Column class
    return Column(sa_type, *args, **kwargs)


def patch() -> None:
    sqlmodel.main.get_column_from_field = get_column_from_field
