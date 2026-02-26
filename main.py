"""
Entry point para o Render — importa o app do backend.
Permite rodar: uvicorn main:app --host 0.0.0.0 --port $PORT
diretamente da raiz do repositório.
"""
import sys
import os

# Adiciona a pasta backend ao path para que 'app' seja encontrado
_backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if _backend_path not in sys.path:
    sys.path.insert(0, _backend_path)

# Garante que o diretório de trabalho do alembic aponte para backend
os.chdir(_backend_path)

from app.main import app  # noqa: F401, E402

