#!/usr/bin/env bash
# Script de inicialização do backend no Render
# Garante que o Python encontre o módulo 'app' dentro da pasta backend
set -e
cd backend
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"

