'''
[ MySQL Async DB Driver ]
pymysql(Driver) + aiomysql(pymysql의 Async 처리 지원)
-> aiomysql은 pymysql 기반에서 동작하며, native DB Driver의 Async 처리와 Connection Pooling 기능 지원

[ SQLAlchmy에서 Async DB 처리 구문]
1) create_async_engine()으로 AsyncEngine 객체 생성
2) connect()를 await로 호출
3) execute()를 await로 호출
4) CursorReesult의 fetch()는 async로 수행할 수 없음
5) commit(), rollback()을 await로 호출
6) close()를 await로 호출

pip install mysql
pip install aiomysql
pip install greenlet
'''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import blog
from contextlib import asynccontextmanager
from db.database import engine

# lifespan : FastAPI가 종료될 때 비동기 데이터베이스 엔진이나 연결 풀과 같은 자원을 안전하게 해제하고 정리하기 위해 사용
@asynccontextmanager
async def lifespan(app : FastAPI) :
    # FastAPI 인스턴스 기동 시, 필요한 작업 수행
    print('Starting up...')
    yield

    # FastAPI 인스턴스 종료 시, 필요한 작업 수행
    print('shutting up...')
    await engine.dispose()

app = FastAPI(lifespan = lifespan)
app.mount('/static', StaticFiles(directory = 'static'), name = 'static')
app.include_router(blog.router)