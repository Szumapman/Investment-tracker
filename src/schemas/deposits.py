from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.transactions import TransactionOut


class DepositIn(BaseModel):
    interest_rate: float
    maturity_date: datetime


class DepositOut(DepositIn):
    id: int
    account_id: int
    transactions: list[TransactionOut]

    model_config = ConfigDict(from_attributes=True)


class DepositInfo(BaseModel):
    deposit: DepositOut
    detail: str
