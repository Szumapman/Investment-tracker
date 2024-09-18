import abc
from datetime import timedelta

from src.database.models import User
from src.repositories.abstract import AbstractUserRepo


class AbstractPasswordHandler(abc.ABC):
    @abc.abstractmethod
    async def hash_password(self, password: str) -> str:
        pass

    @abc.abstractmethod
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        pass


class AbstractEmailService(abc.ABC):
    @abc.abstractmethod
    async def send_email(self, request_type: str, email: str, username: str, host: str) -> None:
        pass


class AbstractAuthService(abc.ABC):
    @abc.abstractmethod
    async def create_email_token(self, data: dict) -> str:
        pass

    @abc.abstractmethod
    async def get_email_from_token(self, token: str) -> str:
        pass

    @abc.abstractmethod
    async def update_user_in_cache(self, user: User) -> None:
        pass

    @abc.abstractmethod
    async def create_access_token(self, data: dict, expires_delta: timedelta) -> (str, str):
        pass

    @abc.abstractmethod
    async def create_refresh_token(self, data: dict, expires_delta: timedelta) -> (str, str):
        pass

    @abc.abstractmethod
    async def decode_refresh_token(self, token: str) -> str:
        pass

    @abc.abstractmethod
    async def get_current_user(self, token: str, user_repo: AbstractUserRepo) -> User:
        pass
