from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base
from enum import Enum

class UserRole(Enum):
    SYSTEM_ADMIN = 1
    INDIVIDUAL_USER = 2

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    phoneNumber = Column(String, unique=True, nullable=False)
    passwordHash = Column(String, nullable=False)
    role = Column(Integer, default=UserRole.INDIVIDUAL_USER, nullable=False, index=True)
    isActive = Column(Boolean, default=True, nullable=False, index=True)

