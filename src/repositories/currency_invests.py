from sqlalchemy.orm import Session

from src.repositories.abstract import AbstractCurrencyInvestRepo
from src.database.models import CurrencyInvest, Transaction, Account
from src.schemas.currency_invests import CurrencyInvestToBuy
from src.schemas.transactions import TransactionIn


class PostgresCurrencyInvestRepo(AbstractCurrencyInvestRepo):

    def __init__(self, db: Session):
        self.db = db

    async def get_currency_invest_by_id(
        self, currency_invest_id: int
    ) -> CurrencyInvest:
        return (
            self.db.query(CurrencyInvest)
            .filter(CurrencyInvest.id == currency_invest_id)
            .first()
        )

    async def create_currency_invest(
        self, transaction_in: TransactionIn, currency_invest_to_buy: CurrencyInvestToBuy
    ) -> CurrencyInvest:
        new_currency_invest = CurrencyInvest(
            currency=currency_invest_to_buy.currency,
            purchase_exchange_rate=currency_invest_to_buy.purchase_exchange_rate,
            current_amount=currency_invest_to_buy.purchase_exchange_rate
            * transaction_in.amount,
        )
        self.db.add(new_currency_invest)
        self.db.commit()
        self.db.refresh(new_currency_invest)
        new_transaction = Transaction(
            account_id=transaction_in.account_id,
            currency_invest_id=new_currency_invest.id,
            amount=transaction_in.amount,
            type=transaction_in.type,
            note=transaction_in.note,
        )
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_currency_invest)
        account = (
            self.db.query(Account)
            .filter(Account.id == transaction_in.account_id)
            .first()
        )
        if transaction_in.type == "INVESTMENT":
            account.balance_investable_funds -= transaction_in.amount
        elif transaction_in.type == "WITHDRAW":
            account.balance_investable_funds += transaction_in.amount
        else:
            raise ValueError("Invalid transaction type")
        self.db.commit()
        return new_currency_invest
