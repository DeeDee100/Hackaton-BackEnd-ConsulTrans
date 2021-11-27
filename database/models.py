from enum import Enum
from os import name

from sqlalchemy.sql.sqltypes import Boolean
from .database import Base
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship


class Medicos(Base):
	__tablename__ = "medicos"

	id = Column(Integer, primary_key=True, onupdate="CASCADE")
	crm = Column(String, unique=True)
	email = Column(String, unique=True)
	name = Column(String, nullable=False)
	estado = Column(String, nullable=True)
	especialidade = Column(String, nullable=False)
	endereco_principal = Column(String, nullable=False)
	endereco_opcional = Column(String, nullable=True)
	pcd = Column(Boolean, nullable= False)
	descript = Column(String, nullable=True)
	phone = Column(Integer, nullable=False)
	aceite = Column(Boolean, nullable= False)

