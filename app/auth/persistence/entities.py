import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.auth.application.domain import Role, User
from app.core.database import Base


class RoleEntity(Base):
    __tablename__ = "roles"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    rolename = Column(String(50), nullable=False, unique=True)

    def to_role(self) -> Role:
        return Role(**self.__dict__)


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)
    role_id = Column(String(255), ForeignKey("roles.id"))

    role = relationship("RoleEntity")

    def to_user(self) -> User:
        user = User(**self.__dict__)
        if self.role:
            user.role = self.role.to_role()
        return user
