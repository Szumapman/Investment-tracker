from datetime import datetime

from pydantic import BaseModel


class DepositIn(BaseModel):
    amount: float
    interest_rate: float
    maturity_date: datetime


class DepositOut(DepositIn):
    id: int
    account_id: int


class DepositInfo(BaseModel):
    deposit: DepositOut
    detail: str
