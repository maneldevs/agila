from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import EntityAlreadyExistsError


async def entity_already_exists_handler(request: Request, exc: EntityAlreadyExistsError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message, "status": exc.status_code})
