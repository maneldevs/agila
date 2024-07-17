from typing import Annotated

from fastapi import Depends

from app.auth.application.domain import Role
from app.auth.application.models import RoleCreateCommand
from app.auth.persistence.role_repository import RoleRepository
from app.core.exceptions import EntityAlreadyExistsError, EntityNotFoundError


class RoleService:

    def __init__(self, role_repository: Annotated[RoleRepository, Depends()]) -> None:
        self.role_repository = role_repository

    def create(self, command: RoleCreateCommand) -> Role:
        try:
            role: Role | None = self.role_repository.create(command=command)
        except EntityAlreadyExistsError as exc:
            exc.message = "Role already exists"
            raise exc
        return role

    def read_all(self) -> list[Role]:
        return self.role_repository.fetch_all()

    def read_role_by_id(self, id: str) -> Role:
        role = self.role_repository.fetch_role_by_id(id)
        if role is None:
            raise EntityNotFoundError("Role not found")
        return role

    def update(self, id: str, command: RoleCreateCommand) -> Role:
        try:
            role = self.role_repository.update(id, command)
            if role is None:
                raise EntityNotFoundError("Role not found")
        except EntityAlreadyExistsError as exc:
            exc.message = "Role already exists"
            raise exc
        return role
