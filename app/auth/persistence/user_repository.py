from sqlalchemy.orm import Session
from fastapi import Depends

from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.persistence.entities import UserEntity
from app.database import get_db


class UserRepository:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, command: UserCreateCommand) -> User:
        user_entity = UserEntity(username=command.username, password=command.password, email=command.email)
        self.db.add(user_entity)
        self.db.commit()
        self.db.refresh(user_entity)
        return user_entity.toUser()
