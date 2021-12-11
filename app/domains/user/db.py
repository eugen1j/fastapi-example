from typing import List

from fastapi import Path
from sqlalchemy.orm import Session

from app.common.pydantic import BaseModel
from app.domains.user.logic import get_password_hash
from app.domains.user.models import UserCreate, UserDb, UserUpdate


class PagePagination(BaseModel):
    page: int = Path(0)
    page_size: int = Path(100, lt=1000)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


def get_user_list(db: Session, pagination: PagePagination) -> List[UserDb]:
    return db.query(UserDb).offset(pagination.offset).limit(pagination.limit).all()


def create_db_user(
    db: Session,
    user: UserCreate,
) -> UserDb:
    data = user.dict()
    password = data.pop("password")
    user_db = UserDb(**data)
    user_db.hashed_password = get_password_hash(password)
    db.add(user_db)
    return user_db


def update_db_user(
    db: Session,
    db_model: UserDb,
    model: UserUpdate,
) -> UserDb:
    data = model.dict(exclude_unset=True)
    if "password" in data:
        password = data.pop("password")
        db_model.hashed_password = get_password_hash(password)

    for key, value in data.values():
        setattr(db_model, key, value)

    db.add(db_model)
    return db_model
