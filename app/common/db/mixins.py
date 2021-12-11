from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field

from .main import Column
from .types import DateTime


class TimestampedMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            index=True,
        ),
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
            onupdate=datetime.utcnow,
            index=True,
        ),
    )
