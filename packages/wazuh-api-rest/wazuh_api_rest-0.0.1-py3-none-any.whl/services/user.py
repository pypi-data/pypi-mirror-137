import jq
import pkg_resources
from services import open_file

USERS_PATH = pkg_resources.resource_filename("resources", "users.json")


def find_all() -> [dict]:
    """Return all """
    return open_file(USERS_PATH)


def find_by_id(id: int) -> dict:
    """Find user by id"""
    tasks = open_file(USERS_PATH)

    tasks = jq.compile(f".[] | select(.id == {id})").input(tasks).first()

    return tasks
