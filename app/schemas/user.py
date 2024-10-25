from app.models.user import UserRole
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from datetime import datetime


class ResetPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str

class UserPassword(BaseModel):
    passwordHash: str

class UserBase(BaseModel):
    email: EmailStr

class UserLogin(UserBase):
    password: str

class UserCreate(UserBase):
    username: constr(min_length=3, max_length=50) # type: ignore
    phoneNumber: str
    password: constr(min_length=8) # type: ignore
    password_confirm: constr(min_length=8) # type: ignore

    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator("password")
    def check_password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number.")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter.")
        return v

class UserCreateInDB(UserBase):
    username: str
    passwordHash: str
    phoneNumber: str
    role: UserRole = UserRole.INDIVIDUAL_USER

class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    isActive: Optional[bool] = True
    organizationId: Optional[int] = None


class User(UserBase):
    id: int
    username: str
    role: UserRole
    organizationId: Optional[int] = None
    isActive: bool
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
