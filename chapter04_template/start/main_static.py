from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

app = FastAPI()

# /static : url path / StaticFiles.directory : directory명 / name : url_for등에서 참조하는 이름
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

# jinja2 Template 생성
templates = Jinja2Templates(directory = 'templates')

@app.get('/items/{id}', response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None) :
    html_name = 'item_static.html'
    return templates.TemplateResponse(
        request = request,
        name = html_name,
        context = {'id' : id, 'q_str' : q}
    )