"""
bind variable (바인드 변수) : SQL에서 값을 직접 문자열로 삽입하지 않고, 자리표시자(placehloder)로 별도로 전달하는 파라미터
- SQL Injection 방지 (쿼리 구조와 데이터 분리)
- 성능 향상 (동잃판 SQL 템플릿 유지 -> Execution Plan 재사용 가능)
"""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime 
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

engine = create_engine(DATABASE_CONN)

try :
    conn = engine.connect()

    query = 'select id, title, author from blog where id = :id and author = :author and modified_dt < :modified_dt'
    stmt = text(query)
    bind_stmt = stmt.bindparams(id = 1, author = '둘리', modified_dt = datetime.now()) # bindparams(bind variable name)

    result = conn.execute(bind_stmt)
    rows = result.fetchall()
    print('rows : ', rows)

    result.close()
except SQLAlchemyError as e :
    print(e)
finally :
    conn.close()