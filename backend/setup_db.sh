#!/usr/bin/env bash
# =============================================================================
# setup_db.sh — Configura o banco PostgreSQL para o CyberSec Tool Suite
# Uso: bash setup_db.sh
# =============================================================================
set -e

DB_NAME="cybersec_db"
DB_USER="postgres"
DB_PASS="postgres"

echo "🔧 Verificando PostgreSQL..."
if ! command -v psql &>/dev/null; then
  echo "❌ psql não encontrado. Instale com: sudo apt install postgresql"
  exit 1
fi

echo "🚀 Iniciando serviço PostgreSQL..."
sudo systemctl start postgresql 2>/dev/null || sudo systemctl start postgresql@16-main 2>/dev/null || true
sleep 2

echo "🗄️ Criando banco '$DB_NAME'..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1 \
  || sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"

echo "🔑 Configurando senha do usuário '$DB_USER'..."
sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "📦 Aplicando migrations (Alembic)..."
cd "$(dirname "$0")"
if [ -f ".venv/bin/alembic" ]; then
  .venv/bin/alembic upgrade head
else
  echo "⚠️  .venv não encontrado. Rode: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
fi

echo ""
echo "✅ Banco configurado com sucesso!"
echo "   Host: 127.0.0.1:5432"
echo "   Banco: $DB_NAME"
echo "   Usuário: $DB_USER"

