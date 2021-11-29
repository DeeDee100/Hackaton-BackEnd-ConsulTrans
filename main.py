from fastapi import FastAPI
from database import models
from database.database import engine
from routes import login, users, feedbacks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


app.include_router(login.router)
app.include_router(users.router)
app.include_router(feedbacks.router)
 