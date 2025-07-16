from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DiagnosticoCreate(BaseModel):
    sintomas: Dict[str, int]  

class DiagnosticoOut(BaseModel):
    id: int
    sintomas: Dict[str, int]
    resultado: Dict[str, float]
    data: datetime

    class Config:
        from_attributes = True