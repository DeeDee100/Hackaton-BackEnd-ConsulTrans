from enum import Enum
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from database.database import get_db
from sqlalchemy.orm.session import Session
from database import models


router = APIRouter(
	tags=['Users']
)

#lista_especialidade = (
# 'ginecologia', 'endócrinologista',
# 'psicologia', 'Clinico Geral',
# 'Cirurgião plástico', 'Urologia')

class Myenum(str, Enum):
	cardiologia = 'Cardiologia'
	ginecologia = 'Ginecologia'
	psicologia = 'Psicologia'
	urologia = 'Urologia'
	cirurgiaoplastico = "Cirurgião plástico"
	clinicogeral = 'Clinico Geral'
	


class MedicoEntry(BaseModel):

	crm: str
	name: str
	email: str
	estado: str
	especialidade: str
	endereco_principal: str
	endereco_opcional: Optional[str]
	pcd: bool
	descript: str
	phone: int
	aceite: bool


@router.get("/users")
def list_Users(db: Session = Depends(get_db)):
	users = db.query(models.Medicos).all()
	return {'data': users}

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

	new_medico = models.Medicos(**medico.dict())
	db.add(new_medico)
	try:
		db.commit()
		db.refresh(new_medico)
		return {'data': new_medico}
	except IntegrityError as err:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT,
							detail={'message': err.args})

@router.get("/users/{crm}")
def get_by_crm(crm: str, db: Session= Depends(get_db)):
	requested = db.query(models.Medicos).filter(models.Medicos.crm == crm).first()
	if not requested:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
					detail=f"Médico com crm: {crm} nao encontrado")
	med = (requested.__dict__)
	med.pop('_sa_instance_state')

	return {'Medico': med}

