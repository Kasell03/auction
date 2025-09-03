from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import settings
from routers import v1, ws


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router_v1 in v1.routers:
    app.include_router(router_v1, prefix=v1.prefix)

for ws_router in ws.routers:
    app.include_router(ws_router)

"""
    PS:
        Редіс не додав бо не має сенсу через те, що я не реалізовував аутентифікацію, щоб мати унікальний ідентифікатор користувачів щоб у редісі зберігати
        підписку юзера на конкретний лот, на випадок розриву підключення, щоб при повторному підключені можна було б відновити стару підписку)
"""