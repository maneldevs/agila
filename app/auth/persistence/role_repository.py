from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query
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

    def fetch_role_by_id(self, id: str) -> Role:
        role: Role = None
        role_entity: RoleEntity = self.db.query(RoleEntity).filter(RoleEntity.id == id).first()
        if role_entity is not None:
            role = role_entity.to_role()
        return role

    def fetch_all(self) -> list[Role]:
        query: Query = self.db.query(RoleEntity)
        role_entities: list[RoleEntity] = query.all()
        return [r.to_role() for r in role_entities]