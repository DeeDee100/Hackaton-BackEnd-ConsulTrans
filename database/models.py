
from sqlalchemy.sql.schema import ForeignKey
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


class Medicos(Base):
	__tablename__ = "medicos"

	crm = Column(String, primary_key=True)
	name = Column(String, nullable=False)
	sobrenome = Column(String, nullable=False)
	email = Column(String, unique=True)
	password = Column(String, nullable=False)
	instagram = Column(String, nullable=True)
	especialidade = Column(String, nullable=False)
	endereco_principal = Column(String, nullable=False)
	site = Column(String, nullable=True)
	atendimento_online = Column(Boolean, nullable=False)
	atendimento_presencial = Column(Boolean, nullable=False)
	pcd = Column(Boolean, nullable= False)
	descript = Column(String, nullable=True)
	phone = Column(Integer, nullable=False)
	aceite = Column(Boolean, nullable= False)
	avaliacoes = relationship("Avaliacoes")

class Avaliacoes(Base):
	__tablename__ = "avaliacoes"

	id = Column(Integer, primary_key=True)
	crm = Column(String, ForeignKey('medicos.crm'))
	total_feedback = Column(Float, nullable=False)
	num_feedback = Column(Integer, nullable=False)
	media_feedback = Column(Float, nullable=False)
