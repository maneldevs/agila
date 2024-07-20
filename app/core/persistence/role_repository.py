from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.core.application.domain import Role
from app.core.application.models import RoleCreateCommand, RoleUpdateCommand
from app.core.persistence.entities import RoleEntity
from app.shared.database import get_db
from app.shared.exceptions import EntityAlreadyExistsError, EntityForeignKeyError


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

    def update(self, id: str, command: RoleUpdateCommand) -> Role:
        role: Role = None
        try:
            role_entity: RoleEntity = self.db.query(RoleEntity).filter(RoleEntity.id == id).first()
            if role_entity is not None:
                command_dict: dict = command.model_dump(exclude_unset=True)
                for key, value in command_dict.items():
                    setattr(role_entity, key, value)
                self.db.commit()
                self.db.refresh(role_entity)
                role = role_entity.to_role()
        except IntegrityError:
            raise EntityAlreadyExistsError()
        return role

    def delete(self, id: str) -> None:
        role: Role = None
        try:
            role_entity: RoleEntity = self.db.query(RoleEntity).filter(RoleEntity.id == id).first()
            if role_entity is not None:
                role = role_entity.to_role()
                self.db.delete(role_entity)
                self.db.commit()
        except IntegrityError:
            raise EntityForeignKeyError()
        return role
