from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional

class BlogInput(BaseModel) :
    title : str = Field(..., min_length=2, max_length=200)
    author : str = Field(..., max_length=100) 
    content : str = Field(..., min_length=2, max_length=4000)
    image_loc : Optional[str] = Field(None, max_length=400)   # 코드 동일 (image_loc : str : None = Field(None, max_length=4000))

class Blog(BlogInput) :
    id: int
    modified_dt : datetime

# 1) pydantic 사용
# class BlogData(BaseModel) :
#     id : int
#     title: str
#     author: str
#     content: str
#     modified_at : datetime
#     image_lic : str | None = None

# 2) pydantic 검증조건 사용하지 않고 dataclass 사용
@ dataclass
class BlogData :
    id : int
    title: str
    author: str
    content: str
    modified_dt: datetime
    image_lic : str | None = None   # dataclass 데코레이터 사용시 None값으로 들어가는 필드를 맨 마지막에 기재 필수