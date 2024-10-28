from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DepositIn(BaseModel):
    amount: float
    interest_rate: float
    maturity_date: datetime


class DepositOut(DepositIn):
    id: int
    account_id: int

    model_config = ConfigDict(from_attributes=True)


class DepositInfo(BaseModel):
    deposit: DepositOut
    detail: str
