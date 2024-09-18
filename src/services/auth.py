from datetime import datetime, timedelta, timezone
import uuid

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.config.config import settings
from src.database.dependencies import get_cache
from src.database.models import User
from src.services.abstract import AbstractAuthService
from src.config.constants import API, AUTH, EMAIL_TOKEN_HOURS_TO_EXPIRE


class AuthService(AbstractAuthService):

    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    EXPIRE_IN_SECONDS = 900
    REFRESH_TOKEN_EXPIRE = 7  # days
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API}{AUTH}/login")

    def __init__(self, cache=get_cache()):
        self.cache = cache

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

    async def update_user_in_cache(self, user: User) -> None:
        await self.cache.set_to_cache(
            key=user.email, value=user, expire=self.EXPIRE_IN_SECONDS
        )

    async def create_access_token(
            self,
            data: dict,
            expires_delta: timedelta = timedelta(seconds=EXPIRE_IN_SECONDS),
    ) -> (str, str):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        session_id = str(uuid.uuid4())
        to_encode.update(
            {
                "iat": datetime.utcnow(),
                "exp": expire,
                "session_id": session_id,
                "scope": self.ACCESS_TOKEN,
            }
        )
        encode_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encode_access_token, session_id




auth_service = AuthService()
