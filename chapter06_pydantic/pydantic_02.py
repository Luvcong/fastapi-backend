from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated
import json

class Address(BaseModel) :
    street : str
    city : str
    country : str

class User(BaseModel) :
    # 문자열 -> 숫자값 자동 파싱을 원하지 않는 경우 strict 모드 설정 필요
    # ConfigDict(strict = True) : 모델 전체 적용
    # model_config = ConfigDict(strict = True)

    id : int
    name : str
    email : str
    addresses : List[Address]
    # age : int | None = None
    
    # 개별 속성에 strict 모드 설정을 하려는 경우 Field or Annotated 이용 / None 적용 시 Optional
    # 1) Feild 이용
    # age : int = Field(None, strict = True)
    # 2) Annotated 이용
    # age : Annotated[int, Strict()] = None

# Pydantic Model 객체화 시 자동으로 검증 수행 수행하고, 검증 오류 시 ValidationError raise 
try:
    user = User(
        id='123',
        name="John Doe",
        email="john.doe@example.com",
        addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}],
        age="29"    # 기본적으로 문자열 값을 자동으로 int 형태로 파싱
    )
    print(user)
except ValidationError as e:
    print("validation error happened")
    print(e)