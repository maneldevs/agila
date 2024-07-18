from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query

from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand, UserUpdateCommand
from app.auth.persistence.entities import UserEntity
from app.core.database import get_db
from app.core.exceptions import EntityAlreadyExistsError, EntityForeignKeyError
from app.core.models import PageParams
from app.core.paginator import Paginator


class UserRepository:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, command: UserCreateCommand) -> User:
        try:
            user_entity: UserEntity = UserEntity(
                username=command.username, password=command.password, email=command.email, role_id=command.role_id
            )
            self.db.add(user_entity)
            self.db.commit()
            self.db.refresh(user_entity)
            return user_entity.to_user()
        except IntegrityError:
            raise EntityAlreadyExistsError()

    def fetch_all(self) -> list[User]:
        query: Query = self.db.query(UserEntity)
        user_entities: list[UserEntity] = query.all()
        return [u.to_user() for u in user_entities]

    def fetch_all_paginated(self, page_params: PageParams) -> list[User]:
        query: Query = self.db.query(UserEntity)
        query = Paginator(UserEntity).paginate_query(query=query, page_params=page_params)
        user_entities: list[UserEntity] = query.all()
        return [u.to_user() for u in user_entities]

    def count_all(self) -> int:
        return self.db.query(UserEntity).count()

    def fetch_user_by_username(self, username: str) -> User:
        user: User = None
        user_entity: UserEntity = self.db.query(UserEntity).filter(UserEntity.username == username).first()
        if user_entity is not None:
            user = user_entity.to_user()
        return user

    def update(self, id: str, command: UserUpdateCommand) -> User:
        user: User = None
        try:
            user_entity: UserEntity = self.db.query(UserEntity).filter(UserEntity.id == id).first()
            if user_entity is not None:
                command_dict: dict = command.model_dump(exclude_unset=True)
                for key, value in command_dict.items():
                    setattr(user_entity, key, value)
                self.db.commit()
                self.db.refresh(user_entity)
                user = user_entity.to_user()
        except IntegrityError:
            raise EntityAlreadyExistsError()
        return user

    def delete(self, id: str) -> None:
        user: User = None
        try:
            user_entity: UserEntity = self.db.query(UserEntity).filter(UserEntity.id == id).first()
            if user_entity is not None:
                user = user_entity.to_user()
                self.db.delete(user_entity)
                self.db.commit()
        except IntegrityError:
            raise EntityForeignKeyError()
        return user
