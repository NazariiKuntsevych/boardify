from .board import repository as board_repository
from .priority import repository as priority_repository
from .status import repository as status_repository
from .task import repository as task_repository
from .user import repository as user_repository

__all__ = [
    "board_repository",
    "priority_repository",
    "status_repository",
    "task_repository",
    "user_repository",
]
