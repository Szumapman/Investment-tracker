import re
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    model_validator,
    ConfigDict,
)

from src.config.constants import MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH

MIN_PASSSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 72  # The bcrypt algorithm only handles passwords up to 72 characters: https://pypi.org/project/bcrypt/
EXAMPLE_PASSWORD = "Password123!"


class Password(BaseModel):
    password: str = Field(
        min_length=MIN_PASSSWORD_LENGTH,
        max_length=MAX_PASSWORD_LENGTH,
        example="Password123!",
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
            rf"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{{{MIN_PASSSWORD_LENGTH},{MAX_PASSWORD_LENGTH}}}$",
            password,
        ):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character"
            )
        elif password == EXAMPLE_PASSWORD:
            raise ValueError("Password cannot be the example password")
        return password


class UserIn(BaseModel):
    username: str = Field(
        min_length=MIN_USERNAME_LENGTH,
        max_length=MAX_USERNAME_LENGTH,
        default="user name",
    )
    email: EmailStr = Field(max_length=150, default="user@example.com")
    password: Password


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


class ResetPassword(BaseModel):
    password: Password
    password2: Password

    @model_validator(mode="after")
    def check_passwords_match(self) -> "ResetPassword":
        if self.password != self.password2:
            raise ValueError("Passwords do not match")
        return self
