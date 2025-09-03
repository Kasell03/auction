from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi import status

from models.auction import Lot, Bid, LotStatus
from schemas.auction import LotCreateSchema, LotSchema, BidCreateSchema, BidReadSchema
from utils.responses import error_exception


class AuctionCRUD:
    @staticmethod
    async def create_lot(db: AsyncSession, lot_data: LotCreateSchema) -> dict:
        stmt = (
            insert(Lot)
            .values(
                **lot_data.model_dump(),
                current_price=lot_data.start_price
            )
            .returning(Lot)
        )
        result = await db.execute(stmt)
        await db.commit()

        created_lot = result.scalar_one()
        lot_dict = LotSchema.model_validate(created_lot).model_dump(mode="json")

        return lot_dict

    @staticmethod
    async def get_lots(db: AsyncSession) -> list[dict]:
        query = (
            select(Lot)
            .options(selectinload(Lot.bids))
            .where(Lot.status==LotStatus.running.value)
            .order_by(Lot.id)

        )

        result = await db.execute(query)
        lots = result.scalars().all()

        return [LotSchema.model_validate(lot).model_dump(mode="json") for lot in lots]

    @staticmethod
    async def is_lot_exist(db: AsyncSession, lot_id: int) -> bool:
        lot = await db.get(Lot, lot_id)
        return bool(lot)


    @staticmethod
    async def create_bid(db: AsyncSession, bid_data: BidCreateSchema, lot_id: int):
        lot = await db.get(Lot, lot_id)

        if lot is None:
            raise error_exception(status_code=status.HTTP_404_NOT_FOUND, detail="Lot with this ID not found")

        if lot.status == LotStatus.ended:
            raise error_exception(status_code=status.HTTP_409_CONFLICT, detail="Bids not allowed")

        lot.current_price = lot.current_price + bid_data.amount

        stmt = (
            insert(Bid)
            .values(
                **bid_data.model_dump(),
                lot_id=lot_id,
            )
            .returning(Bid.id, Bid.user_name, Bid.amount, Bid.created_at, Bid.lot_id)
        )

        result = await db.execute(stmt)
        await db.commit()
        bid = result.mappings().one()

        return BidReadSchema.model_validate(bid).model_dump(mode="json")
