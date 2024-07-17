from pydantic import BaseModel, EmailStr


class RoleCommand(BaseModel):
    rolename: str


class RoleCreateCommand(RoleCommand):
    pass


class RoleUpdateCommand(RoleCommand):
    pass


class UserCommand(BaseModel):
    username: str
    email: EmailStr
    role_id: str | None = None


class UserCreateCommand(UserCommand):
    password: str


class UserUpdateCommand(UserCommand):
    pass
