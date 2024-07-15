from typing import Optional
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"


class UserResponse(BaseModel):
    id: str
    username: str


class UserDetailResponse(UserResponse):
    email: str
    active: bool
    role: str
