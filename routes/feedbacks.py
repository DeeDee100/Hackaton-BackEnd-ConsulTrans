from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from database.database import get_db
import schemas
from database import models
from sqlalchemy.orm.session import Session

router = APIRouter(
	tags=["Avaliações"]
)

#---------GET---------------
@router.get("/feedback")
def avaliacao(db: Session= Depends(get_db)):
	users = db.query(models.Avaliacoes).all()
	return {"data": users}

#----------------------POST------------
@router.post("/feedback", status_code=201)
def criar_avaliacao(feedback: schemas.Feedback, db: Session= Depends(get_db)):
	existe = db.query(models.Avaliacoes).filter(models.Avaliacoes.crm == feedback.crm).first()
	if not existe:
		novo_feedback = models.Avaliacoes(crm= feedback.crm, total_feedback=feedback.avaliacao, num_feedback=1, media_feedback= feedback.avaliacao)
		db.add(novo_feedback)
		db.commit()
		db.refresh(novo_feedback)
		return novo_feedback
	else:
		existe.total_feedback += feedback.avaliacao
		existe.num_feedback += 1
		media = existe.total_feedback / existe.num_feedback
		existe.media_feedback = media
		db.commit()
		return existe

#-----------------GET By CRM---------
@router.get("/feedback/{crm}")
def get_by_crm(crm:str, db: Session= Depends(get_db)):
	requested = db.query(models.Avaliacoes).filter(models.Avaliacoes.crm == crm).first()
	existe = db.query(models.Medicos).filter(models.Medicos.crm == crm).first()

	if not existe:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Medico não Encontrado"})

	if not requested:
		raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
									detail= {'message': 'Avaliacoes nao encontrada'})
	
	return requested

