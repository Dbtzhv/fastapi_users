from typing import Optional
import re

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int


class UserRegister(BaseModel):
    email: str
    password: str = Field(None, min_length=8)
    confirm_password: str = Field(None, min_length=8)
    full_name: Optional[str] = None
    weight: Optional[float] = None

    @field_validator("full_name")
    @classmethod
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value
