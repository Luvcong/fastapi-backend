from sqlalchemy import create_engine, Connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from contextlib import contextmanager
from fastapi import status
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os

# database connection URL
load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

engine = create_engine(DATABASE_CONN, #echo=True,
                       poolclass=QueuePool,
                       #poolclass=NullPool, # Connection Pool 사용하지 않음. 
                       pool_size=10,
                       max_overflow=0,
                       pool_recycle=300)

def direct_get_conn() :
    conn = None
    try :
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')

# @contextmanager # Depends가 이미 contextmanager를 가지고 있기 때문에 여기서는 작성 x
def context_get_conn() :
    conn = None
    try :
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e :
        print(e)
        raise HTTPException(status_code = status.HTTP_503_SERVICE_UNAVAILABLE, detail = '요청하신 서비스가 잠시 내부적으로 문제가 발생했습니다.')
    finally :
        if conn :
            conn.close()