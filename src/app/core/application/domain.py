from typing import Optional
from pydantic import BaseModel


class Role(BaseModel):
    id: str
    rolename: str


class User(BaseModel):
    id: str
    username: str
    password: str
    email: str
    active: bool
    role: Optional[Role] = None

    class Config:
        orm_mode = True
