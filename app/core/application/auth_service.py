from datetime import timedelta
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.application import utils
from app.core.application.domain import User
from app.core.persistence.user_repository import UserRepository
from app.shared.settings import settings
from app.shared.exceptions import CredentialsError, ForbiddenError, TokenInvalidError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AuthService:

    def __init__(self, userRepository: Annotated[UserRepository, Depends()]):
        self.userRepository = userRepository

    def authenticate(self, username: str, password: str) -> str:
        self.__verify_credentials(username, password)
        return self.__generate_access_token(username)

    def get_principal(self, token: str) -> str:
        principal: User | None = None
        try:
            payload: dict = utils.decode_token(token, settings.agila_secret_key, settings.agila_algorithm)
            username: str | None = payload.get("sub")
            if username:
                principal = self.userRepository.fetch_user_by_username(username)
            if principal is None or not principal.active:
                raise TokenInvalidError
        except ExpiredSignatureError:
            raise TokenInvalidError("Token expired")
        except InvalidTokenError:
            raise TokenInvalidError
        return principal

    def __verify_credentials(self, username: str | None, password: str) -> bool:
        user: User = self.userRepository.fetch_user_by_username(username)
        if not user or not utils.verify_password(password, user.password):
            raise CredentialsError()

    def __generate_access_token(self, username: str) -> str:
        data = {"sub": username}
        exp_min = timedelta(minutes=settings.agila_access_token_expire_minutes)
        token = utils.create_access_token(data, settings.agila_secret_key, settings.agila_algorithm, exp_min)
        return token


def get_principal(authService: Annotated[AuthService, Depends()], token: str | None = Depends(oauth2_scheme)) -> str:
    return authService.get_principal(token)


def get_principal_from_cookie(request: Request, authService: Annotated[AuthService, Depends()]) -> str:
    token = request.cookies["token"]
    return authService.get_principal(token)


class Authenticator:
    def __init__(self, allowed_roles: list[str] = []):
        self.allowed_roles = allowed_roles

    def __call__(self, principal: Annotated[User, Depends(get_principal)]) -> User:
        if self.allowed_roles and (not principal.role or principal.role.rolename not in self.allowed_roles):
            raise ForbiddenError
        return principal


class AuthenticatorCookie:
    def __init__(self, allowed_roles: list[str] = []):
        self.allowed_roles = allowed_roles

    def __call__(self, principal: Annotated[User, Depends(get_principal_from_cookie)]) -> User:
        if self.allowed_roles and (not principal.role or principal.role.rolename not in self.allowed_roles):
            raise ForbiddenError
        return principal
