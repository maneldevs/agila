from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.shared.exceptions import BaseError

templates = Jinja2Templates(directory="resources/templates")


def base_handler(request: Request, exc: BaseError):
    return templates.TemplateResponse(
        request=request, name="login.html", status_code=exc.status_code, context={"message": exc.message}
    )
