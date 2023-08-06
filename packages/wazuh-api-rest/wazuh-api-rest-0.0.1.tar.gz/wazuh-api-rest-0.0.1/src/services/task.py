import jq
import pkg_resources

from services import open_file

TASKS_PATH = pkg_resources.resource_filename('resources', 'tasks.json')


def find_all() -> [dict]:
    """REturn all """
    return open_file(TASKS_PATH)


def find_by(completed: str = None, title: str = None) -> [dict]:
    """List all taks base on filters completed and title. In case no param passing list all."""

    if completed is None and title is None:
        raise ValueError("completed or title must be passed")

    tasks = open_file(TASKS_PATH)
    if completed is not None and title:
        result = jq.compile(f'.[] | select( .completed == {str(completed).lower()}) | select( .title | contains("{title}"))').input(
            tasks).all()
    if completed is None and title:
        result = jq.compile(f'.[] | select( .title | contains("{title}"))').input(tasks).all()
    if completed and title is None:
        result = jq.compile(f'.[] | select( .completed == {str(completed).lower()})').input(tasks).all()

    return result


def find_by_id(id: int) -> dict:
    """Find tasks by id"""

    tasks = open_file(TASKS_PATH)
    tasks = jq.compile(f".[] | select(.id == {id})").input(tasks).first()

    return tasks