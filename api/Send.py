from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse, PlainTextResponse, JSONResponse
import json

from db.CRUD import Users, Miners

# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()



async def get_miners_data(request: Request):
    print(await miners_db.get_all_miners_all_time_data())
    return PlainTextResponse(str(await miners_db.get_all_miners_all_time_data()))