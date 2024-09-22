from blacksheep.server.rendering.jinja2 import JinjaRenderer
from starlette.applications import Starlette
from starlette.responses import JSONResponse

from blacksheep.server.application import Application
from blacksheep.server.responses import view_async
from blacksheep.server.routing import Router
from starlette.templating import Jinja2Templates
from blacksheep.settings.html import html_settings



templates = Jinja2Templates(directory='templates', autoescape=False, auto_reload=True)

app_s = Starlette()

@app_s.route("/")
async def hello_world(request):
    context = {'request': request}
    return templates.TemplateResponse('login.html', context)


router = Router()
@router.get("/")
async def hello_world2(request):
    return view_async("login.html", {"example": "Hello", "foo": "World"})

app = Application(router=router)
html_settings.use(JinjaRenderer(loader=, enable_async=True))


import uvicorn
if __name__ == "__main__":
    uvicorn.run(app_s, host="0.0.0.0", port=8000)