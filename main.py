from fastapi import FastAPI
from database import models
from database.database import engine
from routes import login, users, feedbacks

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(login.router)
app.include_router(users.router)
app.include_router(feedbacks.router)
 