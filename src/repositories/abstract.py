import abc
from datetime import datetime

from src.database.models import User, RefreshToken, Account, CurrencyInvest, Transaction
from src.schemas.users import UserIn
from src.schemas.accounts import AccountIn
from src.schemas.currency_invests import CurrencyInvestToBuy
from src.schemas.transactions import TransactionIn


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

    @abc.abstractmethod
    async def update_password(self, user: User) -> User:
        pass


class AbstractTokenRepo(abc.ABC):
    @abc.abstractmethod
    async def add_refresh_token(
        self, refresh_token: str, user_id: int, session_id: str, expires_at: datetime
    ) -> None:
        pass

    @abc.abstractmethod
    async def get_refresh_token(self, refresh_token: str) -> RefreshToken | None:
        pass

    @abc.abstractmethod
    async def get_refresh_tokens(self, user_id: int) -> list[RefreshToken]:
        pass

    @abc.abstractmethod
    async def delete_refresh_token(
        self,
        refresh_token: str = None,
        user_id: int = None,
        session_id: dict = None,
    ) -> None:
        pass

    @abc.abstractmethod
    async def remove_expired_refresh_tokens(self, user_id: int) -> None:
        pass


class AbstractAccountRepo(abc.ABC):
    @abc.abstractmethod
    async def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abc.abstractmethod
    async def get_accounts(self, user_id: int) -> list[Account]:
        pass

    @abc.abstractmethod
    async def create_account(self, user_id: int, account_in: AccountIn) -> Account:
        pass

    @abc.abstractmethod
    async def update_funds(self, account_id: int, amount: float) -> Account:
        pass

    @abc.abstractmethod
    async def delete_account(self, account_id: int) -> None:
        pass


class AbstractCurrencyInvestRepo(abc.ABC):
    @abc.abstractmethod
    async def get_currency_invest_by_id(
        self, currency_invest_id: int
    ) -> CurrencyInvest:
        pass

    # @abc.abstractmethod
    # async def get_currency_invests(self, account_id: int) -> list[CurrencyInvest]:
    #     pass

    @abc.abstractmethod
    async def create_currency_invest(
        self, transaction_in: TransactionIn, currency_invest_to_buy: CurrencyInvestToBuy
    ) -> CurrencyInvest:
        pass

    # @abc.abstractmethod
    # async def update_currency_invest(self, currency_invest_id: int, currency_invest_to_buy: CurrencyInvestToBuy) -> CurrencyInvest:
    #     pass

    # @abc.abstractmethod
    # async def delete_currency_invest(self, currency_invest_id: int) -> None:
    #     pass
