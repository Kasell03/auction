from fastapi import APIRouter

from crud.auction import AuctionCRUD
from dependencies.db import SessionDep
from schemas.auction import LotCreateSchema, BidCreateSchema
from utils.responses import success_response
from services.ws_manager import lot_manager

router = APIRouter(prefix="/lots", tags=["lots"])


@router.get("/")
async def get_lots(db: SessionDep):
    lots: list[dict] = await AuctionCRUD.get_lots(db=db)
    return success_response(data=lots)


@router.post("/")
async def create_lot(db: SessionDep, lot_data: LotCreateSchema):
    created_lot = await AuctionCRUD.create_lot(db=db, lot_data=lot_data)
    return success_response(data=created_lot)


@router.post("/{lot_id}/bids")
async def make_bid(db: SessionDep, bid_data: BidCreateSchema, lot_id: int):
    ws_data = {
        "type": "bid_placed",
        "lot_id": lot_id,
        "bidder": bid_data.user_name,
        "amount": float(bid_data.amount)
    }
    created_bid = await AuctionCRUD.create_bid(db=db, bid_data=bid_data, lot_id=lot_id)
    await lot_manager.send_to_all(lot_id=lot_id, data=ws_data)
    return success_response(data=created_bid)