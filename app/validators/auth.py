from pydantic import BaseModel, EmailStr, field_validator

class SignupBody(BaseModel):
    username: str
    email:EmailStr
    password:str
    
    @field_validator('password')
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 character long")
        return value

    @field_validator('username')
    def username_validator(cls,value):
        if len(value) < 3 :
            raise ValueError("Username must be at least 3 character long")
        return value

class SigninBody(BaseModel):
    email:EmailStr
    password:str
    
    @field_validator('password')
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 character long")
        return value
