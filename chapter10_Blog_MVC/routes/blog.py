from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Connection
from db.database import context_get_conn
from services import blog_svc
from utils import util


# router 생성
router = APIRouter(prefix='/blogs', tags=['blogs'])

# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory='templates')

# 블로그 데이터 전체 조회
@router.get('/')
def get_all_blogs(request : Request, conn: Connection = Depends(context_get_conn)) :
    all_blogs = blog_svc.get_all_blogs(conn = conn)

    return templates.TemplateResponse(
        request = request,
        name = 'index.html',
        context = {'all_blogs': all_blogs})

# 블로그 데이터 단건 조회
@router.get('/show/{id}')
def get_blog_by_id(request: Request, id: int, conn : Connection = Depends(context_get_conn)) :
    blog = blog_svc.get_blog_by_id(conn, id)
    blog.content = util.newline_to_br(blog.content)

    return templates.TemplateResponse(
        request = request,
        name = 'show_blog.html',
        context = {'blog' : blog})

# 블로그 게시글 신규 생성 템플릿 양식 조회
@router.get('/new')
def create_blog_ui(request: Request) :
    return templates.TemplateResponse(
        request = request,
        name = 'new_blog.html',
        context = {}    # 전달 값이 없는 경우 빈 dict 객체 전달
    )

# 블로그 게시글 신규 생성
@router.post('/new')
def create_blog(request : Request
               , title = Form(min_length=2, max_length=200)
               , author = Form(max_length=100)
               , content = Form(min_length=2, max_length=4000)
               , conn : Connection = Depends(context_get_conn)) :
    blog_svc.create_blog(conn = conn, title = title, author = author, content = content)
    return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)

# 블로그 게시글 수정 템플릿 양식 조회
@router.get('/modify/{id}')
def update_blog_ui(request : Request, id : int, conn = Depends(context_get_conn)) :
    blog = blog_svc.get_blog_by_id(conn = conn, id = id)

    return templates.TemplateResponse(
        request = request,
        name = 'modify_blog.html',
        context = {'blog': blog}
    )

# 블로그 게시글 수정
@router.post('/modify/{id}')
def update_blog(request : Request
                , id : int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn : Connection = Depends(context_get_conn)) :
    
    blog_svc.update_blog(conn = conn, id = id, title = title, author = author, content = content)
    return RedirectResponse(f'/blogs/show/{id}', status_code=status.HTTP_302_FOUND)

# 블로그 게시글 삭제
@router.post('/delete/{id}')
def delete_blog(request: Request, id: int, conn = Depends(context_get_conn)) :
    blog_svc.delete_blog(conn = conn, id = id)
    return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)