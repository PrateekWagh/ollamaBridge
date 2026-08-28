from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPrompt(BaseModel):
    prompt:str
class ChatResponse(BaseModel):
    reply:str


class UserSignUp(BaseModel):
    email:EmailStr
    password:str
    confirm_password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class TokenData(BaseModel):
    userId:str