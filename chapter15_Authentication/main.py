# 1) Bcrypt
# : Hashing 알고리즘이며, Encryption 알고리즘이 아님 (패스워드 + Salt + Cost Factor를 합쳐서 Hashing 값 생성)
# : Bcrypt는 패스워드와 같은 민감 정보를 복원할 수 없도록 안전하게 변환

# Bcrypt의 주요 요소
# └ Salt : Hashing이 적용되기 전에 패스워드에 추가되는 랜덤 값 (동일한 패스워드 값이라도 서로 다른 salt 값으로 인하여 해싱 적용 결과가 상이)

# Cost Factor : 해싱을 적용하는데 필요한 복잡도
# └ 높을수록 해싱에 시간이 오래 걸리므로, 패스워드 탈취가 어려움

# Bcrypt를 이용한 검증 방법
# 1) DB 등에 저장되어 있는 Hash된 패스워드 값에서 Salt와 CostFactor 추출
# 2) 사용자가 검증을 위해 입력한 패스워드 값을 추출된 Salt값과 Cost Factor를 이용하여 해싱 적용
# └ $2b$12$lPAsPufkDJm0tzGh2cDMPuD2YHuWcXyYHR.qDSOkIfMAtN1oihn4u
# 3) 해싱 적용 값이 DB에 저장된 해시 패스워드 값과 동일한지 비교하여 검증

'''
라이브러리 설치
pip install bcrypt
pip install passlib
'''

from fastapi import FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from routes import blog, auth
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
app.include_router(auth.router)

app.add_exception_handler(RequestValidationError, exc_handler.custom_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_starlett_http_exception_handler)