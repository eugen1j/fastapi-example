from typing import Callable, Type, TypeVar

import fastapi_sqlalchemy
from fastapi import Depends, HTTPException, Path
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.common.db import SQLModel

T = TypeVar("T")

TDB = TypeVar("TDB", bound=SQLModel)


def get_db() -> Session:
    return fastapi_sqlalchemy.db.session


def get_model(
    DbModelType: Type[TDB],
    *,
    field_name: str = "id",
    path_name: str = "pk",
) -> Callable[[Session, str], TDB]:
    def wrapper(
        db: Session = Depends(get_db),
        field_value: str = Path(..., alias=path_name),
    ) -> TDB:
        try:
            return (
                db.query(DbModelType)
                .filter(getattr(DbModelType, field_name) == field_value)
                .one()
            )
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")

    return wrapper


def remove_model(
    DbModelType: Type[TDB],
    *,
    field_name: str = "id",
    path_name: str = "pk",
) -> Callable[[Session, str], None]:
    def wrapper(
        db: Session = Depends(get_db),
        field_value: str = Path(..., alias=path_name),
    ) -> None:
        try:
            model = (
                db.query(DbModelType)
                .filter(getattr(DbModelType, field_name) == field_value)
                .one()
            )
            db.delete(model)
            db.commit()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")

    return wrapper
