from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
import redis, uuid, json, logging

# 모든 request가 미들웨어 함수를 수행하기 때문에 간단한 로직만 작성해야 함

# Redis setup
redis_pool = redis.ConnectionPool(host = 'localhost', port = 6379, db = 0, max_connections = 10)
redis_client = redis.Redis(connection_pool = redis_pool)

class DummyMiddleware(BaseHTTPMiddleware) :
    async def dispatch(self, request : Request, call_next) :
        print('### request info : ', request.url, request.method)
        print('### request type : ', type(request))

        response = await call_next(request)
        return response
    
class MethodOverrideMiddleware(BaseHTTPMiddleware) :
    async def dispatch(self, request, call_next) :
        print(f'request url : {request.url}, query : {request.query_params}, method : {request.method}')
        if request.method == 'POST' :
            query = request.query_params
            if query :
                method_override = query['_method']  # 없다면 None
                if method_override :
                    method_override == method_override.upper()
                    if method_override in ('PUT', 'DELETE') :
                        request.scope['method'] = method_override

        response = await call_next(request)
        return response

class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, session_cookie: str = "session_redis_id", max_age: int = 3600):
        super().__init__(app)
        self.session_cookie = session_cookie
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        response = None

        # session_id cookie key로 session_id값을 가져와서 저장
        session_id = request.cookies.get(self.session_cookie)

        # 신규 session인지 구분
        initial_session_was_empty = True

        if self.max_age is None or self.max_age <= 0:
            response = await call_next(request)
            return response
        try:
            if session_id:
                session_data = redis_client.get(session_id) # session_id에 해당하는 session data 저장
                if session_data:    # request.state 객체에 새로운 session 객체 생성하여 session data 저장
                    request.state.session = json.loads(session_data)
                    redis_client.expire(session_id, self.max_age)
                    initial_session_was_empty = False
                else:   # session_id는 있으나 session data가 없는 경우 객체 초기화
                    request.state.session = {}
            else:
                session_id = str(uuid.uuid4())
                request.state.session = {}

            response = await call_next(request)
            if request.state.session:
                # logging.info("##### request.state.session:" + str(request.state.session))
                response.set_cookie(self.session_cookie, session_id, max_age=self.max_age, httponly=True)   # max_age 갱신
                redis_client.setex(session_id, self.max_age, json.dumps(request.state.session))
            else:
                # request.state.session가 비어있으나 initial_session_was_empty가 False인 경우
                # FastAPI 로직에서 request.state.session이 clear() 호출되어 삭제된 것을 의미
                # logout이므로 redis에서 해당 session_id 값을 삭제하고, 브라우저의 cookie도 삭제
                if not initial_session_was_empty:
                    # logging.info("##### redis value before deletion:" + str(redis_client.get(session_id)))
                    redis_client.delete(session_id)
                    # logging.info("##### redis value after deletion:" + str(redis_client.get(session_id)))
                    response.delete_cookie(self.session_cookie)
        except Exception as e:
            logging.critical("error in redis session middleware:" + str(e))
        
        return response