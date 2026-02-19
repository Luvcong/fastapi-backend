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

for i in range(10) :
    try :
        conn = direct_get_conn()    # connection pool 생성
        execute_sleep(conn)
        print('loop index : ', i)
    except SQLAlchemyError as e :
        print(e)
    finally :
        conn.close()    # 호출자가 connection pool 자원 반납
        print('connection is closed inside finally')

print('end of loop!')