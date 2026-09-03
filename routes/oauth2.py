from jose import jwt, JWTError
from datetime import datetime as dt, timedelta
from models import TokenData
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
EXPIRE_IN = int(os.environ["EXPIRE_IN"])
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
