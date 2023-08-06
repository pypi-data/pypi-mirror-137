from api import task, user
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(task.router, prefix="/tasks")
api_router.include_router(user.router, prefix="/users")
