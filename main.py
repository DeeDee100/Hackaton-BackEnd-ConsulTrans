from fastapi import FastAPI, Depends
from database import models
from database.database import engine, get_db
from sqlalchemy.orm.session import Session
from routes import users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
	return {"Hello": "World!"}

app.include_router(users.router)
