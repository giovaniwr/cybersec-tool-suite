"""
Entry point para o Render — importa o app do backend.
Permite rodar: uvicorn main:app --host 0.0.0.0 --port $PORT
diretamente da raiz do repositório.
"""
import sys
import os
import traceback

# Adiciona a pasta backend ao path para que 'app' seja encontrado
_backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if _backend_path not in sys.path:
    sys.path.insert(0, _backend_path)

# Garante que o diretório de trabalho aponte para backend
os.chdir(_backend_path)

print(f"[startup] Python {sys.version}", flush=True)
print(f"[startup] sys.path: {sys.path[:3]}", flush=True)
print(f"[startup] cwd: {os.getcwd()}", flush=True)

try:
    from app.main import app  # noqa: F401
    print("[startup] app importado com sucesso", flush=True)
except Exception as e:
    print(f"[startup] ERRO ao importar app: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
