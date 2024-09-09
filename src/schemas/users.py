import re
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

from src.config.constants import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH

MIN_PASSSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 72  # The bcrypt algorithm only handles passwords up to 72 characters: https://pypi.org/project/bcrypt/


class UserIn(BaseModel):
    username: str = Field(
        min_length=MIN_USERNAME_LENGTH,
        max_length=MAX_USERNAME_LENGTH,
        default="user name",
    )
    email: EmailStr = Field(max_length=150, default="user@example.com")
    password: str = Field(
        min_length=MIN_PASSSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH
    )

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < MIN_PASSSWORD_LENGTH:
            raise ValueError(
                f"Password must be at least {MIN_PASSSWORD_LENGTH} characters long"
            )
        elif len(password) > MAX_PASSWORD_LENGTH:
            raise ValueError(
                f"Password must be at most {MAX_PASSWORD_LENGTH} characters long"
            )
        elif not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,100}$", password
        ):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
            )
        return password


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime | None
    is_confirmed: bool

    model_config = ConfigDict(from_attributes=True)


class UserInfo(BaseModel):
    user: UserOut
    detail: str
