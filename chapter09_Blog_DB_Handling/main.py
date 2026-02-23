"""
REST(ful) API
: REST(Reprentational State Transfer) 아키텍처 스타일의 설계 원칙을 준수하는 API
: 웹 뿐만 아니라 네트워크 기반 분산 시스템 애플리케이션 구현 아키텍처 -> REST 기반으로 웹 표준화

주요 설계 원칙
- 동일한 리소스에 대한 균일한 인터페이스
- 클라이언트와 서버는 완전히 독립적
- 무상태 (Stateliess)
- 캐쉬 지원 가능
- 계층화된 시스템 아키텍처
- 온디맨드 코드 (사용자가 원하는 시점에 즉시 요청해서 이용하는 방식)
"""

from fastapi import FastAPI
from routes import blog

app = FastAPI()
app.include_router(blog.router)
