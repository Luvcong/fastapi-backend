'''
Cookie 대비 Session 장점
1) 보안 안정성         : 상세 정보가 아닌, session_id 값만 가지고 있기 떄문에 민감 정보 유출 가능성이 낮음
2) 정보 용량 및 성능   : session_id 값으로만 요청/응답이 이루어지기 떄문에 네트워크 전송 부하가 작음 / But 데이터가 클수록 서버 메모리 용량이 커짐
3) 보안 및 데이터 통제 : session 저장소를 Restart하여 보안 및 데이터 통제 가능
4) 웹 프레임워크 사용 편의성 : 데이터 저장소와의 연계 및 인코딩/디코딩, Serialization이 보다 쉬움

Redis (Remote Dictionary Server) : RAM에 데이터 액세스를 빠르게 수행하는 Database(Cache) 시스템
    - 주로 Key=Value 형태로 다양한 데이터 타입들에 대해 엑세스/수정/삭제/저장 등 수행
    - 메모리의 데이터를 File로 Persistent 저장 가능
    - 마이크로 세컨드 단위의 빠른 처리 성능 (매우 빈번한 데이터 엑세스가 발생할 경우 자주 활용)
        - Caching : 데이터베이스의 부하를 감소키기기 위해 자주 사용되는 데이터 캐싱
        - 사용자 Session : 웹 애플리케이션의 사용자 세션 저장소로 사용
        - 실시간 분석 : 실시간으로 데이터 분석을 빠르게 수행 가능
'''
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

# app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)
app.add_middleware(middleware.RedisSessionMiddleware)

app.include_router(blog.router)
app.include_router(auth.router)

app.add_exception_handler(RequestValidationError, exc_handler.custom_validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_starlett_http_exception_handler)