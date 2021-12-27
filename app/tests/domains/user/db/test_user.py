import pytest
from sqlalchemy.orm import Session

from app.common.errors import RequestValidationError
from app.domains.user.db import (
    create_db_user,
    update_db_user,
    validate_user_create,
    validate_user_update,
)
from app.domains.user.logic import verify_password
from app.domains.user.models import UserCreate, UserUpdate
from app.tests.utils.common import random_lower_string, random_string
from app.tests.utils.domains.user import create_random_user


def test_create_user(db: Session) -> None:
    user = UserCreate(
        username=random_lower_string(),
        password=random_string(),
        is_active=False,
        is_superuser=False,
    )
    user_db = create_db_user(db, user)

    assert user_db.username == user.username
    assert verify_password(user.password, user_db.hashed_password)
    assert user.is_active == user_db.is_active
    assert user.is_superuser == user_db.is_superuser
    assert isinstance(user_db.id, int)


def test_update_user(db: Session) -> None:
    user_db = create_random_user(db)

    user = UserUpdate(
        username=random_lower_string(),
        password=random_string(),
        is_superuser=True,
        is_active=False,
    )

    user_db = update_db_user(db, user_db, user)
    assert user_db.username == user.username
    assert user_db.is_superuser == user.is_superuser
    assert user_db.is_active == user.is_active
    assert verify_password(user.password, user_db.hashed_password)


def test_validate_user_create_fails(db: Session) -> None:
    user_db = create_random_user(db)

    user = UserCreate(
        username=user_db.username,
        password=random_string(),
    )

    with pytest.raises(RequestValidationError):
        validate_user_create(db, user)


def test_validate_user_create_passes(db: Session) -> None:
    user_db = create_random_user(db)

    user = UserCreate(
        username=user_db.username + random_lower_string(4),
        password=random_string(),
    )

    validate_user_create(db, user)


def test_validate_user_update_fails(db: Session) -> None:
    user_db_1 = create_random_user(db)

    user_db_2 = create_random_user(db)

    user_2 = UserUpdate(
        username=user_db_1.username,
        password=random_string(),
    )

    with pytest.raises(RequestValidationError):
        validate_user_update(db, user_db_2, user_2)


def test_validate_user_update_passes(db: Session) -> None:
    user_db = create_random_user(db)

    user = UserUpdate(
        username=user_db.username + random_lower_string(4),
        password=random_string(),
    )

    validate_user_create(db, user)
