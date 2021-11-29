from pydantic import BaseModel, EmailStr
from typing import Optional

#-------Modelos de dados usados ------

class MedicoEntry(BaseModel):
	email: EmailStr
	password: str
	aceite: bool
	name: str
	last_name: str
	specialty: str
	crm: str
	address: str
	pcd: bool
	atendimento_online: bool
	atendimento_presencial: bool
	phone: int
	instagram: Optional[str]
	site: Optional[str]
	descript: str


class UpdateMedico(BaseModel):

	email: Optional[EmailStr]
	password: Optional[str]
	name: Optional[str]
	last_name: Optional[str]
	specialty: Optional[str]
	address: Optional[str]
	pcd: Optional[bool]
	atendimento_online: Optional[bool]
	atendimento_presencial: Optional[bool]
	phone: Optional[int]
	instagram: Optional[str]
	site: Optional[str]
	descript: Optional[str]

class Token(BaseModel):
	access_token: str
	token_type: str

class Feedback(BaseModel):
	crm: str
	avaliacao: float