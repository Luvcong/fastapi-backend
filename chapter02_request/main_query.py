# Query Parameter (= Query String) : URL에서 ? 뒤에 KEY와 VALUE 값을 가지는 형태로 전달 (개별 parameter는 & 로 구분)
# └ http://localhost:9091/items/1?q=Boo => ? 뒤에 값들이 query Parameter 값

from fastapi import FastAPI
from typing import Optional

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# query parameter의 타입과 default값을 함수인자로 설정할 수 있음
# http://localhost:9091/items?skip=0&limit=2

# 1) default 값 설정 o
@app.get('/items')
def read_item(skip: int = 0, limit: int = 2) :
    return fake_items_db[skip: skip + limit]

# 2) default 값 설정 x
# default 값을 설정하지 않은 경우 query parameter에 반드시 해당 인자가 주어져야 함 -> 그렇지 않으면 Pydantic 오류 발생
# SwaggerUI애서 default 값을 설정하지 않은 파라미터는 *required 표시
@app.get('/items_nd')
def read_item_nd(skip: int, limit: int) :
    return fake_items_db[skip: skip + limit]

# 3) default = None
@app.get('/items_op')
def read_item_op(skip: int, limit: int = None) :
    # default 값을 None 으로 설정한 경우에도 파라미터를 넘기지 않은 경우 500 Internal Server Error 발생 (None은 연산이 불가하기 떄문에)
    # return fake_items_db[skip : skip + limit]
    if limit :
        return fake_items_db[skip: skip + limit]
    else :
        return {"limit is not provided"}

# 4) Optional 사용
# Optional을 사용하는 경우에도 default 값을 설정해주어야 함 -> 그렇지 않으면 Pydantic 오류 발생
@app.get('/items_op2')
def read_item_op(skip: int, limit: Optional[int] = None) :
    if limit :
        return fake_items_db[skip: skip + limit]
    else :
        return {"limit is not provided"}

# 5) Path Parameter + Query Parameter 함께 사용
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Default 값 None 설정
# - q : str | None = None         -> 3.10 이상부터 사용 가능
# - q : Optional[int] = None