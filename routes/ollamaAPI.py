from time import timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from datetime import datetime as dt, timedelta, timezone
from db.connection import get_db
from models import UserPrompt, ChatResponse
import ollama
from sqlalchemy.orm.session import Session
from db import models
from routes.oauth2 import get_current_user
router = APIRouter()

GLOBAL_RATE_LIMIT = 5
WINDOW_TIME_IN_SEC = 60




@router.post("/chat")
def chat(user_prompt:UserPrompt, db:Session=Depends(get_db), user:str=Depends(get_current_user)):
    curr_user = db.query(models.Users).filter(models.Users.email==user).first()
    if not curr_user:
        raise HTTPException(status_code=404, detail="You are not a registered")
    curr_conv = db.query(models.ConversationTable).filter(models.Users.userId == models.ConversationTable.userId).first()
    now= dt.now(timezone.utc)
    if not curr_conv:
        curr_conv = models.ConversationTable(request_count=1, userId=curr_user.userId)
        db.add(curr_conv)
    elif (now-curr_conv.requested_At)>timedelta(seconds=WINDOW_TIME_IN_SEC):
        curr_conv.request_count = 1
        curr_conv.requested_At = now

    elif curr_conv.request_count>=5:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests, try again later")

    else:
       curr_conv.request_count+=1
    db.commit()
    db.refresh(curr_conv)
    try:
        # response = ollama.chat(model="llama3", messages=[{"role":"user", "content":user_prompt.prompt}])
        print()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ollama request failed")

    # return ChatResponse(reply=response["message"]["content"])