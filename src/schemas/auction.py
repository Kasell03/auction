import datetime
import decimal

from pydantic import BaseModel, ConfigDict, Field

from models.auction import LotStatus

class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class BidReadSchema(Base):
    id: int
    user_name: str
    amount: decimal.Decimal
    created_at: datetime.datetime
    lot_id: int


class BidCreateSchema(Base):
    user_name: str
    amount: decimal.Decimal = Field(..., gt=0)


class LotSchema(Base):
    id: int
    title: str
    description: str
    status: LotStatus
    start_price: decimal.Decimal
    current_price: decimal.Decimal
    created_at: datetime.datetime
    updated_at: datetime.datetime
    bids: list[BidReadSchema] = []


class LotCreateSchema(Base):
    title: str
    description: str
    start_price: decimal.Decimal = Field(..., gt=0)
