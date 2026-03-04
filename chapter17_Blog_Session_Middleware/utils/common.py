from fastapi import FastAPI
from db .database import engine
from contextlib import asynccontextmanager

# lifespan : FastAPI가 종료될 때 비동기 데이터베이스 엔진이나 연결 풀과 같은 자원을 안전하게 해제하고 정리하기 위해 사용
@asynccontextmanager
async def lifespan(app : FastAPI) :
    # FastAPI 인스턴스 기동 시, 필요한 작업 수행
    print('Starting up...')
    yield

    # FastAPI 인스턴스 종료 시, 필요한 작업 수행
    print('shutting up...')
    await engine.dispose()