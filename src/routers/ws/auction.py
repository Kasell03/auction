from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from dependencies.db import SessionDep
from crud.auction import AuctionCRUD
from services.ws_manager import lot_manager

router = APIRouter(prefix="/lots")

@router.websocket("/{lot_id}")
async def lot_ws(db: SessionDep,websocket: WebSocket, lot_id: int):
    is_lot = await AuctionCRUD.is_lot_exist(db=db, lot_id=lot_id)

    await lot_manager.connect(websocket=websocket)

    if not is_lot:
        await websocket.send_json({"error": "Lot with this ID not found"})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await lot_manager.subscribe_on_lot(websocket=websocket, lot_id=lot_id)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        lot_manager.disconnect(websocket=websocket, lot_id=lot_id)
