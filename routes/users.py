from enum import Enum
from typing import Optional
from passlib.context import CryptContext
from utilis import hash
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
import schemas
from sqlalchemy.exc import IntegrityError
from starlette.responses import Response
from database.database import get_db
from OAuth2.OAuth2 import current_User
from sqlalchemy.orm.session import Session
from database import models


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


router = APIRouter(
	tags=['Medicos']
)

class Myenum(str, Enum):
	cardiologia = 'Cardiologia'
	ginecologia = 'Ginecologia'
	psicologia = 'Psicologia'
	urologia = 'Urologia'
	cirurgiaoplastico = "Cirurgião plástico"
	clinicogeral = 'Clinico Geral'
	


#----------GET--------------
@router.get("/users")
def list_Users(db: Session = Depends(get_db)):
	users = db.query(models.Medicos).all()
	return {'data': users}


#--------------POST----------
@router.post("/users", status_code=201)
def create_Users(medico:schemas.MedicoEntry, db: Session = Depends(get_db)):
	found = False
	espec = medico.especialidade.lower().replace(" ", "")
	for keys in Myenum:
		if espec == keys.name:
			medico.especialidade = keys.value
			found = True

	if found != True:
		raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
									detail= {'message': 'Especialidade não encontrada'})

	psw_hashed = hash(medico.password)
	medico.password = psw_hashed
	new_medico = models.Medicos(**medico.dict())
	db.add(new_medico)
	try:
		db.commit()
		db.refresh(new_medico)
		return_med = medico.dict()
		return_med.pop('password')
		return {'data': return_med}
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

#---------------Get- By Especialidade -----------------
@router.get('/especialistas/{especialidade}')
def get_by_especialidade(espec:str, db: Session= Depends(get_db)):
	request = db.query(models.Medicos).filter(models.Medicos.especialidade == espec).all()
	return request

#----------DELETE------------

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
def update_User(crm: str, med: schemas.UpdateMedico, db: Session= Depends(get_db),
	current_user: int= Depends(current_User)):

	if current_user.crm != crm:
		return "crm diferente"
	
	user_query = db.query(models.Medicos).filter(models.Medicos.crm == crm)
	user_exist = user_query.first()

	medico_entry = med.dict()

	for key in medico_entry:
		if medico_entry[key] != None:
				if key == 'password':
					hashed = hash(medico_entry[key])
					medico_entry[key] = hashed
		else:
			if key == 'name':
				medico_entry[key] = user_exist.name
			if key == 'sobrenome':
				medico_entry[key] = user_exist.sobrenome
			elif key == 'email':
				medico_entry[key] = user_exist.email
			elif key == 'password':
				medico_entry[key] = user_exist.password
			elif key == 'instagram':
				medico_entry[key] = user_exist.instagram
			elif key == 'especialidade':
				medico_entry[key] = user_exist.especialidade
			elif key == 'site':
				medico_entry[key] = user_exist.site
			elif key == 'atendimento_presencial':
				medico_entry[key] = user_exist.atendimento_presencial
			elif key == 'atendimento_online':
				medico_entry[key] = user_exist.atendimento_online
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
