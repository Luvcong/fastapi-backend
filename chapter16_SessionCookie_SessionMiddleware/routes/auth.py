from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from sqlalchemy import Connection
from passlib.context import CryptContext
from pydantic import EmailStr
from db.database import context_get_conn
from services import auth_svc

# router 생성
router = APIRouter(prefix='/auth', tags=['auth'])

# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory='templates')

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

def get_hashed_password(password : str) :
    return pwd_context.hash(password)

def verfify_password(password : str, hashed_password : str) :
    return pwd_context.verify(password, hashed_password)

@router.get('/register')
async def register_user_ui(request : Request) :
    return  templates.TemplateResponse(
        request = request,
        name = 'register_user.html',
        context = {}
    )

@router.post('/register')
async def register_user(name : str = Form(min_length = 2, max_length = 100),
                        email : EmailStr = Form(...),
                        password : str = Form(min_length = 2, max_length =30),
                        conn : Connection = Depends(context_get_conn)) :
    
    user = await auth_svc.get_user_by_email(conn = conn, email = email)
    if user is not None :
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '해당 Email은 이미 등록되어 있습니다.')

    hashed_password = get_hashed_password(password)
    await auth_svc.register_user(conn = conn, name = name, email = email, hashed_password = hashed_password)
    return RedirectResponse('/blogs', status_code = status.HTTP_302_FOUND)


@router.get('/login')
async def login_user_ui(request : Request) :
    return  templates.TemplateResponse(
        request = request,
        name = 'login.html',
        context = {}
    )


@router.post('/login')
async def login(email : str = Form(...),
                password : str = Form(min_length = 2, max_length = 30),
                conn : Connection = Depends(context_get_conn)) :
    # email 중복 체크
    user = await auth_svc.get_password_by_email(conn = conn, email = email)
    if user is None :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = '해당 이메일 사용자는 존재하지 않습니다.')
    
    is_correct_pw = verfify_password(password = password, hashed_password = user.hashed_password)

    if not is_correct_pw :
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = '로그인 입력 정보가 일치하지 않습니다.')
    
    return RedirectResponse('/blogs', status_code = status.HTTP_302_FOUND)