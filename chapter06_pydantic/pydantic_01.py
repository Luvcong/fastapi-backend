"""
pydantic : Data 저장 활용 및 Validation을 한번에 할 수 있는 라이브러리

1) 다양하고 빠른 Validation 수행
- 스키마/데이터 타입 검증 및 데이터 값에 대한 검증 수행
- 정규식 지원 및 다양한 내장 검증 로직 제공
- Core 검증 로직은 Rust로 제작되어 가장 빠른 파이썬 데이터 검증 라이브러리

2) Serialization 지원
- Pydantic 객체는 BaseModel을 상속한 Pydantic Model 클래스에 기반하여 생성

3) 다양한 Echo 시스템에서 활용되며, 문서화 시스템에서 지원
- FastAPI, HuggingFace, LangChain

Pydantic 사용 이유 ?
- 스키마 구조, Optional/Mandatory, 데이터 검증 등이 함께 포함 
    -> 데이터 값 자체만 담거나 유연한 구조체가 필요한 경우 사용하지 않는 것이 더 적합
    -> Client의 입력 데이터는 Pydantic으로, RDBMS의 데이터 추출을 담는 경우는 dataclass가 적합
"""

from pydantic import BaseModel
import json

# 일반 클래스와 Pydantic Model 비교
# Pydantic Model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None # Optional[int] = None

# 일반 클래스 선언
class UserClass:
    def __init__(self, id: int, name: str, email: str, age: int):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

    def get_info(self):
        return f"id: {self.id}, name: {self.name}"
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, email: {self.email}, age: {self.age}"

# 인스턴스 생성
userobj = UserClass(10, 'test_name', 'tname@example.com', 40)
print("userobj :", userobj, userobj.id)

# Pydantic Model 객체화
# User(10, 'test_name', 'tname@example.com', 40) 하지 않도록 유의 => 첫번째 인자가 정의해놓은 파라미터가 아니기 떄문
user = User(id=10, name="test_name", email="tname@example.com", age=40)
print("user :", user, user.id)

# 1) dict keyword argument(kwargs) -> Pydantic Model 객체화
user_from_dict = User(**{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40})

# 2) json 문자열 -> Pydantic Model 객체화
json_string = '{"id": 10, "name": "test_name", "email": "tname@example.com", "age": 40}'
json_dict = json.loads(json_string) # JSON -> dict 형태로 변환
print("json_dict type:", type(json_dict))

# 인스턴스 생성
user_from_json = User(**json_dict)
print("user_from_json:", user_from_json, user_from_json.id)

# ===================================================================
# Pydantic Model의 상속 (부모 필드 + 자식 필드 모두 포함)
class AdvancedUser(User):
    advanced_level: int

adv_user = AdvancedUser(id=10, name="test_name", email="tname@example.com", age=40, advanced_level=9)
print("adv_user:", adv_user)


# Nested JSON: JSON 객체 안에 또 다른 JSON 객체가 포함된 구조
# Nested JSON -> Pydantic Model 생성
class Address(BaseModel):
    street: str
    city: str

class UserNested(BaseModel):
    name: str
    age: int
    address: Address

# 1) JSON 문자열을 Pydantic 모델로 변환
json_string_nested = '{"name": "John Doe", "age": 30, "address": {"street": "123 Main St", "city": "Anytown"}}'

# JSON 문자열 -> Python dict (역직렬화)
json_dict_nested = json.loads(json_string_nested)

# dict -> Pydantic 모델 객체 (내부적으로 Address도 자동 생성)
user_nested_01 = UserNested(**json_dict_nested)
print("user_nested_01:", user_nested_01, user_nested_01.address, user_nested_01.address.city)

# 2) dict 형태를 address 필드에 전달 -> Pydantic이 자동으로 Address 모델로 변환
user_nested_02 = UserNested(name="test_name", age=40, address = {"street": "123 Main St", "city": "Anytown"})
print("user_nested_02:", user_nested_02, user_nested_02.address, user_nested_02.address.city)

# Pydantic 모델 -> Python dict (직렬화)
user_dump_01 = user.model_dump()        # Pydantic -> Python dict
print(user_dump_01, type(user_dump_01))

# Pydantic 모델 -> JSON 문자열 (직렬화)
user_dump_02 = user.model_dump_json()   # Pydantic -> json 문자열
print(user_dump_02, type(user_dump_02))