from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from utility import verify_password, passwordToHash
from db.connection import get_db
from . import oauth2
from sqlalchemy.orm.session import Session
from db.models import Users
router = APIRouter()
@router.post("/login")
def login(user_login_details:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    curr = db.query(Users).filter(Users.email == user_login_details.username).first()
    if not curr:
        raise HTTPException(status_code=404, detail="Not a registered user")

    if not verify_password(user_login_details.password, curr.hashed_password):
        raise HTTPException(status_code=400,detail="Invalid credentials")
    access_token = oauth2.create_token(data={"username":user_login_details.username})
    return {"access_token":access_token, "token_type":"Bearer"}