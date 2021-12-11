from sqlalchemy import Boolean, String
from sqlmodel import Field

from app.common.db import Column, SQLModel, TimestampedMixin
from app.common.pydantic import AllOptional, BaseModel


class UserDb(SQLModel, TimestampedMixin, table=True):
    __tablename__ = "user"

    username: str = Field(
        sa_column=Column(String, unique=True),
        description="Login field",
    )
    hashed_password: str = Field(
        sa_column=Column(String),
    )
    is_active: bool = Field(
        sa_column=Column(Boolean, default=True),
    )
    is_superuser: bool = Field(
        sa_column=Column(Boolean, default=False),
        description="Some super powers",
    )


class UserBase(BaseModel):
    username: str
    is_active: bool = True
    is_superuser: bool = False


class UserView(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate, metaclass=AllOptional):
    pass
