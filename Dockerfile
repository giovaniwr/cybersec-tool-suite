FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY backend/ ./backend/

# Copia o alembic.ini que fica na pasta backend
WORKDIR /app/backend

# Expõe a porta que o Render vai usar
EXPOSE 8000

# Roda migrations e inicia o servidor
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

