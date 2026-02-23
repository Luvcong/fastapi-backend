from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool, NullPool
from dotenv import load_dotenv
import os

# database connection url
load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

# engine 생성
# 1) default : connection pool 사용
# engine = create_engine(DATABASE_CONN)

# 2) Connection Pool 옵션 사용
engine = create_engine(DATABASE_CONN, 
                       poolclass = QueuePool, # Connection Pool 사용
                       #poolclass = NullPool, # Connection Pool 사용하지 않음
                       pool_size = 10,        # 생성할 수 있는 최대 Connection Pool 개수
                       max_overflow = 2       # pool_size까지 다 사용한 뒤에 생성할 수 있는 마지막 Connection Pool 개수
                       )

print('#### engine created!')

# connection pool close 함수
def direct_execute_sleep(is_close: bool = False) :
    # connection pool 생성
    conn = engine.connect()
    query = 'select sleep(5)' # 5초 대기
    result = conn.execute(text(query))
    
    # 반환
    result.close()

    # is_close가 True인 경우에만 connection close()
    if is_close :
        conn.close()
        print('conn closed')

# connection pool 반복 사용 테스트
for i in range(10) :
    print('loop index : ', i)
    direct_execute_sleep(is_close = True)

print('end of loop!')

"""
select * from sys.session where db = 'blog_db' order by conn_id;

- workbench에서 해당 쿼리로 모니터링 확인해보면,
반복 횟수만큼 connection이 생성되지 않고 처음 생성된 connection을 계속해서 사용하는 것을 확인할 수 있음
(loop index : 1, 2, 3... 진행되지만 conn_id는 처음 생성된 값 그대로)

- connection close를 하지 않는 경우 계속해서 connection이 생성되므로 pool_size 등의 제한을 걸어주는게 좋음
"""