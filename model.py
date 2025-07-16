from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    historico = relationship("Diagnostico", back_populates="usuario")


class Diagnostico(Base):
    __tablename__ = 'diagnosticos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    sintomas = Column(Text, nullable=False)  
    resultado = Column(Text, nullable=False) 
    data = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="historico")
