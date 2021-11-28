from enum import Enum
from typing import Optional
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response
from database.database import get_db
from sqlalchemy.orm.session import Session
from database import models


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


router = APIRouter(
	tags=['Users - Medicos']
)

class Myenum(str, Enum):
	cardiologia = 'Cardiologia'
	ginecologia = 'Ginecologia'
	psicologia = 'Psicologia'
	urologia = 'Urologia'
	cirurgiaoplastico = "Cirurgião plástico"
	clinicogeral = 'Clinico Geral'
	

class MedicoEntry(BaseModel):
	email: EmailStr
	password: str
	aceite: bool
	name: str
	sobrenome: str
	especialidade: str
	crm: str
	endereco_principal: str
	pcd: bool
	atendimento: str
	phone: int
	instagram: Optional[str]
	site: Optional[str]
	descript: str

class MedicoResponse(BaseModel):
	email: EmailStr
	aceite: bool
	name: str
	sobrenome: str
	especialidade: str
	crm: str
	endereco_principal: str
	pcd: bool
	atendimento: Optional[str]
	phone: int
	instagram: str
	site: str
	descript: str


class UpdateMedico(BaseModel):

	email: Optional[EmailStr]
	password: Optional[str]
	aceite: Optional[bool]
	name: Optional[str]
	sobrenome: Optional[str]
	especialidade: Optional[str]
	crm: Optional[str]
	endereco_principal: Optional[str]
	pcd: Optional[bool]
	atendimento: Optional[str]
	phone: Optional[int]
	instagram: Optional[str]
	site: Optional[str]
	descript: Optional[str]

#----------GET--------------
@router.get("/users")
def list_Users(db: Session = Depends(get_db)):
	users = db.query(models.Medicos).all()
	return {'data': users}


#--------------POST----------
@router.post("/users", status_code=201)
def create_Users(medico:MedicoEntry, db: Session = Depends(get_db)):
	found = False
	espec = medico.especialidade.lower().replace(" ", "")
	for keys in Myenum:
		if espec == keys.name:
			medico.especialidade = keys.value
			found = True

	if found != True:
		raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
									detail= {'message': 'Especialidade não encontrada'})


	psw_hashed = pwd_context.hash(medico.password)
	medico.password = psw_hashed
	new_medico = models.Medicos(**medico.dict())
	db.add(new_medico)
	try:
		db.commit()
		db.refresh(new_medico)
		return {'data': new_medico}
	except IntegrityError as err:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT,
							detail={'message': err.args})


#-----------GET-By-CRM-----
@router.get("/users/{crm}")
def get_by_crm(crm: str, db: Session= Depends(get_db)):
	requested = db.query(models.Medicos).filter(models.Medicos.crm == crm).first()
	if not requested:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					detail=f"Médico com crm: {crm} nao encontrado")
	med = (requested.__dict__)
	med.pop('_sa_instance_state')

	return {'Medico': med}

#----------DELETE--------

@router.delete("/users/{crm}", status_code=204)
def delete_medico(crm: str, db: Session= Depends(get_db)):
	requested = db.query(models.Medicos).filter(models.Medicos.crm == crm).first()

	if not requested:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					detail=f"Médico com crm: {crm} nao encontrado")

	db.delete(requested)
	db.commit()
	return Response(status_code=204)


#--------PATCH-----
@router.patch("/users/{crm}")
def update_User(crm: str, med: UpdateMedico, db: Session= Depends(get_db)):
	user_query = db.query(models.Medicos).filter(models.Medicos.crm == crm)
	user_exist = user_query.first()

	medico_entry = med.dict()

	for key in medico_entry:
		if medico_entry[key] != None:
				pass
		else:
			if key == 'name':
				medico_entry[key] = user_exist.name
			elif key == 'email':
				medico_entry[key] = user_exist.email
			elif key == 'estado':
				medico_entry[key] = user_exist.estado
			elif key == 'especialidade':
				medico_entry[key] = user_exist.especialidade
			elif key == 'endereco_opcional':
				medico_entry[key] = user_exist.endereco_opcional
			elif key == 'endereco_principal':
				medico_entry[key] = user_exist.endereco_principal
			elif key == 'pcd':
				medico_entry[key] = user_exist.pcd
			elif key == 'descript':
				medico_entry[key] = user_exist.descript
			elif key == 'phone':
				medico_entry[key] = user_exist.phone

	user_query.update(medico_entry, synchronize_session=False)
	db.commit()

	return {'message': ' updated'}
