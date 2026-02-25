'''
- RequestValidationError
: FastAPI는 Pydantic Model의 데이터 검증 실패 시 => ReqeustValidationError를 발생 시키며, 내부적으로 request_validation_exception_hanlder()를 이용하여 처리
: RequestValidationError는 Pydantic의 ValidationError를 Wrapping
'''
from fastapi import FastAPI, HTTPException, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from routes import blog
from utils.common import lifespan
from utils import exc_handler


app = FastAPI(lifespan = lifespan)

templates = Jinja2Templates(directory = 'templates')
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')

app.include_router(blog.router)

# 1) 사용자 정의 exception handler (JSONResponse)
# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request: Request, exc : HTTPException) :
#     return JSONResponse(status_code = exc.status_code, content = {'error' : '처리 중 에러가 발생했습니다.', 'detail' : exc.detail, 'code' : exc.status_code})

# 2) 사용자 정의 exception handler (Jinja2Templates)
# @app.exception_handler(HTTPException)
# async def custom_http_exception_handler(request: Request, exc : HTTPException) :
#     return templates.TemplateResponse(
#         request = request,
#         name = 'http_error.html',
#         context = {'status_code' : exc.status_code, 'title_messages' : '불편을 드려 죄송합니다.', 'detail' : exc.detail},
#         status_code = exc.status_code
#     )

# 3) 사용자 정의 exception handler (RequestValidation)
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request : Request, exc : RequestValidationError) :
#     return templates.TemplateResponse(
#         request = request,
#         name = 'validation_error.html',
#         context = {'status_code' : status.HTTP_402_PAYMENT_REQUIRED, 'title_messages' : '잘못된 값을 입력하였습니다.', 'detail' : exc.errors()},
#         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
#     )

# 3-1) 분리한 utils 파일에 있는 exception handler 사용 (RequestValidation)
app.add_exception_handler(RequestValidationError, exc_handler.custom_validation_exception_handler)

# 4) 사용자 정의 exception handler (StarletteHTTPException)
# python에서 HTTPException 사용 시, starlete exception 클래스를 사용하도록 권장하고 있음
# @app.exception_handler(StarletteHTTPException)
# async def custon_http_exception_handler(request: Request, exc : StarletteHTTPException) :
#     return JSONResponse(status_code = exc.status_code, content = {'error' : '처리 중 에러가 발생했습니다.', 'detail' : exc.detail, 'code' : exc.status_code})

# 4-1) 분리한 utils 파일에 있는 exception handler 사용 (StarlletHTTPException)
app.add_exception_handler(StarletteHTTPException, exc_handler.custom_starlett_http_exception_handler)

'''
1) exception_handler()     : 데코레이터 -> @app.exception_handler(ExceptionType)
2) add_exception_handler() : 함수 등록  -> app.add_exception_handler(ExceptionType, handler)
'''
