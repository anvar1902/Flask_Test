from blacksheep.server import Application
from blacksheep.server.authentication import Authentication, AuthResult
from blacksheep.server.authentication.cookie import CookieAuthentication
from blacksheep.server.middleware.sessions import SessionMiddleware
from blacksheep.server.static import StaticFilesHandler
from blacksheep.messages import Request
from blacksheep import Response, TextContent
from blacksheep.server.responses import redirect
from blacksheep.templating import use_templates

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
templates = use_templates(directory='templates', autoescape=False, auto_reload=True)


# Класс для базовой авторизации
class BasicAuthBackend(Authentication):
    async def authenticate(self, request: Request):
        # Проверка, авторизован ли пользователь через сессии
        if request.session.get("user"):
            username = request.session["user"]
            # Возвращаем успех аутентификации с учётом "authenticated" и роли пользователя
            return AuthResult(True, username=username, roles=["authenticated", username])
        return AuthResult(False)


# Создаем приложение BlackSheep
app = Application()

# Подключаем middleware для сессий и авторизации
app.middlewares.append(SessionMiddleware(secret="Aya"))
app.middlewares.append(CookieAuthentication(backend=BasicAuthBackend()))

# Добавляем поддержку статических файлов
app.serve_files(StaticFilesHandler('./static'), root_path='/static')


# Главная страница
@app.router.get("/")
@BasicAuthBackend.require_roles(['authenticated', 'admin'], redirect_to="/login")
async def home(request: Request):
    return redirect('/panel/main')


# Страница авторизации
@app.router.route("/login", methods=['GET', 'POST'])
async def login(request: Request):
    if request.user.is_authenticated:
        return redirect('/panel/main')

    error = None
    if request.method == 'POST':
        form = await request.form()
        username = form['username']
        password = form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if await users_db.check_user_password(username, hashed_password):
            request.session['user'] = username
            return redirect('/panel/main')
        else:
            error = 'Неправильное имя пользователя или пароль'

    context = {'request': request}
    return templates.render('login.html', context)


# Выход из системы
@app.router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return redirect('/login')


# Основная страница админ панели
@app.router.route("/panel/main", methods=['GET', 'POST'])
@BasicAuthBackend.require_roles(['authenticated'], redirect_to="/login")
async def panel_main(request: Request):
    context = {
        'request': request,
        'statistics': True,
        'time': time,
        "data": await miners_db.get_all_miners_all_time_data()
    }
    return templates.render('panel.html', context)


# Страница настроек админ панели
@app.router.get("/panel/settings")
@BasicAuthBackend.require_roles(['authenticated', 'admin'], redirect_to="/login")
async def panel_settings(request: Request):
    context = {
        'request': request,
        'settings': True,
        'time': time,
        "data": await miners_db.get_all_miners_all_time_data()
    }
    return templates.render('panel.html', context)


# Запуск приложения
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "key.pem"), ssl_certfile=os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), "cert.pem"))
