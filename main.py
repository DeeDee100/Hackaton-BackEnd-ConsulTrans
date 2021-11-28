from fastapi import FastAPI
from database import models
from database.database import engine
from routes import users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
	return {"Hello": "World!"}

app.include_router(users.router)
