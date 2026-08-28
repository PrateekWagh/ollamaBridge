from fastapi import APIRouter, HTTPException, Depends
from  models import UserSignUp

from sqlalchemy.orm.session import Session
from db import connection, models
from utility import passwordToHash

router = APIRouter()


@router.post("/signUp")
def signUp(user:UserSignUp, db:Session=Depends(connection.get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Password and Confirm Password did not match!")
    user_exist = db.query(models.Users).filter(models.Users.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=404, detail="User already exist")
    new_user= models.Users(email=user.email, hashed_password=passwordToHash(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"SignUp successful"}
