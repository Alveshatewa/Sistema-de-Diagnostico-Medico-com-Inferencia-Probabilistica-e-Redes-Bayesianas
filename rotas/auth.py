from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from model import Usuario
from schemas import UsuarioCreate, UsuarioOut, Token
from auth import get_db, gerar_hash_senha, criar_token, autenticar_usuario

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UsuarioOut)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed = gerar_hash_senha(user.senha)
    novo = Usuario(nome=user.nome, email=user.email, senha=hashed)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    access_token = criar_token({"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}