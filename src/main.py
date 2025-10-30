from fastapi import FastAPI

from .api.exception_handelrs import not_found_handler
from .api.routes import user_router
from .config import settings
from .repositories import NotFound

app = FastAPI(debug=settings.DEBUG)
app.include_router(user_router)
app.add_exception_handler(NotFound, not_found_handler)
