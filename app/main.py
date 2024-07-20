from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.controller import admin_router, auth_router, role_router, user_router
import app.shared.exception_handlers as handlers
import app.shared.exception_handlers_admin as handlers_admin
from app.shared.exceptions import BaseError

# API -> http://localhost/...

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(role_router.router)
app.add_exception_handler(BaseError, handlers.base_handler)


@app.get("/health")
async def read_root() -> dict:
    return {"status": "ok"}


# ADMIN WEB ->   # http://localhost/admin/...

admin = FastAPI()
app.mount("/static", StaticFiles(directory="resources/static"), name="static")
app.mount("/admin", admin)
admin.include_router(admin_router.router)
admin.add_exception_handler(BaseError, handlers_admin.base_handler)
