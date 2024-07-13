import uuid
from sqlalchemy import Boolean, Column, String
from app.auth.application.domain import User
from app.core.database import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    active = Column(Boolean, nullable=False, default=True)

    def toUser(self):
        return User(**self.__dict__)
