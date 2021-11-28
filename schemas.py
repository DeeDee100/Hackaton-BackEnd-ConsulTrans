from pydantic import BaseModel, EmailStr
from typing import Optional


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
	sobrenome: Optional[str]
	especialidade: Optional[str]
	endereco_principal: Optional[str]
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