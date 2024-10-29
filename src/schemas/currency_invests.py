from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.transactions import TransactionOut


class CurrencyInvestIn(BaseModel):
    currency: str


class CurrencyInvestToBuy(CurrencyInvestIn):
    purchase_exchange_rate: float


class CurrencyInvestOut(CurrencyInvestToBuy):
    id: int
    account_id: int
    purchase_date: datetime
    current_amount: float
    transactions: list[TransactionOut]

    model_config = ConfigDict(from_attributes=True)


class CurrencyInvestInfo(BaseModel):
    currency_invest: CurrencyInvestOut
    detail: str
