from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, validator
from src.schemas.user import UserResponse

# Here are some shemas for validation of input information

class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=150)
    last_name: str = Field(min_length=3, max_length=150)
    email: EmailStr
    phone_number: str = Field(default=..., example="380973458623")
    birth_date: date
    additional_data: Optional[str] = Field(default=None, example="Additional information")

    @validator("phone_number")
    def validate_phone_number(cls, value):
        signs_valid = ['(', ')', '+', '-', ' ']
        temp_value = value
        for element in temp_value:
            if element in signs_valid:
                temp_value = temp_value.replace(element, '')
        if not temp_value.isdigit():
            raise ValueError("Phone number should contain only digits.")
        return value


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str 
    birth_date: datetime
    additional_data: Optional[str]
    created_at: datetime | None #for user
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True