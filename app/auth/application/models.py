from pydantic import BaseModel, EmailStr


class RoleCreateCommand(BaseModel):
    rolename: str


class UserCommand(BaseModel):
    username: str
    email: EmailStr
    role_id: str | None = None


class UserCreateCommand(UserCommand):
    password: str


class UserUpdateCommand(UserCommand):
    pass
