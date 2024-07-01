from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: bool = True
    full_name: Optional[str] = None
    weight: Optional[float] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str
    is_superuser: bool = False


class UserUpdate(UserBase):
    is_superuser: bool = False


class UserUpdatePassword(BaseModel):
    password: str
    new_password: str


class UserOut(UserBase):
    id: int = Field(description="Identification number")
    model_config = ConfigDict(
        from_attributes=True,  # orm_mode in v1
        json_schema_extra={
            "example": {
                "email": "denibatyzhev@gmail.com",
                "is_active": True,
                "full_name": "Deni Batyzhov",
                "id": 1,
            }
        },
    )
