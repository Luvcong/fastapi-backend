# 1) FastAPI import
from fastapi import FastAPI

# 2) FastAPI instance 생성
app = FastAPI()

# 3) Path 오퍼레이션 생성
# # Path는 도메인명(example.com)을 제외하고 / 로 시작하는 URL 부분
# 만약 url이 https://example.com/items/foo 라면 path는 /items/foo 
# Operation은 GET, POST, PUT/PATCH, DELETE등의 HTTP 메소드
@app.get("/"
         , summary='간단한 API'
         , tags=['Simple']
         , description='매우 간단한 API입니다.')
async def root():
    # 아래처럼 docstring으로 작성해도 swaggerUI의 description 역할을 함 (discription 파라미터가 우선순위)
    """
    이것은 간단한 API 입니다. 아래는 인자값입니다.

    - ** 인자값 1은 ~
    - ** 인자값 2는 ~
    """

    return {"message": "Hello World"}

# 4) FastAPI 실행
# uvicorn 모듈명(파일명):인스턴스명 --port=9091 --reload
# --reload : 코드 변경사항 저장 시, 자동 재시작 기능 활성화하는 옵션

# 5) 정상실행 확인
# localhost:9091

"""
- FastAPI : 웹 프레임워크, API를 쉽게 만들기 위한 도구 (요청을 어떻게 처리할지에 대한 코드 작성)
- └ ASGI 표준을 따르며 비동기 방식으로 요청을 처리 -> python 웹 프레임워크 중에서 최상의 속도 제공
- └ ASGI를 구현한 Uvicorn 서버 사용
- └ ASGI(Asynchronous Server Gateway Interface) : 비동기 처리와 실시간 통신(WebSocket)을 가능하게 하는 파이썬 웹 표준 (서버와 Python 웹 애플리케이션이 통신하는 규약)
- └ 내재화된 Pydantic 통합으로 데이터 검증과 직렬화, 파싱 과정을 안전하고 정밀하게 처리

[요약 정리]
- FastAPI : 요청 처리 로직
- Uvicorn : 실제로 포트를 열고 요청을 받는 서버
- ASGI : FastAPI와 Uvicorn 서버의 규격

- FastAPI 사용시, Content-type을 따로 지정해주지 않는 경우 JSON으로 직렬화하여 response가 지정됨

"""

# Swagger UI : API들을 브라우저 기반에서 편리하게 관리 및 문서화, 테스트 할 수 있는 기능 제공 (localhost:9091/docs)

# HTTP Request
# Method / URL / Protocal Version -> GET /index.html HTTP/1.1
# Headers
# Body(Optional)