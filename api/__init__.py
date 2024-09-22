from starlette.applications import Starlette
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser, requires
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from zoneinfo import ZoneInfo
import hashlib
import os
import time
import asyncio
import datetime

from db.CRUD import Users, Miners
from api.Receive import *
from api.Send import *



# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()



routes = [
    Route('/endpoint', miners_endpoint, methods=['GET', 'POST']),
    Route('/get_data', get_miners_data, methods=['GET', 'POST'])
]

app = Starlette(routes=routes)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "key.pem"), ssl_certfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "cert.pem"))