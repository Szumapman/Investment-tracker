import abc


class AbstractPasswordHandler(abc.ABC):
    @abc.abstractmethod
    async def hash_password(self, password: str) -> str:
        pass

    @abc.abstractmethod
    async def verify_password(self, password: str, hashed_password: str) -> bool:
        pass


class AbstractEmailService(abc.ABC):
    @abc.abstractmethod
    async def send_confirmation_email(
        self, email: str, username: str, host: str
    ) -> None:
        pass


class AbstractAuthService(abc.ABC):
    @abc.abstractmethod
    async def create_email_token(self, data: dict) -> str:
        pass
