'''
1) Middleware : 클라이언트가 API를 요청할 때 미들웨어가 가로채서 선 처리 로직을 작성하여 API 최종 요청 진행
    - call_next : 선처리 작업 후 엔드포인트에 등록된 수행 함수를 호출하여 response 출력

    - FastAPI는 Custom Middleware를 생성하고 등록 가능
    - Pure ASGI Middleware를 구현하는 방법과 BaseHTTPMiddleware를 상속받아 구현하는 방법 존재
        - BaseHTTPMiddleware 클래스를 상속받고 dispatch()를 오버라이드 해주는 방법이 간단하여 사용 편리
    - dispatch() 메서드에서 필요한 선처리 작업 수행 -> call_next() 호출 -> API 함수 수행 후 Response 반환
'''

'''
2) CORS(Cross-Origin Resource Sharing)
: 서로 다른 Origin(출처)를 가진 Resource에 대한 접근을 허용할지에 대한 절차 및 정책
    - 클라이언트는 초기 접속 Origin(site)이 아닌, 다른 서드 파티 API 접근이나 리소스를 참조할 때
      브라우저와 해당 서버간 리소스 허용에 대한 메커니즘을 관리할 수 있도록 해줌
    - Origin은 URL에서 프로토콜, 도메인, 포트 중 하나라도 다르면 동일한 Origin이 아닌 것으로 간주

- CORS 동작 방식
    - 브라우저는 서버 접속 시 헤더에 Origin 정보를 기재하여 접속
    - 브라우저는 Header Origin에 처음 접속한 Origin 정보를 담아서 해당 서버로 전달
    - 리소스 접속을 요청 받은 서버에서는 브라우저가 보낸 Origin을 허용할 것인지 CORS 기반으로 판단하여
      허용 가능한 Origin에 대한 리스트를 응답으로 보내고, 브라우저에서 리스트 확인 후 해당 Origin이 있을 경우 Respone 출력
    
- CORS Preflight Reuqest
    : 브라우저는 먼저 CORS 요건에 맞는 요청인지 사전에 Preflight 요청으로 확인 후 본 요청 수행
    : Preflight request -> Preflight response -> request -> response
    
- CORS 설정
    1) allow_origins     : Cross origin request를 허용할 origin 리스트 (허용하려는 특정 도메인들)
    2) allow_orign_regex : 패턴 매칭 형태로 origin 서브 도메인 한꺼번에 허용
    3) allow_method      : 허용할 Request HTTP 메서드 유형 리스트
    4) allow_headers     : 허용할 Request Header 리스트 (클라이언트가 보낼 수 있는 Header)
    5) allow_credentials : 쿠키나 인증 정보를 포함한 요청을 허용할지에 대한 여부 / Default는 False
    6) expose_headers    : 브라우저가 접근 가능한 response haeder 리스트 (커스텀 토큰 헤더 등)
    7) max_age           : Preflight reques 정보의 Cache 유지 시간 (초)
'''


from fastapi import FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routes import blog
from utils.common import lifespan
from utils import exc_handler, middleware


app = FastAPI(lifespan = lifespan)

templates = Jinja2Templates(directory = 'templates')
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

app.add_middleware(CORSMiddleware, 
                   allow_origins = ['*'],
                   allow_methods = ['*'],
                   allow_headers = ['*'],
                   allow_credentials = True,
                   max_age = -1  # 시간 한도 갱신 없이 계속 적용
                   )
# app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)

app.include_router(blog.router)

app.add_exception_handler(RequestValidationError, exc_handler.custom_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_starlett_http_exception_handler)
