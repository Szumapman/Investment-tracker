from datetime import datetime
from enum import Enum


from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from src.config.constants import MAX_NOTE_LENGTH


class TransactionTypeEnum(str, Enum):
    INVESTMENT = "INVESTMENT"
    WITHDRAW = "WITHDRAW"


class TransactionIn(BaseModel):
    account_id: int
    amount: float
    note: str | None = None
    type: TransactionTypeEnum

    @field_validator("note")
    def validate_note(cls, value):
        if value and len(value) > MAX_NOTE_LENGTH:
            raise ValueError(f"Note must be less than {MAX_NOTE_LENGTH} characters")
        return value


class TransactionOut(TransactionIn):
    id: int
    deposit_id: int | None
    asset_id: int | None
    currency_invest_id: int | None
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
