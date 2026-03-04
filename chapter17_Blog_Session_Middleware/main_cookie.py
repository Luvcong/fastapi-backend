'''
- Cookie : 개인화된 특정 정보를 브라우저와 서버 간에 유지하기 위해 만들어짐
           여러 개의 쿠키를 가질 수 있고, 개별 쿠키는 고유한 Key값으로 구분되어 Value값을 가짐 (하나에 최대 4kb까지 저장)
           보통 JSON 포맷으로 여러 개의 정보들을 저장하며, 최대 300개까지 쿠키를 저장하되 하나의 도메인당 최대 20개까지만 허용

  Client (Browser)                       Server
    |                                      |
    | (1) ---- HTTP Request ----------->   |  <-- 최초 접속
    |                                      |
    | (2) <--- HTTP Response + Cookie ---  |  <-- 'Set-Cookie' 헤더 포함
    |                                      |
    | (3) ---- HTTP Request + Cookie ----> |  <-- 저장된 쿠키를 헤더에 포함
    |                                      |
    | (4) <--- HTTP Response (+ Cookie) -- |  <-- 사용자 식별 후 응답
    |                                      |

- Cookie와 보안 관련
: 보안에 취약 -> 가급적 최소한의 정보를 저장하고, 민감 정보는 저장하지 않도록 구현
: 쿠키 정보를 암호화 할 수 있으나 서버에서 복호화하는데 시간이 소요 (요청을 보낼 떄마다 복호화 -> 서버 자원 낭비)
: 쿠키 정보가 수정/변조가 되었는지 확인이 가능하도록 Signed Key 기반으로 인코딩한 Signed Cookie가 주로 활용되나,
  Signed Cookie 역시 디코딩하여 원본 값 확인이 가능함
: └ 쿠키에 정보 자체를 담지 않고, 쿠키를 식별한 Cookie Id(Session Id)만 담는 방식으로 많이 사용 (상세 정보는 서버측에 저장)

- 도메인 구분에 따른 Cookie 유형
1) First Party Cookie : 사용자가 직접 URL을 입력하여 방문한 사이트에서 발행된 쿠키
    - 사용자 세션 관리 / 개인화 / 사용자 분석 등..
2) Third Party Cookie : 사용자가 직접 URL을 입력하여 방문한 사이트가 아닌, 다른 사이트에서 생성된 쿠키
    - 개인화 광고 / 소셜 미디어 통합 / 사용자 분석 솔루션 등..

- Cookie 주요 메타 파라미터
1) max_age   : 쿠키 유지 시간 (정수형 값, 초 단위)
2) expires   : 쿠키 유지 일시 (일자 + 시분초) -> datetime이나 문자열 등의 입력 값 사용 (Wed, 21 Oct 2024 07:29:00 GMT)
3) path      : 쿠키가 적용되는 서버의 path (해당 서버의 지정된 path에 접속 시 쿠키가 보내짐)
4) domain    : 쿠키가 유효한 도메인 (도메인 접속 시 쿠키가 보내짐)
5) secure    : True인 경우 HTTPS 접속 시에만 쿠키를 전송하도록 설정
6) httponly  : True인 경우 Javascript에서 쿠기 접근 차단 => XSS 공격 시, 악성 스크립트가 세션을 탈취하는 것을 방지
7) samesite  : CSRF 공격 방지
    - Strict : 다른 Origin에서 요청이 오면 쿠키를 보내지 않음 / 링크 클릭, GET Request도 차단
                    └ Origin : Scheme + Host + Port (예시 : https://example.com => https + example.com + 443)
    - Lax    : 기본적으로는 Strict와 같으나 사용자가 직접 링크를 클릭한 GET Request는 허용 (iframe, image, javascript call로는 보내지지 않음)
    - None   : Cross-Origin이라도 Cookie 전송 (단, 반드시 Secure=True 옵션과 함께 사용해야함 - 브라우저 정책)
'''

from fastapi import FastAPI, Request, Depends, HTTPException, Form, Response, Cookie, status
from fastapi.responses import HTMLResponse, RedirectResponse
import json

app = FastAPI()

# User Dict 생성 (테스트용)
users_db = {
    'test@test.com' : {
        'username' : 'test',
        'email' : 'test@test.com',
        'password' : 'test'
     }
}

# 쿠키 존재 여부 체크
# 1-1) Request 객체에서 cookie 정보 추출 
def get_logged_user(request : Request):
    cookies = request.cookies

    if 'my_cookie' in cookies.keys() :
        my_cookie_value = cookies['my_cookie']
        cookie_user = json.loads(my_cookie_value) # json.laods() : json -> dict 변환
        return cookie_user
    
    return None

# 1-2) Cookie 클래스를 이용하여 cookie 정보 추출
def get_logged_user_by_cookie_di(my_cookie = Cookie(None)):    # Key값의 이름을 cookie의 Key 이름으로 설정 
    if not my_cookie :
        return None
    
    cookie_user = json.loads(my_cookie)
    return cookie_user

# Home page
@app.get('/')
async def read_root(cookie_user: dict = Depends(get_logged_user)):
    if not cookie_user :
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'> 로그인 </a>", status_code = status.HTTP_401_UNAUTHORIZED)
    
    return HTMLResponse(f"환영합니다. {cookie_user['username']}님")

# Login UI page
@app.get('/login')
async def login_form():
    return HTMLResponse("""
        <form action="/login" method="post">
            Email: <input type="email" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

# Login
@app.post('/login')
async def login(email: str = Form(...), password: str = Form(...)):
    user_data = users_db[email] # dict
     
    # email, password 일치 검증
    if not user_data or user_data["password"] != password :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email과 Password가 일치하지 않습니다")

    # FastAPI의 Response 객체에 cookie 값 설정
    user_json = json.dumps({'username' : user_data['username'], 'email' : user_data['email']})

    # 반드시 return되는 response 객체에 set_cookie()를 호출해서 쿠키전달
    response = RedirectResponse(url = '/', status_code = status.HTTP_302_FOUND)

    response.set_cookie(key = 'my_cookie', value = user_json, httponly = True, max_age = 3600)
    response.set_cookie(key = 'my_another_cookie', value = user_json, httponly = True, max_age = 3600)
    # reponse.set_cookie... 여러개의 쿠키 생성 가능
    # max_age를 설정하지 않는 경우 Session Cookie로 생성되고, 브라우저 종료시 쿠키 삭제
    
    # 기본 httponly=True, samesite=Lax
    return response

@app.get('/user_profile')
async def user_profile(cookie_user: dict = Depends(get_logged_user_by_cookie_di)):
    if not cookie_user:
        return HTMLResponse("로그인 하지 않았습니다. 여기서 로그인 해주세요. <a href='/login'>로그인</a>.", status_code=status.HTTP_401_UNAUTHORIZED)
    
    return HTMLResponse(f"{cookie_user['username']}님의 email 주소는 {cookie_user['email']}")

@app.get('/logout')
async def logout(response: Response):
    # Cookie 삭제
    response = RedirectResponse(url='/', status_code = status.HTTP_302_FOUND)
    response.delete_cookie("my_cookie")
    response.delete_cookie("my_another_cookie")
    return response