from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetIn(BaseModel):
    asset_name: str


class AssetToBuy(AssetIn):
    purchase_share_price: float
    share_quantity: float


class AssetOut(AssetToBuy):
    id: int
    account_id: int
    purchase_date: datetime
    current_share_quantity: float

    model_config = ConfigDict(from_attributes=True)


class AssetInfo(BaseModel):
    asset: AssetOut
    detail: str
