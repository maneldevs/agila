from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.controller import auth_router, user_router
from app.core.exceptions import EntityAlreadyExistsError

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)


@app.get("/health")
async def read_root() -> dict:
    return {"status": "ok"}


@app.exception_handler(EntityAlreadyExistsError)
async def entity_alreasy_exists_handler(request: Request, exc: EntityAlreadyExistsError):
    return JSONResponse(status_code=400, content={'message': exc.message, 'status': 400})
