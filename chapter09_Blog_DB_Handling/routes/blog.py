from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from db.database import direct_get_conn, context_get_conn
from schemas.blog_schema import Blog, BlogData
from utils import util


# router 생성
router = APIRouter(prefix='/blogs', tags=['blogs'])

# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory='templates')

# 블로그 데이터 전체 조회
@router.get('/')
async def get_all_blogs(request : Request) :
    conn = None
    try :
        conn = direct_get_conn()
 
        query = 'select id, title, author, content, image_loc, modified_dt FROM blog'
        result = conn.execute(text(query))

        # rows = [Blog(id = row.id,
        #               title = row.title,
        #               author = row.author,
        #               content = row.content,
        #               image_loc= row.image_loc,
        #               modified_dt = row.modified_dt)
        #               for row in result]     # rows = result.fetchall()

        all_blogs = [BlogData(id = row.id,
                        title = row.title,
                        author = row.author,
                        content = util.truncate_text(row.content),
                        image_loc= row.image_loc,
                        modified_dt = row.modified_dt)
                        for row in result]     # rows = result.fetchall()
        
        result.close()
        return templates.TemplateResponse(request = request,
                                    name = 'index.html',
                                    context = {'all_blogs': all_blogs})
        # return rows
    except SQLAlchemyError as e :
        print('SQLAlchemy Error : ', e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')
    except Exception as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = '알 수 없는 이유로 서비스 오류가 발생했습니다.')
    finally :
        if conn :
            conn.close()

@router.get('/show/{id}')
async def get_blog_by_id(request: Request, id: int, conn : Connection = Depends(context_get_conn)) :
    try :
        conn = direct_get_conn()

        # query = f'select id, title, author, content, image_loc, modified_dt from blog where id = {id}'
        query = f'select id, title, author, content, image_loc, modified_dt from blog where id = :id'   # bind variable 사용

        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)

        # 한 건도 없는 경우
        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')

        row = result.fetchone()
        blog = BlogData(id=row[0], title=row[1], author=row[2], content=util.newline_to_br(row[3]), image_loc=row[4], modified_dt=row[5])
        
        result.close()
        # return blog
        return templates.TemplateResponse(
            request = request,
            name = 'show_blog.html',
            context = {'blog' : blog}
        )
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')
    # finally : # context_get_conn()에서 conn.close()를 진행하기 때문에 여기서 close를 진행하지 않아도 가능
    #     if conn :
    #         conn.close()

@router.get('/new')
def create_blog_ui(request: Request) :
    return templates.TemplateResponse(
        request = request,
        name = 'new_blog.html',
        context = {}    # 전달 값이 없는 경우 빈 dict 객체 전달
    )

@router.post('/new')
def create_blog(request : Request
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn : Connection = Depends(context_get_conn)) :
    try :
        query = f'insert into blog(title, author, content, modified_dt) values ("{title}", "{author}", "{content}", now())'
        conn.execute(text(query))
        conn.commit()   # insert이므로 commit() 진행 / SQLAlchemy의 경우 기본적으로 rollback을 가져가기 때문에 commit() 명시적으로 작성 필수

        return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)   # redirect시 get method로 전송
    except SQLAlchemyError as e :
        print(e)
        conn.rollback() # close() 될 때 rollback이 되므로 작성하지 않아도 무방
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '요청 데이터가 제대로 전달되지 않았습니다.')

@router.get('/modify/{id}')
def update_blog_ui(request : Request, id : int, conn = Depends(context_get_conn)) :
    try :
        query = f'select id, title, author, content from blog where id = :id'
        stmt = text(query)
        bind_stmt = stmt.bindparams(id = id)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        row = result.fetchone()

        return templates.TemplateResponse(
            request = request,
            name = 'modify_blog.html',
            context = {'id' : row.id, 'title' : row.title, 'author' : row.author, 'content' : row.content}
        )
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '요청 데이터가 제대로 전달되지 않았습니다.')

@router.post('/modify/{id}')
def update_blog(request : Request
                , id : int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn : Connection = Depends(context_get_conn)) :
    try :
        query = f'update blog set title = :title, author = :author, content = :content where id = :id'
        bind_stmt = text(query).bindparams(id = id, title = title, author = author, content = content)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        conn.commit()

        return RedirectResponse(f'/blogs/show/{id}', status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'요청 데이터가 제대로 전달되지 않았습니다.')

# Form에서 delete method가 실행되지 않아 post로만 사용 가능
@router.post('/delete/{id}')
def delete_blog(request: Request, id: int, conn = Depends(context_get_conn)) :
    try :
        query = f'delete from blog where id = :id'
        bind_stmt = text(query).bindparams(id = id)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        conn.commit()
        return RedirectResponse('/blogs', status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = f'요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')