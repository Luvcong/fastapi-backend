# Python 기반에서 RDBMS(Relational Database Management System) 사용

"""
Client App -> RDBMS
1) DB Connection 요청                    -> Client의 Connection을 위한 세션 생성 및 Connection 허용
2) 생성된 Connection을 이용하여 SQL 요청 -> SQL 검증 및 파싱하여 실행 계획 수립 (SQL 수행 후 결과를 반환할 수 있는 Cursor 생성)
3) Cursor에서 결과 데이터 fectch 요청    -> Cursor에 결과를 fetch한 후 Client에게 전송
4) Connection 종료 요청                  -> 해당 Connection의 세션을 종료 (세션이 점유한 자원도 같이 정리)

- 안정적인 DB 자원 관리를 위한 필수 Client 코드 구성 요소
    : Connection 관리
    : SQL 재활용
    : Cursor 정리

- SQLAlchemy
    : 자신만의 DB Client Driver를 가지고 있지 않음
    : 서로 다른 드라이버나 서로 다른 RDBMS 여도 공통의 DB 처리 API 기반으로 코드를 작성할 수 있게 해주는 역할
    : 많은 3-party 솔루션들이 SQLAlchemy를 지원함
"""


# Connection Pooling : Connection을 종료시키지 않고 다시 Pool에 반환하는 기법
# DataBase서버에서 Connection을 생성하는 작업은 DB 자원을 소모 (사용자/패스워드 검증, 사용자 권한 확인 및 설정, 세션 메모리 할당)
# 빈번한 OLTP 작업 요청마다 DB Connection을 생성하고 종료하는 작업은 많은 자원을 소모 -> 안정적인 DB 운영에 큰 영향
# └ 일정 수의 Connection을 미리 Pool에서 생성하고, 생성된 Coonection을 미리 가져다 SQL 수행하여 Connection 종료 없이 다시 Pool에 반환

"""
Connection Pool에서 생성된 자원 사용 후 다시 반납하기 위해서는 connection close()를 진행해주어야 함
- close()를 하더라도 Connection이 종료되는 것이 아니라 다시 Connection Pool로 돌아가서 대기 상태로 반환되는 것
- close()를 하지 않는 경우 사용한 Connection이 반환되지 않아 새로운 Connection을 생성해야돼서 자원 낭비

Connection Pooling 주요 파라미터
- poolclass : 지정하지 않는 경우 Connection Pool 사용 (QueuePool), None Pool을 지정하면 Connection Pool을 사용하지 않음
- pool_size : pool에서 유지되는 Connection 개수
- max_overflow : pool_size를 넘어서 추가 Connection이 필요할 경우 허용될 개수
- pool_recycle : Connection이 Pool내에서 유지되는 시간 (초) / 해당 시간이 넘어가면 접속 시, 새로운 Connection Pool로 생성
    └ 기본 값은 -1이며, 이 경수 수가 된다.
"""