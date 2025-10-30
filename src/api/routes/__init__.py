from .auth import router as auth_router
from .board import router as board_router
from .task import router as task_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "board_router",
    "task_router",
    "user_router",
]
