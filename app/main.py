from fastapi import FastAPI

from app.auth.controller import auth_router, user_router
import app.core.exception_handlers as handlers
from app.core.exceptions import BaseError

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.add_exception_handler(BaseError, handlers.base_handler)


@app.get("/health")
async def read_root() -> dict:
    return {"status": "ok"}
