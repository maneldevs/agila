from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import BaseError


async def base_handler(request: Request, exc: BaseError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message, "status": exc.status_code})
