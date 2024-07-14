from typing import Annotated

from fastapi import Depends

from app.auth.application import utils
from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.persistence.user_repository import UserRepository
from app.core.models import PageParams


class UserService:
    def __init__(self, user_repository: Annotated[UserRepository, Depends()]) -> None:
        self.user_repository = user_repository

    def create(self, command: UserCreateCommand) -> User:
        password_hashed = utils.generate_password_hash(command.password)
        command.password = password_hashed
        user = self.user_repository.create(command=command)
        return user

    def read_all(self) -> list[User]:
        return self.user_repository.fetch_all()

    def read_all_paginated(self, page_params: PageParams) -> list[User]:
        return self.user_repository.fetch_all_paginated(page_params)

    def count_all(self) -> int:
        return self.user_repository.count_all()
