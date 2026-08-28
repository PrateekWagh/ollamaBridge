from fastapi import FastAPI
from routes import user, auth, ollamaAPI
from db import connection
connection.Base.metadata.create_all(bind=connection.engine)


app = FastAPI()

@app.get("/")
def home():
    return "Welcome"
app.include_router(ollamaAPI.router)
app.include_router(user.router)
app.include_router(auth.router)