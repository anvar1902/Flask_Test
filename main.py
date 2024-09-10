from blacksheep.server.application import Application
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from api import app as api_app
from app import app as panel_app

app = Starlette(
    routes=[
        Mount("/panel", panel_app, name="panel"),  # Panel
        Mount("", api_app, name="api"),  # API
        Mount('/static', StaticFiles(directory='static', html=True), name='static')
    ]
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")