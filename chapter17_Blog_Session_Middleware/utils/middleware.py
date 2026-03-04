from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# 모든 request가 미들웨어 함수를 수행하기 때문에 간단한 로직만 작성해야 함

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
