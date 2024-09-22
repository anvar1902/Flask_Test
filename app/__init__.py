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



# Главная страница
@requires(['authenticated', 'admin'], redirect="login")
async def home(request: Request):
    return RedirectResponse(url='/panel/main')



# Страница авторизации
async def login(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse(url='/panel/main')

    error = None
    if request.method == 'POST':
        form = await request.form()
        username = form['username']
        password = form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if await users_db.check_user_password(username, hashed_password):
            request.session['user'] = username
            return RedirectResponse(url='/panel/main')
        else:
            error = 'Неправильное имя пользователя или пароль'

    context = {'request': request}
    return templates.TemplateResponse('login.html', context)



# Выход из системы
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url='/login')



# Основная страница админ панели
@requires(['authenticated'], redirect="login")
async def panel_main(request: Request):
    context = {'request': request, 'statistics': True, 'time': time, "data": await miners_db.get_all_miners_all_time_data()}
    return templates.TemplateResponse('panel.html', context)



# Страница настроек админ панели
@requires(['authenticated', 'admin'], redirect="login")
async def panel_settings(request: Request):
    context = {'request': request, 'settings': True, 'time': time, "data": await miners_db.get_all_miners_all_time_data()}
    return templates.TemplateResponse('panel.html', context)


# Определяем маршруты приложения
routes = [
    Route('/', home),
    Route('/login', login, methods=['GET', 'POST']),
    Route('/logout', logout),
    Route('/panel/main', panel_main, methods=['GET', 'POST']),
    Route('/panel/settings', panel_settings),
    Mount('/static', StaticFiles(directory='static', html=True), name='static')
]

# Middleware
middleware = [
    Middleware(SessionMiddleware, secret_key="Aya"),  # Сессии
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())  # Авторизация
]

# Создаем приложение Starlette
app = Starlette(routes=routes, middleware=middleware)

# Запуск приложения
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "key.pem"), ssl_certfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "cert.pem"))