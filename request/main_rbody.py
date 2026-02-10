from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()

# 1) Pydantic Model 생성
# Pydantic Model 클래스는 반드시 BaseModel을 상속받아 생성
class Item(BaseModel) :
    name : str
    description : str | None = None  # description: Optional[str] = None
    price : float
    tax : float | None = None        # tax: Optional[float] = None
    
# 2) 기본
@app.post("/items")
async def create_item(item: Item):  # 파라미터 값으로 Pydantic model이 입력되면 Json 형태의 Request Body 처리
    print(">>> item type:", type(item))
    print(">>> item:", item)
    return item

"""
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
"""

# 3) Pydantic Model 값 업데이트
# model_dump() => pydantic model 객체를 dict 형태로 반환
@app.post("/items_tax/")
async def create_item_tax(item: Item) :
    item_dict = item.model_dump()
    print(">>> item_dict:", item_dict)

    if item.tax:
        price_with_tax = item.price + item.tax
        # item.price_with_tax  # 에러 발생 (이미 선언된 Pydantic model 객체에 직접 접근해서 값 추가는 불가)
        item_dict.update({"price_with_tax": price_with_tax})
    
    return item_dict   

# 4) Path, Query, Request Body 모두 함께 사용
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    
    if q:
        result.update({"q": q})
        print('>>> reesult : ', result)
    return result

# User 객체 생성
class User(BaseModel):
    username: str
    full_name: str | None = None    #full_name: Optional[str] = None

# 여러개의 request body parameter 처리
# json 데이터의 이름값과 수행함수의 인자명이 같아야 함
@app.put("/items_mt/{item_id}")
async def update_item_mt(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    print("results:", results)
    # results: {'item_id': 2, 'item': Item(name='Foo', description='The pretender', price=42.0, tax=3.2), 'user': User(username='dave', full_name='Dave Grohl')}
    return results

