"""
Entry point para o Render — importa o app do backend.
Permite rodar: uvicorn main:app --host 0.0.0.0 --port $PORT
diretamente da raiz do repositório.
"""
import sys
import os

# Adiciona a pasta backend ao path para que 'app' seja encontrado
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.main import app  # noqa: F401, E402

