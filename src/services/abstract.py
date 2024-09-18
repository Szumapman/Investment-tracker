import abc
from datetime import timedelta, datetime

from src.database.models import User
from src.repositories.abstract import AbstractUserRepo


class AbstractPasswordHandler(abc.ABC):
    """
    Abstract class for password handler
    """

    @abc.abstractmethod
    async def hash_password(self, password: str) -> str:
        """
        Hash password
        Args:
            password (str): password to hash

        Returns:
            str: hashed password
        """
        pass

    @abc.abstractmethod
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify password

        Args:
            password (str): password to verify
            hashed_password (str): hashed password to verify against

        Returns:
            bool: True if password is valid, False otherwise
        """
        pass


class AbstractEmailService(abc.ABC):
    """
    Abstract class for email service
    """

    @abc.abstractmethod
    async def send_email(
        self, request_type: str, email: str, username: str, host: str
    ) -> None:
        """
        Method to send email

        Args:
            request_type (str): type of request
            email (str): email to send to
            username (str): username to send to
            host (str): host used to send email
        """
        pass


class AbstractAuthService(abc.ABC):
    """
    Abstract class for auth service
    """

    @abc.abstractmethod
    async def create_email_token(self, data: dict) -> str:
        """
        Method to create token used in link sent to user

        Args:
            data (dict): data to be encoded in token

        Returns:
            str: token
        """
        pass

    @abc.abstractmethod
    async def get_email_from_token(self, token: str) -> str:
        """
        Method to get email from token

        Args:
            token (str): token to decode

        Returns:
            str: email
        """
        pass

    @abc.abstractmethod
    async def update_user_in_cache(self, user: User) -> None:
        """
        Method to update user in cache

        Args:
            user (User): user to update
        """
        pass

    @abc.abstractmethod
    async def create_access_token(
        self, data: dict, expires_delta: timedelta
    ) -> (str, str):
        """
        Method to create access token

        Args:
            data (dict): data to encode
            expires_delta (timedelta): delta to expire token

        Returns:
            tuple (str, str): encoded access token, session id
        """
        pass

    @abc.abstractmethod
    async def create_refresh_token(
        self, data: dict, expires_delta: timedelta
    ) -> (str, datetime):
        """
        Method to create refresh token

        Args:
            data (dict): data to encode
            expires_delta (timedelta): delta to expire token

        Returns:
            tuple (str, datetime): encoded refresh token, token expire time
        """
        pass

    @abc.abstractmethod
    async def decode_refresh_token(self, token: str) -> str:
        """
        Method to decode refresh token

        Args:
            token (str): token to decode

        Returns:
            str: email
        """
        pass

    @abc.abstractmethod
    async def get_current_user(self, token: str, user_repo: AbstractUserRepo) -> User:
        """
        Method to get current user

        Args:
            token (str): token to decode
            user_repo (AbstractUserRepo): user repository

        Returns:
            User: user
        """
        pass

    @abc.abstractmethod
    async def get_session_id_from_token(self, token: str, user_email: str) -> str:
        """
        Method to get session id from token

        Args:
            token (str): token to decode
            user_email (str): email of user who performed action

        Returns:
            str: session id
        """
        pass

    @abc.abstractmethod
    async def delete_user_from_cache(self, user_email: str) -> None:
        """
        Method to delete user from cache

        Args:
            user_email (str): email of user to delete
        """
        pass
