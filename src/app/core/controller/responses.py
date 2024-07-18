from typing import Optional
from pydantic import BaseModel

from app.core.application.domain import Role


class TokenResponse(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"


class RoleResponse(BaseModel):
    id: str
    rolename: str


class UserResponse(BaseModel):
    id: str
    username: str


class UserDetailResponse(UserResponse):
    email: str
    active: bool
    role: Optional[Role] = None

    class Config:
        orm_mode = True
