"""
jinja2 : 화면 표시를 담당하는 frontend 코드와 데이터를 처리하는 backend 코드를 분리하여 개발 효율성을 높여주는 템플릿 엔진

- {{ }} : 변수 출력시 사용
- {% %} : if, for 문에서 사용
- {# #} : 주석
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 1) jinja2 Template 생성 (인자로 directory 입력)
templates = Jinja2Templates(directory='templates')

class Item(BaseModel) :
    name : str
    price : float

# response_class = HTMLResponse를 생략하면 Swagger UI에서 application/json으로 인식
@app.get('/items/{id}', response_class=HTMLResponse)
async def read_item(request: Request, id: str, q: str | None = None) :
    # 내부에서 Pydantic 객체 생성
    item = Item(name = 'test_item', price = 10)

    # Pydantic -> dict 변환
    item_dict = item.model_dump()

    return templates.TemplateResponse(
        request = request,
        name = 'item.html',  # template 파일명
        context = {'id' : id, 'q_str' : q, 'item' : item, 'item_dict' : item_dict}  # key 값이 tempalte으로 전달
    )

    # FastAPI 0.108 이하 버전에서는 아래와 같이 TemplateResponse() 인자 호출
    # return templates.TemplateResponse(name="item.html",
    #                                   {"request": request, "id": id, "q_str": q, "item": item, "item_dict": item_dict})


@app.get('/item_gubun')
async def read_item_by_gubun(request: Request, gubun: str) :
    item = Item(name = 'test_item_02', price = 4.0)

    return templates.TemplateResponse(
        request = request,
        name = 'item_gubun.html',
        context = {'gubun' : gubun, 'item' : item}
    )

@app.get('/all_items', response_class=HTMLResponse)
async def read_all_items(request: Request) :
    all_items = [Item(name = 'test_item_' + str(i), price = i) for i in range(5)]
    print('all_items : ', all_items)
    
    return templates.TemplateResponse(
        request = request,
        name = 'item_all.html',
        context = {'all_items' : all_items}
    )

# safe read
@app.get('/read_safe', response_class=HTMLResponse)
async def read_safe(request: Request) :
    html_str = '''
    <ul>
    <li>튼튼</li>
    <li>저렴</li>
    </ul>
    '''

    return templates.TemplateResponse(
        request = request,
        name = 'read_safe.html',
        context = {'html_str' : html_str}
    )