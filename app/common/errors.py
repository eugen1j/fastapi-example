from app.common.pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str
