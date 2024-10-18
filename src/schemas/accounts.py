from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict

class CurrencyEnum(str, Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"

class AccountIn(BaseModel):
    currency: CurrencyEnum
    balance_investable_funds: float = Field(default=0.00, ge=0, description="Balance of investable funds in the account must be greater than or equal to 0.00")
    
    @field_validator("balance_investable_funds")
    def validate_balance_investable_funds(cls, value):
        if value < 0.00:
            raise ValueError("Balance of investable funds in the account must be greater than or equal to 0.00")
        if round(value, 2) != value:
            raise ValueError("Balance of investable funds in the account must be a float with 2 decimal places")
        return value
    

class AccountOut(BaseModel):
    id: int
    user_id: int
    balance_investable_funds: float
    currency: CurrencyEnum
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    

class AccountInfo(BaseModel):
    account: AccountOut
    detail: str
    
    
class AccountFunds(BaseModel):
    balance_investable_funds: float = Field(default=0.00, ge=0, description="Balance of investable funds in the account must be greater than or equal to 0.00")
    
    @field_validator("balance_investable_funds")
    def validate_balance_investable_funds(cls, value):
        if value < 0.00:
            raise ValueError("Balance of investable funds in the account must be greater than or equal to 0.00")
        if round(value, 2) != value:
            raise ValueError("Balance of investable funds in the account must be a float with 2 decimal places")
        return value