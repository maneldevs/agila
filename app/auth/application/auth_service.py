from typing import Annotated

from fastapi import Depends

from app.auth.persistence.user_repository import UserRepository


class AuthService:
    def __init__(self, userRepository: Annotated[UserRepository, Depends()]) -> None:
        self.userRepository = userRepository

    def authenticate(self) -> str:
        # TODO mmr verify user credentials
        # TODO mmr generate token
        token: str = "fake_token"
        return token
