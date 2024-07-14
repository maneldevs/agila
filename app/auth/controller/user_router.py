from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.application.user_service import UserService
from app.auth.controller.responses import UserDetailResponse, UserResponse
from app.core.models import PageParams, PageResponse

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserDetailResponse)
async def create(command: UserCreateCommand, service: Annotated[UserService, Depends()]):
    user: User = service.create(command)
    return user


@router.get("/", response_model=PageResponse[UserDetailResponse])
async def read_all_paginated(page_params: Annotated[PageParams, Depends()], service: Annotated[UserService, Depends()]):
    total: int = service.count_all()
    users: list[User] = service.read_all_paginated(page_params)
    return PageResponse(page=page_params.page, size=page_params.size, total=total, content=users)


@router.get("/index/", response_model=list[UserResponse])
async def read_all(service: Annotated[UserService, Depends()]):
    users: list[User] = service.read_all()
    return users
