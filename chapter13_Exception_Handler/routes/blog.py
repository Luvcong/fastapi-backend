from fastapi import APIRouter, Request, Depends, status, Form, UploadFile, File
from fastapi.responses import RedirectResponse, JSONResponse
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
async  def get_all_blogs(request : Request, conn: Connection = Depends(context_get_conn)) :
    all_blogs = await blog_svc.get_all_blogs(conn = conn)

    return templates.TemplateResponse(
        request = request,
        name = 'index.html',
        context = {'all_blogs': all_blogs})

# 블로그 데이터 단건 조회
@router.get('/show/{id}')
async def get_blog_by_id(request: Request, id: int, conn : Connection = Depends(context_get_conn)) :
    blog = await blog_svc.get_blog_by_id(conn, id)
    blog.content = util.newline_to_br(blog.content)

    return templates.TemplateResponse(
        request = request,
        name = 'show_blog.html',
        context = {'blog' : blog})

# 블로그 게시글 신규 생성 템플릿 양식 조회
@router.get('/new')
async def create_blog_ui(request: Request) :
    return templates.TemplateResponse(
        request = request,
        name = 'new_blog.html',
        context = {}    # 전달 값이 없는 경우 빈 dict 객체 전달
    )

# 블로그 게시글 신규 생성
@router.post('/new')
async def create_blog(request : Request
               , title = Form(min_length=2, max_length=200)
               , author = Form(max_length=100)
               , content = Form(min_length=2, max_length=4000)
               , imagefile : UploadFile | None = File(None)
               , conn : Connection = Depends(context_get_conn)) :
    
    image_loc = None
    if len(imagefile.filename.strip()) > 0 :
        # 반드시 transactional 처리를 위해 upload_file()이 먼저 수행되어야 함
        image_loc = await blog_svc.upload_file(author = author, imagefile = imagefile)

    await blog_svc.create_blog(conn = conn, title = title, author = author, content = content, image_loc = image_loc)
    return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)

'''
- UploadFile : File에 대한 메타 정보를 갖고 있음
    - filename : 클라이언트가 업로드하는 파일명
    - content_type : MIME/미디어 타입 (image/jpeg 등)
    - file : python의 spooledTemporaryFile 객체
             OS의 임시 디렉터리에 동기 방식으로 파일을 Upload 할 시에는 SpooledTemporaryFile 객체의 file.read()를 호출
    
- 비동기 I/O 처리 수행 -> async로 선언되어 있으므로 await로 호출해야 함
'''

# 블로그 게시글 수정 템플릿 양식 조회
@router.get('/modify/{id}')
async def update_blog_ui(request : Request, id : int, conn = Depends(context_get_conn)) :
    blog = await blog_svc.get_blog_by_id(conn = conn, id = id)

    return templates.TemplateResponse(
        request = request,
        name = 'modify_blog.html',
        context = {'blog': blog}
    )

# 블로그 게시글 수정
@router.post('/modify/{id}')
async def update_blog(request : Request
                , id : int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , imagefile : UploadFile | None = File(None) 
                , conn : Connection = Depends(context_get_conn)) :
    image_loc = None
    if len(imagefile.filename.strip()) > 0 :
        image_loc = await blog_svc.upload_file(author = author, imagefile = imagefile)
        
    await blog_svc.update_blog(conn = conn, id = id, title = title, author = author, content = content, image_loc = image_loc)

    return RedirectResponse(f'/blogs/show/{id}', status_code=status.HTTP_302_FOUND)

# 블로그 게시글 삭제
@router.delete('/delete/{id}')
async def delete_blog(request: Request, id: int, conn = Depends(context_get_conn)) :
    blog = await blog_svc.get_blog_by_id(conn = conn, id = id)
    await blog_svc.delete_blog(conn = conn, id = id, image_loc = blog.image_loc)

    return JSONResponse(content = '게시글이 삭제되었습니다.', status_code = status.HTTP_200_OK)
    # return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)