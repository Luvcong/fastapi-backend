# Request : HTTP 요청의 메서드, URL, 헤더, 쿠키, 클라이언트 IP 등 모든 원시 정보에 접근할 수 있는 객체
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/items")
async def read_item(request: Request) :
    client_host = request.client.host
    headers = request.headers
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

# path parameter 같이 사용
@app.get("/items/{item_group}")
async def read_item_p(request: Request, item_group: str):
    client_host = request.client.host
    headers = request.headers 
    query_params = request.query_params
    url = request.url
    path_params = request.path_params
    http_method = request.method

    return {
        "client_host": client_host,
        "headers": headers,
        "query_params": query_params,
        "path_params": path_params,
        "url": str(url),
        "http_method":  http_method
    }

@app.post("/items_json/")
async def create_item_json(request: Request):
    data =  await request.json()  # Parse JSON body
    print("received_data:", data) # received_data: {'name': 'Foo', 'description': 'An optional description', 'price': 45.2, 'tax': 3.5}
    return {"received_data": data} 
# request.json()을 사용하면 반환타입이 dict

@app.post("/items_form/")
async def create_item_form(request: Request):
    data = await request.form()    # Parse Form body
    print("received_data:", data)  # received_data: FormData([('username', 'kim'), ('email', 'kim@didim.com')])
    return {"received_data": data}
# request.form()을 사용하면 반환타입이 FormData