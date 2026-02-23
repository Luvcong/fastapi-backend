"""
- SQLAlchemy 설치
pip install SQLAlchemy

- MySQL Connection 설치
pip install mysql-connector-python
"""
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv, os

# 1) database connection URL 설정
load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

# 2) engine 생성
engine = create_engine(DATABASE_CONN, poolclass=QueuePool, pool_size=10, max_overflow=0)

try :
    # 3) Connection 얻기
    conn = engine.connect()

    # 4) SQL 선언 및 text로 감싸기
    query = 'select id, title from blog'
    stmt = text(query)

    # 5) SQL 호출하여 CorsorResult 반환
    result = conn.execute(stmt)

    rows = result.fetchall()   # 전체 조회 데이터 가져오기
    # result.fetchone     # 전체 조회 데이터에서 1건만 가져오기

    print('rows : ', rows)    # [(1, '테스트 title 1'), (2, '테스트 title 2'), (3, '테스트 title 3'), (4, '테스트 title 4')]
    # 각 개별 원소는 Row Type으로 되어있으며, 리스트로 반환
    print(type(rows))       # <class 'list'>
    print(type(rows[0]))    # <class 'sqlalchmy.engine.row.Row'>
    
    print(rows[0].id, rows[0].title)    # key 접근 방식
    print(rows[0][0], rows[0][1])       # index 접근 방식
    
    # index 접근 방식이 key 접근 방식보다 속도가 조금 더 빠름
    # key로 접근하는 경우 _key_to_index 를 사용해서 해당 key의 index를 매핑 후 조회
    print(rows[0]._key_to_index)

    result.close()
except SQLAlchemyError as e :
    print(e)
finally :
    # 6) Connection 반환 (except가 발생하더라도 Connection 반환 필요)
    conn.close()