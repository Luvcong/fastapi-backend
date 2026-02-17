"""
1) JSONResponse      : JSON타입 Content 전송 (Python objevt -> json 포맷으로 자동 변환)
2) HTMLResponse      : HTML Content 전송
3) RedirectRespone   : 요청 처리 후 다른 URL로 Client를 다른 URL로 리다이렉트 하기 위해 사용
4) PlainTextResponse : 일반 Text Content 전송
5) FileResponse      : 파일을 다운로드 할 때 주로 사용
6) StreamingResponse : 대용량 파일의 스트리밍이나 채팅 메시지 등에서 사용
"""

from fastapi import FastAPI, Form, status
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    RedirectResponse
)

app = FastAPI()

# 1) JSON Response
@app.get('/resp_json/{item_id}', response_class=JSONResponse)    # response_class default value : JSONReponse
async def response_json(item_id: int, q: str | None = None) :
    return JSONResponse(content={'message' : 'hello world', 'item_id' : item_id, 'q' : q},
                        status_code=status.HTTP_200_OK
                        )

# 2) HTML Response
@app.get('/resp_html/{item_id}', response_class=HTMLResponse)
async def response_html(item_id: int, item_name: str | None = None) :
    html_str = f'''
    <html>
    <body>
        <h2>HTML Response</h2>
        <p>item_id: {item_id}</p>
        <p>item_name: {item_name}</p>
    </body>
    </html>
    '''
    return HTMLResponse(content = html_str, status_code=status.HTTP_200_OK)

# 3) Redirect (Get -> Get)
@app.get('/redirect')
async def redirect_only(comment: str | None = None) :
    print(f'redirect : {comment}')

    # RedirectReponse status code default value : 307 TEMPORARY_REDIRECT
    return RedirectResponse(url=f'/resp_html/3?item_name={comment}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)

# 3) Redirect (Post -> Get)
@app.post('/create_redirect')
async def create_item(item_id: int = Form(), item_name: str = Form()) :
    print(f'item_id : {item_id} / item_name : {item_name}')

    # method가 변경되는 경우 sdtatus code default value : 302 FOUND
    # status code를 적지 않으면 405 Error: Method Not Allowed 발생
    return RedirectResponse(url=f'/resp_html/{item_id}?item_name={item_name}', status_code=status.HTTP_302_FOUND)

# 302 FOUND / 303 SEE_OTHER 구분
# - 302 FOUND     : HTTP 스펙상으로는 명확하게 GET Method 전환으로 명시되어 있지 않으나 대부분의 브라우저들이 302 코드에 대해서 Get Method로 전환함
# - 303 SEE_OTHER : HTTP 스펙상으로 명확하게 GET Method 전환으로 명시가 되어있음 (정석)

"""
1. HTTP Status Code
- 2xx : 성공적으로 요청 수행
- 3xx : 추가적인 Redirection 요청
- 4xx : Client의 잘못된 요청 등의 오류
- 5xx : Server 오류

2. HTTP 응답은 상태 라인, 헤더, 바디 3가지로 구성
- 상태 라인 : 버전 / 코드
- 헤더 : 메타 데이터
- 바디 : 실제 데이터

- HTTP 응답 구성 요소 예시
[Status Line]
HTTP/1.1 200 OK

[Headers]
Content-Type: application/json
Content-Length: 27
...

(빈 줄)

[Body]
{"message":"hello world"}
"""

from pydantic import BaseModel

# request model
class Item(BaseModel) :
    name: str
    description: str
    price: float
    tax: float | None = None

# Pydantic model for response data
class ItemResp(BaseModel):
    name: str
    description: str
    price_with_tax: float


# response_model 사용 시, status_code는 데코레이터에서 선언하는 것을 권장 (Response 객체를 직접 반환하는 경우 return에 작성)
# FastAPI가 return 값을 response_model 기준으로 검증 및 직렬화하여 응답 생성
@app.post('/create_item', response_model = ItemResp, status_code = status.HTTP_201_CREATED)
async def create_item_model(item: Item) :
    if item.tax :
        price_with_tax = item.price + item.tax
    else :
        price_with_tax = item.price
    
    item_resp = ItemResp(name = item.name,
                        description = item.description,
                        price_with_tax = price_with_tax)
    
    return item_resp    # 최종 반환 값이 response_model과 일치해야함
