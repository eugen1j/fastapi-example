from fastapi import Path
from sqlalchemy.orm import Session

from app.common.errors import RequestValidationError
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
    user_db: UserDb,
    user: UserUpdate,
) -> UserDb:
    data = user.dict(exclude_unset=True)
    if "password" in data:
        password = data.pop("password")
        user_db.hashed_password = get_password_hash(password)

    for key, value in data.items():
        setattr(user_db, key, value)

    db.add(user_db)
    return user_db


def validate_user_create(
    db: Session,
    user: UserCreate,
) -> None:
    if db.query(UserDb).filter(UserDb.username == user.username).first():
        raise RequestValidationError(
            "body.username",
            f"Username '{user.username}' is already taken",
        )


def validate_user_update(
    db: Session,
    user_db: UserDb,
    user: UserUpdate,
) -> None:
    if (
        user.username
        and db.query(UserDb)
        .filter(UserDb.username == user.username, UserDb.id != user_db.id)
        .first()
    ):
        raise RequestValidationError(
            "body.username",
            f"Username '{user.username}' is already taken",
        )
