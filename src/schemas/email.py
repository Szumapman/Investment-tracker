from pydantic import BaseModel, EmailStr
from sqlalchemy import Enum

EMAIL_TYPE = Enum("confirm", "reset_password", name="email_type")

# class EmailTypeEnum(str, Enum):
#     confirm = "confirm"
#     reset_password = "reset_password"


class RequestEmail(BaseModel):
    email: EmailStr
    request_type: str = EMAIL_TYPE
