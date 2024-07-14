from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, Query

from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.persistence.entities import UserEntity
from app.core.database import get_db
from app.core.exceptions import EntityAlreadyExistsError
from app.core.models import PageParams
from app.core.utils import paginate_query


class UserRepository:

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create(self, command: UserCreateCommand) -> User:
        try:
            user_entity: UserEntity = UserEntity(
                username=command.username, password=command.password, email=command.email
            )
            self.db.add(user_entity)
            self.db.commit()
            self.db.refresh(user_entity)
            return user_entity.to_user()
        except IntegrityError:
            raise EntityAlreadyExistsError("User already exists")

    def fetchAll(self, page_params: PageParams) -> list[User]:
        query: Query = self.db.query(UserEntity)
        query = paginate_query(query=query, page_params=page_params)
        user_entities: list[UserEntity] = query.all()
        return [u.to_user() for u in user_entities]

    def countAll(self) -> int:
        return self.db.query(UserEntity).count()
