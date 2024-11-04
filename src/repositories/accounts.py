from sqlalchemy.orm import Session

from src.repositories.abstract import AbstractAccountRepo
from src.database.models import Account
from src.schemas.accounts import AccountIn


class PostgresAccountRepo(AbstractAccountRepo):
    def __init__(self, db: Session):
        self.db = db

    async def get_account_by_id(self, account_id: int) -> Account:
        return self.db.query(Account).filter(Account.id == account_id).first()

    async def get_accounts(self, user_id: int) -> list[Account]:
        accounts = self.db.query(Account).filter(Account.user_id == user_id).all()
        return accounts

    async def create_account(self, user_id: int, account_in: AccountIn) -> Account:
        new_account = Account(
            user_id=user_id,
            balance_investable_funds=account_in.balance_investable_funds,
            currency=account_in.currency,
        )
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account

    async def update_funds(self, account_id: int, amount: float) -> Account:
        account = self.get_account_by_id(account_id)
        account.balance_investable_funds += amount
        self.db.commit()
        self.db.refresh(account)
        return account

    async def delete_account(self, account_id: int) -> Account:
        account = self.get_account_by_id(account_id)
        self.db.delete(account)
        self.db.commit()
        return account
