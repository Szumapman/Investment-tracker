from datetime import datetime, timedelta, timezone
import uuid
import pickle

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

from src.config.config import settings
from src.repositories.abstract import AbstractUserRepo
from src.database.dependencies import get_cache, get_user_repo
from src.database.models import User
from src.services.abstract import AbstractAuthService
from src.config.constants import API, AUTH, EMAIL_TOKEN_HOURS_TO_EXPIRE


class AuthService(AbstractAuthService):
    """
    AuthService class for authentication and authorization of users.

    Attributes:
        SECRET_KEY (str): secret key for JWT
        ALGORITHM (str): algorithm for JWT
        EXPIRE_IN_SECONDS (int): expiration time for JWT in seconds
        REFRESH_TOKEN_EXPIRE (int): expiration time for refresh token in days
        ACCESS_TOKEN (str): name of access token scope
        REFRESH_TOKEN (str): name of refresh token scope
        oauth2_scheme (OAuth2PasswordBearer): OAuth2PasswordBearer instance
        cache (Cache): cache instance
    """

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
        """
        Create a token for link sending to user in email.

        Args:
            data (dict): data to encode

        Returns:
            str: token
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            hours=EMAIL_TOKEN_HOURS_TO_EXPIRE
        )
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str) -> str:
        """
        Get email from token.

        Args:
            token (str): token to decode

        Returns:
            str: email from token

        Raises:
            HTTPException: 422 if token is invalid
        """
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
        """
        Update user in cache.

        Args:
            user (User): user to update
        """
        await self.cache.set_to_cache(
            key=user.email, value=user, expire=self.EXPIRE_IN_SECONDS
        )

    async def __prepare_token_to_encode(
        self, data: dict, expires_delta: timedelta, scope: str
    ) -> dict:
        """
        Helper method to prepare token to encode.

        Args:
            data (dict): data to encode
            expires_delta (timedelta): delta to expire token
            scope (str): scope of token

        Returns:
           tuple (dict, str): token to encode and session id
        """
        to_encode = data.copy()
        if scope == self.ACCESS_TOKEN:
            to_encode.update({"session_id": str(uuid.uuid4())})
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update(
            {
                "iat": datetime.now(timezone.utc),
                "exp": expire,
                "scope": scope,
            }
        )
        return to_encode

    async def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta = timedelta(seconds=EXPIRE_IN_SECONDS),
    ) -> tuple[str, str]:
        """
        Create access token.

        Args:
            data (dict): data to encode in token
            expires_delta (timedelta): delta to expire token

        Returns:
            tuple (str, str): encoded access token, session id
        """
        to_encode = await self.__prepare_token_to_encode(
            data, expires_delta, self.ACCESS_TOKEN
        )
        encode_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encode_access_token, to_encode.get("session_id")

    async def create_refresh_token(
        self,
        data: dict,
        expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE),
    ) -> tuple[str, datetime]:
        """
        Create refresh token.

        Args:
            data (dict): data to encode in token
            expires_delta (timedelta): delta to expire token

        Returns:
            tuple (str, datetime): encoded refresh token, expire date
        """
        to_encode = await self.__prepare_token_to_encode(
            data, expires_delta, self.REFRESH_TOKEN
        )
        encode_refresh_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encode_refresh_token, to_encode.get("exp")

    async def decode_refresh_token(self, token: str) -> str:
        """
        Decode refresh token.

        Args:
            token (str): refresh token to decode

        Returns:
            str: email of user

        Raises:
            HTTPException: 401 if token is invalid
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == self.REFRESH_TOKEN:
                email = payload.get("sub")
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except jwt.exceptions.PyJWTError as e:
            print(e)  # TODO: log error
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        user_repo: AbstractUserRepo = Depends(get_user_repo),
    ) -> User:
        """
        Get current user from token.

        Args:
            token (str): token to decode and authenticate user
            user_repo (AbstractUserRepo): user repository

        Returns:
            User: user object

        Raises:
            HTTPException: if token is invalid or user is not found
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if await self.cache.get_from_cache(token):
            raise credentials_exception
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == self.ACCESS_TOKEN:
                email = payload.get("sub")
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except jwt.exceptions.PyJWTError as e:
            print(e)  # TODO: log error
            raise credentials_exception

        user = await self.cache.get_from_cache(f"user:{email}")
        if user is None:
            user = await user_repo.get_user_by_email(email)
            if user is None:
                raise credentials_exception
            await self.cache.set_to_cache(email, user, self.EXPIRE_IN_SECONDS)
        else:
            user = pickle.loads(user)
        return user

    async def get_session_id_from_token(self, token: str, user_email: str) -> str:
        """
        Get session id from token

        Args:
            token (str): token to decode
            user_email (str): email of the user who performed the action

        Returns:
            str: session id from token

        Raises:
                HTTPException: if token is invalid or user email is not the same as the one in the token
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("scope") == self.ACCESS_TOKEN:
                email = payload.get("sub")
                session_id = payload.get("session_id")
                if email != user_email or session_id is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                return session_id
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        except jwt.exceptions.PyJWTError as e:
            print(e)  # TODO: log error
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

    async def delete_user_from_cache(self, user_email: str) -> None:
        """
        Deletes user from cache.

        Args:
            user_email (str): user email
        """
        await self.cache.delete_from_cache(f"user:{user_email}")

    async def add_token_to_blacklist(self, token: str) -> None:
        """
        Adds token to blacklist.

        Args:
            token: logout access token
        """
        await self.cache.set_to_cache(token, "blacklisted", self.EXPIRE_IN_SECONDS)


auth_service = AuthService()
