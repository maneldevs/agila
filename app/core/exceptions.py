class BaseError(Exception):
    def __init__(self, message: str, status_code: int, *args, **kwargs) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(*args, **kwargs)


class EntityAlreadyExistsError(BaseError):
    def __init__(self, message: str = "Entity already exists", *args, **kwargs) -> None:
        super().__init__(message=message, status_code=400, *args, **kwargs)


class EntityNotFoundError(BaseError):
    def __init__(self, message: str = "Entity not found", *args, **kwargs) -> None:
        super().__init__(message, status_code=404, *args, **kwargs)


class CredentialsError(BaseError):
    def __init__(self, message: str = "Incorrect username or password", *args, **kwargs) -> None:
        super().__init__(message, status_code=401, *args, **kwargs)


class TokenInvalidError(BaseError):
    def __init__(self, message: str = "Token invalid", *args, **kwargs) -> None:
        super().__init__(message, status_code=401, *args, **kwargs)


class ForbiddenError(BaseError):
    def __init__(self, message: str = "Forbidden", *args, **kwargs) -> None:
        super().__init__(message, status_code=403, *args, **kwargs)
