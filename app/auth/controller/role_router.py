from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.application.auth_service import Authenticator
from app.auth.application.domain import Role, User
from app.auth.application.models import RoleCreateCommand
from app.auth.application.role_service import RoleService
from app.auth.controller.responses import RoleResponse


router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("/", response_model=RoleResponse)
async def create(
    command: RoleCreateCommand,
    service: Annotated[RoleService, Depends()],
    _: Annotated[User, Depends(Authenticator(allowed_roles=["admin"]))],
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
