from starlette.requests import Request
from starlette.responses import JSONResponse


async def not_found_handler(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "No matching data found"},
    )
