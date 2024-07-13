from typing import Annotated

from fastapi import Depends

from app.auth.application import utils
from app.auth.application.domain import User
from app.auth.application.models import UserCreateCommand
from app.auth.persistence.user_repository import UserRepository


class UserService:
    def __init__(self, userRepository: Annotated[UserRepository, Depends()]) -> None:
        self.userRepository = userRepository

    def create(self, command: UserCreateCommand) -> User:
        password_hashed = utils.generate_password_hash(command.password)
        command.password = password_hashed
        user = self.userRepository.create(command=command)
        return user

    def readAll(self) -> list[User]:
        return self.userRepository.fetchAll()
