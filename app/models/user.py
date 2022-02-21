import string
from typing import Optional

from pydantic import constr, validator, EmailStr

from app.models.core import CoreModel, IDModelMixin, DateTimeModelMixin


def validate_username(username: str):
    allowed = string.ascii_letters + string.digits + '_' + '-'
    assert all(
        c in allowed for c in username), f"Username {username} contains invalid characters"
    assert len(username) >= 3, f"Username {username} is too short"
    return username


class UserBase(CoreModel):
    username: Optional[str]
    email: Optional[EmailStr]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: constr(min_length=7, max_length=100)

    @validator('username', pre=True)
    def username_is_valid(cls, v):
        return validate_username(v)


class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]

    @validator('username', pre=True)
    def username_is_valid(cls, v):
        return validate_username(v)


class UserPasswordUpdate(CoreModel):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, UserBase):
    password: constr(min_length=7, max_length=100)
    salt: str

    pass


class UserPublic(IDModelMixin, UserBase):
    pass
