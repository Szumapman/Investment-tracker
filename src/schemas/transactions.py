from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from src.config.constants import MAX_NOTE_LENGTH


class TransactionIn(BaseModel):
    amount: float
    note: str | None = None

    @field_validator("note")
    def validate_note(cls, value):
        if value and len(value) > MAX_NOTE_LENGTH:
            raise ValueError(f"Note must be less than {MAX_NOTE_LENGTH} characters")
        return value


class TransactionOut(TransactionIn):
    id: int
    account_id: int
    deposit_id: int | None
    asset_id: int | None
    currency_invest_id: int | None
    type: str
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
