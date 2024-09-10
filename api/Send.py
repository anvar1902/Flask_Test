from blacksheep.server.application import Application
from blacksheep.server.responses import json
from blacksheep.messages import Request
from blacksheep.server.routing import Router

from db.CRUD import Users, Miners

# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()

router = Router()



@router.get("/get_miners_data")
async def get_miners_data(request: Request):
    return json(await miners_db.get_all_miners_all_time_data())