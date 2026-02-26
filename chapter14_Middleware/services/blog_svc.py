from fastapi import status, UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import BlogData
from utils import util
from typing import List
from dotenv import load_dotenv
import os, time
import aiofiles as aio
# from fastapi.exception_handlers import http_exception_handler   # default로 적용되어 따로 import 필요 없음 (http_exception_handler 구현부 참고)

load_dotenv()
UPLOAD_DIR = os.getenv('UPLOAD_DIR')

# 블로그 데이터 전체 조회
async def get_all_blogs(conn : Connection) -> List:
    try :
        query = '''
            select id
                 , title
                 , author
                 , content
                 , case when image_loc is null then '/static/default/blog_default.png' else image_loc end as image_loc
                 , modified_dt
             from blog
        '''
        result = await conn.execute(text(query))

        all_blogs = [BlogData(id = row.id,
                        title = row.title,
                        author = row.author,
                        content = util.truncate_text(row.content),
                        image_loc= row.image_loc,
                        modified_dt = row.modified_dt)
                        for row in result]     # rows = result.fetchall()
        
        result.close()
        return all_blogs
    except SQLAlchemyError as e :
        print('SQLAlchemy Error : ', e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')
    except Exception as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = '알 수 없는 이유로 서비스 오류가 발생했습니다.')
    finally :
        if conn :
            await conn.close()

# 블로그 데이터 단건 조회
async def get_blog_by_id(conn : Connection, id: int) :
    try :
        # query = f'select id, title, author, content, image_loc, modified_dt from blog where id = {id}'
        query = f'select id, title, author, content, image_loc, modified_dt from blog where id = :id'   # bind variable 사용

        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = await conn.execute(bind_stmt)

        # 한 건도 없는 경우
        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')

        row = result.fetchone()
        blog = BlogData(id=row[0], title=row[1], author=row[2], content=(row[3]), image_loc=row[4], modified_dt=row[5])

        if blog.image_loc is None :
            blog.image_loc = '/static/default/blog_default.png'
        
        result.close()
        return blog
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')

# 블로그 글 신규 생성
async def create_blog(conn : Connection, title : str, author : str, content : str, image_loc = None) :
    try :
        query = f'insert into blog(title, author, content, image_loc, modified_dt) values ("{title}", "{author}", "{content}", {util.none_to_null(image_loc, is_squote = True)} , now())'
        await conn.execute(text(query))
        await conn.commit()
        # return True
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '요청 데이터가 제대로 전달되지 않았습니다.')

# 블로그 파일 업로드
# pip install aiofiles
async def upload_file(author: str, imagefile: UploadFile) :
    try :
        # 디렉터리 경로 설정
        user_dir = f'{UPLOAD_DIR}/{author}/'

        # 디렉터리 존재 여부 체크
        if not os.path.exists(user_dir) :
            os.mkdir(user_dir)

        filename_only, ext = os.path.splitext(imagefile.filename)
        upload_filename = f'{filename_only}_{int(time.time())}{ext}'
        upload_image_loc = user_dir + upload_filename

        # 파일 읽고 쓰기
        async with aio.open(upload_image_loc, 'wb') as outfile :
            # while content := imagefile.file.read(1024) :    # 동기 방식
            while content := await imagefile.read(1024) :   # 비동기 방식
                await outfile.write(content)
        print('File Upload Success ! : ', upload_image_loc)
        
        # upload_image_loc : ./static.....
        return upload_image_loc[1:]
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = '이미지 파일이 제대로 업로드 되지 않았습니다.')

# 블로그 게시글 수정
async def update_blog(conn : Connection, id : int, title : str, author : str, content : str, image_loc : UploadFile) :
    try :
        query = f'''
            update blog
               set title = :title
                 , author = :author
                 , content = :content
                 , image_loc = :image_loc
             where id = :id
        '''
        bind_stmt = text(query).bindparams(id = id, title = title, author = author, content = content, image_loc = image_loc)
        result = await conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        await conn.commit()
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'요청 데이터가 제대로 전달되지 않았습니다.')

# 블로그 게시글 삭제
async def delete_blog(conn : Connection, id : int, image_loc : str = None) :
    try :
        query = f'delete from blog where id = :id'
        bind_stmt = text(query).bindparams(id = id)
        result = await conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        await conn.commit()

        if image_loc is not None :
            image_path = f'.{image_loc}'
            print('image_path : ', image_path)
            if os.path.exists(image_path) :
                os.remove(image_path)
        
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = f'요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')
    except Exception as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = '알 수 없는 이유로 오류가 발생했습니다.')