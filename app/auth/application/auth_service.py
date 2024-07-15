from datetime import timedelta
from typing import Annotated

from fastapi import Depends

from app.auth.application import utils
from app.auth.application.domain import User
from app.auth.persistence.user_repository import UserRepository
from app.core.settings import settings
from app.core.exceptions import CredentialsError


class AuthService:

    def __init__(self, userRepository: Annotated[UserRepository, Depends()]) -> None:
        self.userRepository = userRepository

    def authenticate(self, username: str, password: str) -> str:
        self.__verify_credentials(username, password)
        return self.__generate_access_token(username)

    def __verify_credentials(self, username: str | None, password: str) -> bool:
        user: User = self.userRepository.fetch_user_by_username(username)
        if not user or not utils.verify_password(password, user.password):
            raise CredentialsError()

    def __generate_access_token(self, username: str) -> str:
        data = {"sub": username}
        expiration_min = timedelta(minutes=settings.agila_access_token_expire_minutes)
        token = utils.create_access_token(data, settings.agila_secret_key, settings.agila_algorithm, expiration_min)
        return token
