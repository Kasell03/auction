from fastapi import WebSocket


class LotManager:
    _manager_instance: None | dict[int, set[WebSocket]] = None

    @classmethod
    def init(cls):
        if cls._manager_instance is None:
            cls._manager_instance = {}


    @classmethod
    async def send_to_all(cls, lot_id: int, data: dict):
        ws_to_remove = set()

        if lot_id in cls._manager_instance:
            for ws in cls._manager_instance[lot_id]:
                try:
                    await ws.send_json(data=data)
                except Exception:
                    ws_to_remove.add(ws)

        if ws_to_remove:
            for removing_ws in ws_to_remove:
                cls.disconnect(removing_ws, lot_id)


    @classmethod
    async def connect(cls, websocket: WebSocket):
        await websocket.accept()

    @classmethod
    async def subscribe_on_lot(cls, websocket: WebSocket, lot_id: int):
        if lot_id not in cls._manager_instance:
            cls._manager_instance[lot_id] = {websocket,}

    @classmethod
    def disconnect(cls, websocket: WebSocket, lot_id: int):
        if lot_id in cls._manager_instance:
            cls._manager_instance[lot_id].remove(websocket)
            if not cls._manager_instance[lot_id]:
                cls._manager_instance.pop(lot_id)

lot_manager = LotManager()
lot_manager.init()
