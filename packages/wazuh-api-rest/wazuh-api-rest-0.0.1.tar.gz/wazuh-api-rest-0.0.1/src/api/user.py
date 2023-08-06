
import logging
from fastapi import APIRouter
from services.user import find_all, find_by_id

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_all() -> dict:
    """Get All"""
    users = find_all()
    return {"total_items": len(users), "data": users}


@router.get("/{user_id}")
def get_by_id(user_id: int) -> dict:
    """Get by User Id """
    return find_by_id(user_id)
