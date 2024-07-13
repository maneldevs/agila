from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends

from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.persistence.entities import UserEntity
from app.core.database import get_db
from app.core.exceptions import EntityAlreadyExistsError


class UserRepository:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, command: UserCreateCommand) -> User:
        try:
            user_entity = UserEntity(username=command.username, password=command.password, email=command.email)
            self.db.add(user_entity)
            self.db.commit()
            self.db.refresh(user_entity)
            return user_entity.toUser()
        except IntegrityError:
            raise EntityAlreadyExistsError("User already exists")
