from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["Admin Web"])
templates = Jinja2Templates(directory="src/resources/templates")


@router.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@router.get("/home", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={})
