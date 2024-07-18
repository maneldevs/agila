from typing import Annotated
from fastapi import APIRouter, Depends, status
from app.core.application.auth_service import Authenticator
from app.core.application.domain import Role, User
from app.core.application.models import RoleCreateCommand, RoleUpdateCommand
from app.core.application.role_service import RoleService
from app.core.controller.responses import RoleResponse


router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create(
    command: RoleCreateCommand,
    service: Annotated[RoleService, Depends()],
    principal: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    role: Role = service.create(command)
    return role


@router.get("/index", response_model=list[RoleResponse])
async def read_all(
    service: Annotated[RoleService, Depends()],
    _: Annotated[User, Depends(Authenticator())],
):
    roles: list[Role] = service.read_all()
    return roles


@router.get("/{id}", response_model=RoleResponse)
async def read_one_by_id(
    id: str, service: Annotated[RoleService, Depends()], _: Annotated[User, Depends(Authenticator())]
):
    role: Role = service.read_role_by_id(id)
    return role


@router.put("/{id}", response_model=RoleResponse)
async def update(
    id: str,
    command: RoleUpdateCommand,
    service: Annotated[RoleService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    role: Role = service.update(id, command)
    return role


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: str,
    service: Annotated[RoleService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
):
    service.delete(id)
