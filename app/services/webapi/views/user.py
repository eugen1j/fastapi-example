import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from app.common.errors import ErrorMessage
from app.domains.user.db import create_db_user, update_db_user
from app.domains.user.models import UserCreate, UserDb, UserUpdate, UserView
from app.services.webapi.deps import get_db, get_model, remove_model

router = APIRouter()


@router.post("/", response_model=UserView)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> UserDb:
    return create_db_user(db, user)


@router.patch(
    "/{pk}/",
    response_model=UserView,
    responses={HTTP_404_NOT_FOUND: {"model": ErrorMessage}},
)
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    user_db: UserDb = Depends(get_model(UserDb)),
) -> UserDb:
    return update_db_user(db, user_db, user)


@router.get(
    "/{pk}/",
    response_model=UserView,
    responses={HTTP_404_NOT_FOUND: {"model": ErrorMessage}},
)
def read_user(user: UserDb = Depends(get_model(UserDb))) -> UserDb:
    return user


@router.delete(
    "/{pk}/",
    responses={HTTP_404_NOT_FOUND: {"model": ErrorMessage}},
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Depends(remove_model(UserDb))],
)
def delete_user() -> Response:
    return Response(status_code=HTTP_204_NO_CONTENT)
