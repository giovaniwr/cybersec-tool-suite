FROM python:3.12-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY backend/ ./backend/

# Trabalha dentro da pasta backend (onde está o alembic.ini e o pacote app/)
WORKDIR /app/backend

EXPOSE 8000

# Em produção: roda migrations + servidor
# Em dev (docker-compose): o CMD é sobrescrito pelo command: no compose
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
