from fastapi import FastAPI

from .api.routes import user_router
from .config import settings

app = FastAPI(debug=settings.DEBUG)
app.include_router(user_router)
