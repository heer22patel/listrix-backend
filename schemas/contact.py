import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

PHONE_PATTERN = re.compile(r"^[0-9+\-\s()]{7,20}$")


class ContactCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=50)
    message: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty.")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and not PHONE_PATTERN.match(v):
            raise ValueError("Phone number format looks invalid.")
        return v


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    message: Optional[str]

    model_config = {"from_attributes": True}
