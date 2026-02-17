"""
Field() : Pydantic 모델에서 필드의 제약조건, 기본값, 메타데이터를 명시할 때 사용
- 유효성 검증 조건을 추가할 때 사용
- 기본 값 및 필수 값을 명시적으로 지정할 때 사용
- Field(...) : 필수 값이라는 의미
"""

from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated, Optional
import json

class User(BaseModel):
    # username: str = Field(description="The user's username", json_schema_extra={"example" : "john_doe"})
    # 위 코드처럼 작성해도 되지만, 명시적으로 필수 값인 것을 표현하기 위해 ...을 사용하는 것을 권장
    username: str = Field(..., description="The user's username", json_schema_extra={"example" : "john_doe"})
    email: str = Field(..., description="The user's email address", json_schema_extra={"example" : "john.doe@example.com"})
    password: str = Field(..., min_length=8, description="The user's password")
    age: Optional[int] = Field(None, ge=0, le=120, description="The user's age, must be between 0 and 120", json_schema_extra={"example" : 30})
    is_active: bool = Field(default=True, description="Is the user currently active?", json_schema_extra={"example" : True})

# Example usage
try:
    user = User(username="john_doe", email="john.doe@example.com", password="Secret123")
    print('user : ', user)
except ValidationError as e:
    print(e.json())

print('----------')

# https://docs.pydantic.dev/2.8/concepts/fields/

# gt - greater than (>)
# lt - less than (<)
# ge - greater than or equal to (>=)
# le - less than or equal to (<=)
# multiple_of - a multiple of the given number (배수 값)
# allow_inf_nan - allow 'inf', '-inf', 'nan' values
    # 1) inf  : 양의 무한대 (Infinity)
    # 2) -inf : 음의 무한대
    # 3) nan  : 정의 불가능한 수
 
class Foo(BaseModel):
    positive: int = Field(gt=0)
    non_negative: int = Field(ge=0)
    negative: int = Field(lt=0)
    non_positive: int = Field(le=0)
    even: int = Field(multiple_of=2)    # 2의 배수 / multiple_of = 3 : 3의 배수
    love_for_pydantic: float = Field(allow_inf_nan=True)

foo = Foo(
    positive = 1,
    non_negative = 0,
    negative = -1,
    non_positive = 0,
    even = 2,
    love_for_pydantic = float('inf'),
)
print(foo)
print('----------')

"""
min_length : 문자열 최소 길이
max_length : 문자열 최대 길이
pattern    : 문자열 정규 표현식
"""

class Foo(BaseModel):
    short: str = Field(min_length=3)
    long: str = Field(max_length=10)
    regex: str = Field(pattern=r'^\d*$')

foo = Foo(short='foo', long='foobarbaz', regex='123')
print(foo)
print('----------')

'''
max_digits     : Decimal 최대 숫자수 / 소수점 앞에 0만 있는 경우나, 소수점값의 맨 마지막 0는 포함하지 않음
decimal_places : 소수점 자리수 / 소수점값의 맨 마지막 0는 포함하지 않음
'''
from decimal import Decimal

class Foo(BaseModel) :
    precise : Decimal = Field(max_digits = 5, decimal_places = 2)

print('foo : ', Foo(precise=Decimal('123.45')))      # foo :  precise=Decimal('123.45')
print('foo : ', Foo(precise=Decimal('123.450')))     # foo :  precise=Decimal('123.450')
print('foo : ', Foo(precise=Decimal('123.4500000'))) # foo :  precise=Decimal('123.4500000') => 123.45로 체크되어 오류 발생 X
print('foo : ', Foo(precise=Decimal('0.4500000')))   # foo :  precise=Decimal('0.4500000')
# print('foo : ', Foo(precise=Decimal('23.456')))      # ValidationError : decimal_places가 2로 설정되어 있으므로 오류 발생