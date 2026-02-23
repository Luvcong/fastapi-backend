from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool, NullPool
from dotenv import load_dotenv
import os

# database connection URL
load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

engine = create_engine(DATABASE_CONN,
                       echo = True,     # SQLAlchemy가 내부적으로 어떻게 동작하는지 SQL문 출력
                       poolclass = QueuePool,
                       pool_size = 10,
                       max_overflow = 0
                       )

def context_execute_sleep() :
    # 1) default
    # conn = engine.connect()

    # 2) WITH절을 사용한 Connection Pool 반환
    with engine.connect() as conn :
        query = 'select sleep(5)'
        result = conn.execute(text(query))
        result.close()
        # conn.close()  # with절을 사용하는 경우 connection pool 자동 반환

for i in range(10) :
    print('loop index : ', i)
    context_execute_sleep()

print('end of loop!')