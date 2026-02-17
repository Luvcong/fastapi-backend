from pydantic import BaseModel
from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()

# 개별 Form data 값을 Form()에서 처리하여 수행함수 적용
# Form()은 form data값이 반드시 입력되어야 함 -> Form(None)과 Annotated[str, Form()] = None은 Optional
@app.post('/login')
async def login(username: str = Form(),
                email: str = Form(),
                country: Annotated[str, Form()] = None) :
    return {'username' : username, 'email' : email, 'country' : country}


# ellipsis(...) 을 사용하면 form data값이 반드시 입력되어야 함
# Form() == From(...) 같은 의미 -> 보통 Form() 문법을 더 많이 사용
@app.post('/login_f/')
async def login(username: str = Form(...), 
                email: str = Form(...),
                country: Annotated[str, Form()] = None):
    return {'username' : username, 'email' : email, 'country' : country}

# path, query parameter 함께 사용
@app.post('/login_pq/{login_gubun}')
async def login(login_gubun: int,
                q: str | None = None, 
                username: str = Form(), 
                email: str = Form(),
                country: Annotated[str, Form()] = None):
    return {"login_gubun": login_gubun,
            "q": q,
            "username": username, 
            "email": email, 
            "country": country}

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# json request body용 end point
@app.post("/items_json/")
async def create_item_json(item: Item):
    return item

# form tag용 end point
@app.post("/items_form/")
async def create_item_from(name: str = Form(),
                           description: Annotated[str, Form()] = None,
                           price: str = Form(),
                           tax: Annotated[int, Form()] = None
                           ):
    return {"name": name, "description": description, "price": price, "tax": tax}

"""
create_item_json / create_item_form은 동일한 코드지만,
json, form 타입을 구분해서 코드를 작성해주는 것이 좋음

-> json은 pydantic 객체를 한번에 전달해도 무방
-> form은 전달 파라미터마다 각각 작성해주는 것을 권장
"""