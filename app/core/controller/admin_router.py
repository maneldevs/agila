from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from app.core.application.auth_service import AuthService, AuthenticatorCookie
from app.core.application.domain import User
from app.shared.exceptions import CredentialsError

router = APIRouter(prefix="", tags=["Admin Web"])
templates = Jinja2Templates(directory="resources/templates")


@router.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={})


@router.post("/login", response_class=HTMLResponse)
async def admin_login_perform(
    request: Request,
    command: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends()],
):
    response: HTMLResponse = None
    try:
        token: str = service.authenticate(command.username, command.password)
        response = templates.TemplateResponse(request=request, name="index.html", context={"message": None})
        response.set_cookie("token", f"{token}", httponly=True)
    except CredentialsError as exc:
        response = templates.TemplateResponse(
            request=request, name="login.html", status_code=exc.status_code, context={"message": exc.message}
        )
    return response


@router.get("/home", response_class=HTMLResponse)
async def admin_home(request: Request, _: Annotated[User, Depends(AuthenticatorCookie(allowed_roles=["admin"]))]):
    response = templates.TemplateResponse(request=request, name="home.html", context={})
    return response
