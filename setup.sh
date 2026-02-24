#!/usr/bin/env bash
# setup.sh — Instala dependências e inicia os dois servidores

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║      CyberSec Tool Suite — Setup         ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── Backend ─────────────────────────────────────
echo "▶ Configurando backend Python..."

VENV_DIR="/tmp/cybersec-venv"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
  echo "  ✅ Virtualenv criado em $VENV_DIR."
fi

source "$VENV_DIR/bin/activate"
pip install -r "$BACKEND_DIR/requirements.txt" -q
echo "  ✅ Dependências Python instaladas."

# ── Frontend ────────────────────────────────────
echo ""
echo "▶ Configurando frontend React..."
cd "$FRONTEND_DIR"
npm install --silent
echo "  ✅ Dependências Node instaladas."

# ── Iniciar servidores ──────────────────────────
echo ""
echo "▶ Iniciando servidores..."
echo ""

cd "$BACKEND_DIR"
source "$VENV_DIR/bin/activate"
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "  🐍 Backend rodando em http://localhost:8000 (PID $BACKEND_PID)"
echo "  📖 Swagger UI: http://localhost:8000/docs"

cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!
echo "  ⚛️  Frontend rodando em http://localhost:5173 (PID $FRONTEND_PID)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Acesse: http://localhost:5173            ║"
echo "║  Pressione Ctrl+C para encerrar.         ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Aguarda os processos
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servidores encerrados.'" INT TERM
wait

