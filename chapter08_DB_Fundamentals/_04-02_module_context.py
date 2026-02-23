from sqlalchemy import Connection, text
from sqlalchemy.exc import SQLAlchemyError
from _04_database import direct_get_conn

def execute_query(conn: Connection) :
    query = 'select * from blog'
    result = conn.execute((text(query)))

    rows = result.fetchall()
    print('rows : ', rows)

    result.close()

def execute_sleep(conn: Connection) :
    query = 'select sleep(5)'
    result = conn.execute(text(query))
    result.close()

# 1) with절 사용 - generator type으로 반환된 경우
# for i in range(10) :
#     try :
#         conn_gen = direct_get_conn()    # connection pool 생성
#         print('#### before next()')
#         conn = next(conn_gen)   # next()를 사용하여 generator type 객체를 꺼내주어야 함
#         execute_sleep(conn)
#         print('loop index : ', i)
#     except SQLAlchemyError as e :
#         print(e)
#     finally :
#         conn.close()    # 호출한 쪽에서 connection pool 자원 반납
#         print('connection is closed inside finally')

# 2) context 사용
for i in range(10) :
    try :
        with direct_get_conn() as conn :
            execute_sleep(conn)
            print('loop index : ', i)
    except SQLAlchemyError as e :
        print(e)
        raise e

print('end of loop!')