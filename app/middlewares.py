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
from jinja2 import Environment, FileSystemLoader
from zoneinfo import ZoneInfo
import hashlib
import os
import time
import asyncio
import datetime

from db.CRUD import Users, Miners



# Создаем объекты для работы с базой данных
users_db = Users()
miners_db = Miners()

# Подключаем шаблонизатор Jinja2
templates = Jinja2Templates(directory='templates', autoescape=False, auto_reload=True)



class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        # Проверка, авторизован ли пользователь через сессии
        if conn.session.get("user"):
            username = conn.session["user"]
            return AuthCredentials(["authenticated", username]), SimpleUser(username)