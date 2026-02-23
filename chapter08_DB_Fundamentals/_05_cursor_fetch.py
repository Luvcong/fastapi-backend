# fetchall()   : 조회된 모든 데이터 반환    (반환 타입 : list / 개별 원소 : row set)
# fetchone()   : 단일 원소 반환             (반환 타입 : row set)
# fetchmany(n) : n건만 조회하여 데이터 반환 (반환 타입 : list / 개별 원소 : row set)

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_CONN = os.getenv('DATABASE_CONN')

engine = create_engine(DATABASE_CONN)

try :
    conn = engine.connect()
    query = 'select id, title from blog'

    result = conn.execute(text(query))

    # 1) result_all()
    # result_all = result.fetchall()
    # print(f'result_all : {result_all} / type : {type(result_all)}')   # [(1, '테스트 title 1'), (2, '테스트 title 2'), (3, '테스트 title 3'), (4, '테스트 title 4')] / type : <class 'list'>

    # 2) result_one()
    # result_one = result.fetchone()
    # print(f'result_one : {result_one} / type : {type(result_one)}')   # (1, '테스트 title 1') / type : <class 'sqlalchemy.engine.row.Row'>

    # 3) result_many(n)
    # result_many = result.fetchmany(2)
    # print(f'result_many : {result_many} / type : {type(result_many)}')  # [(1, '테스트 title 1'), (2, '테스트 title 2')] / type : <class 'list'>

    # ** List Comprehension으로 row set을 개별 원소로 가지는 list 반환
    # rows = [row for row in result.fetchall()]
    # print('rows : ', rows)

    # 4) mappings() : 개별 row의 컬럼명을 key로 가지는 dict로 반환
    # row_dict = result.mappings().fetchall()
    # print('row_dict : ', row_dict)  # [{'id': 1, 'title': '테스트 title 1'}, {'id': 2, 'title': '테스트 title 2'}, {'id': 3, 'title': '테스트 title 3'}, {'id': 4, 'title': '테스트 title 4'}]

    # ** 코드 레벨에서 컬럼명 명시
    # todo - 오류 체크
    result_one = result.fetchone()
    rows = [(row.id, row.title) for row in result_one]
    print('rows : ', rows)
    

    result.close()
except SQLAlchemyError as e :
    print(e)
finally :
    conn.close()
    print('connection close finally')