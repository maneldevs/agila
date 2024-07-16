from typing import Annotated

from fastapi import Depends

from app.auth.application.domain import Role
from app.auth.application.models import RoleCreateCommand
from app.auth.persistence.role_repository import RoleRepository
from app.core.exceptions import EntityAlreadyExistsError


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
