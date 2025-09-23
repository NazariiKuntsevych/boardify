from fastapi import FastAPI

from .api.routes import auth_router, board_router, user_router
from .config import settings

app = FastAPI(debug=settings.DEBUG)
app.include_router(auth_router)
app.include_router(board_router)
app.include_router(user_router)
