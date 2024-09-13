import abc

from src.database.models import User
from src.schemas.users import UserIn


class AbstractUserRepo(abc.ABC):
    @abc.abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        pass

    @abc.abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        pass

    @abc.abstractmethod
    async def create_user(self, user: UserIn) -> User:
        pass

    @abc.abstractmethod
    async def confirm_user_email(self, email: str) -> None:
        pass
