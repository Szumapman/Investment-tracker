from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.config.config import settings
from src.services.abstract import AbstractAuthService
from src.config.constants import API, AUTH, EMAIL_TOKEN_HOURS_TO_EXPIRE


class AuthService(AbstractAuthService):

    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API}{AUTH}/login")

    async def create_email_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            hours=EMAIL_TOKEN_HOURS_TO_EXPIRE
        )
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload.get("sub")
            return email
        except jwt.PyJWTError as e:
            print(e)  # TODO: log error
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid token for email verification",
            )


auth_service = AuthService()
