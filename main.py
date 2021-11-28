from fastapi import FastAPI
from database import models
from database.database import engine
from routes import login, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(login.router)
app.include_router(users.router)
