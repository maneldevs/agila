from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.application.models import UserCreateCommand
from app.auth.application.user_service import UserService
from app.auth.controller.responses import UserDetailResponse

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserDetailResponse)
async def register(command: UserCreateCommand, service: Annotated[UserService, Depends()]):
    user = service.create(command)
    return user
