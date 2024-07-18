from fastapi import FastAPI

from app.core.controller import auth_router, role_router, user_router
import app.shared.exception_handlers as handlers
from app.shared.exceptions import BaseError

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(role_router.router)
app.add_exception_handler(BaseError, handlers.base_handler)


@app.get("/health")
async def read_root() -> dict:
    return {"status": "ok"}
