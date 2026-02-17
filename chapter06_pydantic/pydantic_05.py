from pydantic import BaseModel, ValidationError, field_validator, model_validator

class User(BaseModel) :
    username : str
    password : str
    confirm_password : str

    @field_validator('username')
    def username_must_not_be_empty(cls, value: str) :
        if not value.strip() :
            raise ValueError('Username must not be empty')
        return value
    
    @field_validator('password')
    def password_must_be_strong(cls, value: str) :
        if len(value.strip()) < 8 :
            raise ValueError('Password must be at least 8 characters long')
        # if any ... : 하나라도 true가 있는 경우 true
        if not any(char.isdigit() for char in value) :
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value) :
            raise ValueError('Password must contain at least one letter')
        return value

    # Pydantic Ver2
    # @model_validator(mode='after')
    # def check_passwords_match(cls, values) :
    #     password = values.password
    #     confirm_password = values.confirm_password
    #     if password != confirm_password :
    #         raise ValueError('Password do not match')
    #     return values

    # Pydantic v2.12 부터 model_validator(mode='after')를 classmethod로 사용하는 방식이 deprecated
    # 현재는 동작하지만 경고 발생 : v3에서 제거될 예정으로 instance method로 작성 필요
    
    # Pydantic Ver3
    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
# 검증 테스트
try :
    user = User(username = 'jhee', password = 'password123', confirm_password = 'password123')
    print('user : ', user)
except ValidationError as e :
    print(e)