from sqlalchemy.orm import Session

from src.repositories.abstract import AbstractAccountRepo
from src.database.models import Account
from src.schemas.accounts import AccountIn

class PostgresAccountRepo(AbstractAccountRepo):
    def __init__(self, db: Session):
        self.db = db
        
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