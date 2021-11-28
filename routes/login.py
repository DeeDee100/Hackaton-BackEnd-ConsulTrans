from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from database.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import utilis
from OAuth2 import OAuth2
from database import models
from sqlalchemy.orm.session import Session

router = APIRouter(
	tags=['Login']
)

class Token(BaseModel):
	access_token: str
	token_type: str

class MedLogin(BaseModel):
	email:str
	password: str


@router.post("/login")
def login(credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
	user = db.query(models.Medicos).filter(models.Medicos.email == credentials.username).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					detail="invalid CPF")
	
	acess_token = OAuth2.create_token(data={"user_crm": user.crm})
	return {"access_token": acess_token, "token_type": "bearer"}