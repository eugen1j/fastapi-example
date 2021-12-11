from fastapi import APIRouter

from app.services.webapi.views import user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
