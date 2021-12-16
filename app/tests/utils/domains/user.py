from sqlalchemy.orm import Session

from app.domains.user.db import create_db_user
from app.domains.user.models import UserCreate, UserDb
from app.tests.utils.common import random_lower_string


def create_random_user(db: Session) -> UserDb:
    user = UserCreate(
        username=random_lower_string(),
        password=random_lower_string(),
    )
    return create_db_user(db, user)


def create_random_superuser(db: Session) -> UserDb:
    user = UserCreate(
        username=random_lower_string(),
        password=random_lower_string(),
        is_superuser=True,
    )
    return create_db_user(db, user)
