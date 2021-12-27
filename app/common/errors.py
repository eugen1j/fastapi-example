from fastapi import HTTPException

from app.common.pydantic import BaseModel


class ErrorMessage(BaseModel):
    detail: str


class RequestValidationError(HTTPException):
    def __init__(self, loc: str, msg: str, typ: str = "value_error") -> None:
        super().__init__(422, [{"loc": loc.split("."), "msg": msg, "type": typ}])
