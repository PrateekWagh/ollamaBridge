from jose import jwt, JWTError
from datetime import datetime as dt, timedelta
from models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
EXPIRE_IN = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()
    expire_in=dt.now()+timedelta(minutes=EXPIRE_IN)
    to_encode.update({"exp":expire_in})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def validate_token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    except JWTError:
        raise credential_exception
    userId = payload.get("username")
    if userId is None:
        raise credential_exception
    tokenData = TokenData(userId=userId)
    return tokenData.userId



def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"www-authenticate":"Bearer"})
    return validate_token(token, credential_exception)
