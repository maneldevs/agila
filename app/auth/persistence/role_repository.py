from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from sqlalchemy.orm import Session

from app.auth.application.domain import Role
from app.auth.application.models import RoleCreateCommand
from app.auth.persistence.entities import RoleEntity
from app.core.database import get_db
from app.core.exceptions import EntityAlreadyExistsError


class RoleRepository:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, command: RoleCreateCommand) -> Role:
        try:
            role_entity: RoleEntity = RoleEntity(rolename=command.rolename)
            self.db.add(role_entity)
            self.db.commit()
            self.db.refresh(role_entity)
            return role_entity.to_role()
        except IntegrityError:
            raise EntityAlreadyExistsError()
