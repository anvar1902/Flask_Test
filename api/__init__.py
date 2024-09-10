from blacksheep.server.application import Application
from blacksheep.server.responses import json, file, redirect
from blacksheep.server.routing import Router
from zoneinfo import ZoneInfo
import hashlib
import os
import time
import asyncio
import datetime

from db.CRUD import Users, Miners
import api.Receive as Receive
import api.Send as Send



# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()

router = Router(prefix="/api", sub_routers=[Receive.router, Send.router])





app = Application(router=router)
app.base_path = "/api"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "key.pem"), ssl_certfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "cert.pem"))