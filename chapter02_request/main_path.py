# Path Parameter : URL Path의 일부로 path에 정보를 담아서 Request로 전달
# └ http://localhost:9091/items/1 => 1이 path parameter 값

from fastapi import FastAPI

app = FastAPI()

@app.get('/items/all')
def read_all_items():
    return {"message": "all items"}

@app.get('/items/{item_id}')    # {}로 지정된 변수가 path parameter
def read_id(item_id: int) :     # type hint : int형이 아닌 다른 자료형을 넣으면 에러 발생 (Pydantic)
    return {'item_id' : item_id}    # dict 형태로 반환하면 content-type: application/json

# 아래 api는 절대 들어올 수가 없음
# api 매핑 순서는 위에서부터 순차적으로 진행되어 /items/{item_id}에 매핑됨
# └ Path Parameter값과 특정 지정 Path가 충돌되지 않도록 endpoint 작성 코드 위치에 주의!
@app.get('/items/all')
def read_all_items():
    return {"message": "all items"}