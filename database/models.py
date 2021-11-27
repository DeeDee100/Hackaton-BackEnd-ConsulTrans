from enum import Enum
from os import name

from sqlalchemy.sql.sqltypes import Boolean
from .database import Base
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship


class Medicos(Base):
	__tablename__ = "medicos"

	id = Column(Integer, primary_key=True)
	crm = Column(String, unique=True)
	email = Column(String, unique=True)
	password = Column(String, nullable=False)
	name = Column(String, nullable=False)
	sobrenome = Column(String, nullable=False)
	instagram = Column(String, nullable=True)
	especialidade = Column(String, nullable=False)
	endereco_principal = Column(String, nullable=False)
	site = Column(String, nullable=False)
	atendimento = Column(String, nullable=False)
	pcd = Column(Boolean, nullable= False)
	descript = Column(String, nullable=True)
	phone = Column(Integer, nullable=False)
	aceite = Column(Boolean, nullable= False)

