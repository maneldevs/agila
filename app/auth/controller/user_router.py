from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.auth.application.auth_service import Authenticator
from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand, UserUpdateCommand
from app.auth.application.user_service import UserService
from app.auth.controller.responses import UserDetailResponse, UserResponse
from app.core.models import PageParams, PageResponse

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserDetailResponse, status_code=status.HTTP_201_CREATED)
async def create(
    command: UserCreateCommand,
    service: Annotated[UserService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    user: User = service.create(command)
    return user


@router.get("/", response_model=PageResponse[UserDetailResponse])
async def read_all_paginated(
    page_params: Annotated[PageParams, Depends()],
    service: Annotated[UserService, Depends()],
    _: Annotated[User, Depends(Authenticator())],
):
    total: int = service.count_all()
    users: list[User] = service.read_all_paginated(page_params)
    return PageResponse(page=page_params.page, size=page_params.size, total=total, content=users)


@router.get("/index", response_model=list[UserResponse])
async def read_all(
    service: Annotated[UserService, Depends()],
    _: Annotated[User, Depends(Authenticator())],
):
    users: list[User] = service.read_all()
    return users


@router.get("/by_username/{username}", response_model=UserDetailResponse)
async def read_one_by_username(
    username: str, service: Annotated[UserService, Depends()], _: Annotated[User, Depends(Authenticator())]
):
    user: User = service.read_user_by_username(username)
    return user


@router.put("/{id}", response_model=UserDetailResponse)
async def update(
    id: str,
    command: UserUpdateCommand,
    service: Annotated[UserService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    user: User = service.update(id, command)
    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str,
    service: Annotated[UserService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    service.delete(id)
