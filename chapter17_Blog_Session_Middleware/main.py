# Stateless한 Web의 특성 : 클라이언트가 개인화된 특정 정보를 서버와 지속적으로 유지할 수 없음 (Stgateles)
# └ 웹은 클라이언트의 HTML 리소스 요청에 대해서 해당 HTML을 빠르고 안정적으로 전달하는 목적으로 설계
# └ 서버는 Client 접속을 지속적으로 유지하지 않고, 리소스 전송이 완료되면 클라이언트의 연결을 종료시킴

# 웹이 엔터프라이즈 환경에서 사용되기 위해서 상태 관리가 필요해져 Cookie가 도입
# └ 사용자 특화된 정보를 브라우저에 저장하면서 브라우저와 서버간 상태관리가 가능해짐
# └ 최근에는 쿠키의 보안상의 이유로 브라우저는 특정 session key만 가지고 있고, 서버에서 사용자 특화 정보를 메모리/DB 등으로 저장, 관리하는 세션 방식이 널리 사용중

from fastapi import FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from routes import blog, auth
from utils.common import lifespan
from utils import exc_handler, middleware
from dotenv import load_dotenv
import os


app = FastAPI(lifespan = lifespan)

app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

app.add_middleware(CORSMiddleware, 
                   allow_origins = ['*'],
                   allow_methods = ['*'],
                   allow_headers = ['*'],
                   allow_credentials = True,
                   max_age = -1  # 시간 한도 갱신 없이 계속 적용
                   )

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app.add_middleware(SessionMiddleware, secret_key = SECRET_KEY, max_age = 3600)

# app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)

app.include_router(blog.router)
app.include_router(auth.router)

app.add_exception_handler(RequestValidationError, exc_handler.custom_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_starlett_http_exception_handler)