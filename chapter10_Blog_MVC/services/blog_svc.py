from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import BlogData
from utils import util
from typing import List


# 블로그 데이터 전체 조회
def get_all_blogs(conn : Connection) -> List:
    try :
        query = 'select id, title, author, content, image_loc, modified_dt from blog'
        result = conn.execute(text(query))

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
            conn.close()

# 블로그 데이터 단건 조회
def get_blog_by_id(conn : Connection, id: int) :
    try :
        # query = f'select id, title, author, content, image_loc, modified_dt from blog where id = {id}'
        query = f'select id, title, author, content, image_loc, modified_dt from blog where id = :id'   # bind variable 사용

        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)

        # 한 건도 없는 경우
        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')

        row = result.fetchone()
        blog = BlogData(id=row[0], title=row[1], author=row[2], content=(row[3]), image_loc=row[4], modified_dt=row[5])
        
        result.close()
        return blog
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')

# 블로그 글 신규 생성
def create_blog(conn : Connection, title : str, author : str, content : str) :
    try :
        query = f'insert into blog(title, author, content, modified_dt) values ("{title}", "{author}", "{content}", now())'
        conn.execute(text(query))
        conn.commit()
        # return True
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = '요청 데이터가 제대로 전달되지 않았습니다.')

# 블로그 게시글 수정
def update_blog(conn : Connection, id : int, title : str, author : str, content : str) :
    try :
        query = f'update blog set title = :title, author = :author, content = :content where id = :id'
        bind_stmt = text(query).bindparams(id = id, title = title, author = author, content = content)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        conn.commit()
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'요청 데이터가 제대로 전달되지 않았습니다.')

# 블로그 게시글 삭제
def delete_blog(conn : Connection, id : int) :
    try :
        query = f'delete from blog where id = :id'
        bind_stmt = text(query).bindparams(id = id)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0 :
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'해당 ID {id}는(은) 존재하지 않습니다.')
        
        conn.commit()
    except SQLAlchemyError as e :
        print(e)
        conn.rollback()
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = f'요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')