
import logging
from fastapi import APIRouter
from services.task import find_all, find_by_id, find_by

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_by(completed: bool = None, title: str = None) -> dict:
    """Get by Completed and/or Title"""
    if completed is None and title is None:
        tasks = find_all()
    else:
        tasks = find_by(completed=completed, title=title)

    return {"total_items": len(tasks), "data": tasks}


@router.get("/{id}")
def get_by_id(id: int) -> dict:
    """Get by task Id """

    result = find_by_id(id)
    return result
