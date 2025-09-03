import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger, String, Text, Enum, ForeignKey,
    DateTime, Numeric, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


NUMERIC = lambda: Numeric(18, 8)

class LotStatus(str, enum.Enum):
    running = "running"
    ended = "ended"


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[LotStatus] = mapped_column(Enum(LotStatus, name="lot_status"), nullable=False,
                                              default=LotStatus.running)
    start_price: Mapped[Decimal] = mapped_column(NUMERIC(), nullable=False)
    current_price: Mapped[Decimal] = mapped_column(NUMERIC(), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now(), nullable=False)
    bids: Mapped[list["Bid"]] = relationship(back_populates="lot", cascade="all, delete-orphan", lazy="selectin")


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id", ondelete="CASCADE"), index=True, nullable=False)
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    amount: Mapped[Decimal] = mapped_column(NUMERIC(), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    lot: Mapped["Lot"] = relationship(back_populates="bids", lazy="selectin")