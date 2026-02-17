"""
비동기 함수 선언 시 : async 키워드 사용
비동기 함수 호출 시 : await 키워드 사용

- async def : 비동기 Event Loop를 적용
- def : ThreadPool을 적용
"""
from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

# async.. await...
async def long_running_task() :
    await asyncio.sleep(20) # time.sleep(20) # 동기 (20초동안 cpu가 아무것도 하지 못하고 대기)
    return {'status' : 'long_running task completed'}

# 비동기 방식으로 수행
@app.get('/task')
async def run_task() :
    return await long_running_task()

# task가 끝난 후 quick이 실행됨 (단일 동기 방식으로 수행됨)
@app.get('/task2')
async def run_task() :
    time.sleep(20)  # 동기
    return {'status' : 'long_running task completed'}

# 별도의 thread를 생성하여 수행되어 바로 quick이 실행됨 (병렬 방식)
@app.get('/task3')
def run_task() :
    time.sleep(20)
    return {'status' : 'long_running task completed'}

@app.get('/quick')
async def quick_response() :
    return {'status' : 'quick response'}

# [MultiProcess 방식으로 uvicron 실행]
# uvicorn main:app --workes=4 --port=9091
# : 4개의 ThreadPool 생성됨
# : 병렬로 실행되어 /task2의 단일 동기 방식임에도 불구하고 바로 quick이 실행됨

"""
FastAPI는 단독으로 만들어진 프레임워크가 아니라 크게 아래 3가지로 구성
1) Uvicoron : Python 기반의 ASGI 웹 서버 (특히 비동기 프로그래밍 수행에 초점)
    - JAVA의 tomcat 같은 역할
2) Starlette : ASGI 기반의 Lightwight, Framework/toolkit (웹 애플리케이션 구현을 위한 많은 기반 컴포넌트 제공)
    - Routing, middleware, Cookie 등 FastAPI에 사용되는 많은 기능들이 Starlette에 기반
3) FastAPI : 웹 Framework (Starlette의 기능에 다양한 편의 기능 추가)
    - 편리한 Request 처리, Dependency Injection, Pydantic 통합, 문서 자동화 등의 기능
"""