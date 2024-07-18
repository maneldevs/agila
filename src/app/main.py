from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.controller import auth_router, role_router, user_router
import app.shared.exception_handlers as handlers
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
app.mount("/static", StaticFiles(directory="src/resources/static"), name="static")
app.mount("/admin", admin)
templates = Jinja2Templates(directory="src/resources/templates")


@admin.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})
