from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')
 
engine = create_engine(DATABASE_CONN,
                       poolclass = QueuePool,
                       pool_size = 10,
                       max_overflow = 0
                       )

# 1) default
# def direct_get_conn() :
#     try :
#         conn = engine.connect()
#         return conn
#     except SQLAlchemyError as e :
#         print(e)
#         raise e

# 2) with절 사용 (generator로 반환되므로 비권장)
# def direct_get_conn() :
#     try :
#         with engine.connect() as conn :
#             yield conn  # generator type으로 반환 (호출자가 next()를 사용해서 generator를 꺼내주어야 함)
#     except SQLAlchemyError as e :
#         print(e)
#         raise e

# 3) context 사용 (권장)
@contextmanager
def direct_get_conn() :
    try :
        conn = engine.connect()
        yield conn
    except SQLAlchemyError as e :
        print(e)
        raise e
    finally :
        conn.close()