from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine
from rotas import auth, diagnostico
import os
from dotenv import load_dotenv

load_dotenv()
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(diagnostico.router)
app.include_router(diagnostico.historico_router)