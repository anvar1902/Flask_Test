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

from api import app as api_app
from app import app as panel_app

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        # Проверка, авторизован ли пользователь через сессии
        if conn.session.get("user"):
            username = conn.session["user"]
            return AuthCredentials(["authenticated", username]), SimpleUser(username)

middleware = [
    Middleware(SessionMiddleware, secret_key="Aya"),  # Сессии
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())  # Авторизация
]

app = Starlette(
    routes=[
        Mount("/api", api_app),
        Mount("/", panel_app),
        Mount('/static', StaticFiles(directory='static', html=True), name='static')
    ],
    middleware=middleware
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")