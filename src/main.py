from fastapi import FastAPI

from .api.routes import auth_router, board_router, priority_router, status_router, task_router, user_router
from .config import settings

app = FastAPI(debug=settings.DEBUG)
app.include_router(auth_router)
app.include_router(board_router)
app.include_router(priority_router)
app.include_router(status_router)
app.include_router(task_router)
app.include_router(user_router)
