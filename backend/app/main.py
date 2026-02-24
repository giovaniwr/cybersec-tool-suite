from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import password
from app.database import create_tables
import app.models.senha_validador_model  # noqa: F401 — registra o model no metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executado na inicialização: cria tabelas se não existirem."""
    await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="CyberSec Tool Suite",
    description="Ferramentas de segurança cibernética",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(password.router)


@app.get("/api/tools")
async def get_tools():
    return [
        {
            "id": "password-validator",
            "name": "Validador de Senha",
            "description": "Verifique se sua senha é realmente segura com base nos padrões modernos de cibersegurança (NIST/OWASP).",
            "icon": "🔐",
            "route": "/password",
            "available": True,
        },
        {
            "id": "hash-checker",
            "name": "Verificador de Hash",
            "description": "Verifique se um arquivo foi adulterado comparando seu hash.",
            "icon": "🔍",
            "route": "/hash",
            "available": False,
        },
        {
            "id": "phishing-detector",
            "name": "Detector de Phishing",
            "description": "Analise URLs suspeitas para identificar tentativas de phishing.",
            "icon": "🎣",
            "route": "/phishing",
            "available": False,
        },
    ]


@app.get("/")
async def root():
    return {"message": "CyberSec Tool Suite API is running!"}

