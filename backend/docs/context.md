# 📦 Backend — Contexto de Desenvolvimento

> Use este arquivo como referência sempre que for desenvolver ou expandir o backend.
> Ele descreve a arquitetura, padrões adotados, contratos de API e guias de como adicionar novas funcionalidades.

---

## 🏗️ Stack & Tecnologias

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.12+ | Linguagem principal |
| FastAPI | 0.132+ | Framework web / API REST |
| Pydantic v2 | 2.12+ | Validação e serialização de dados |
| Pydantic-Settings | 2.13+ | Leitura de variáveis de ambiente (.env) |
| SQLAlchemy | 2.0+ | ORM assíncrono |
| asyncpg | 0.31+ | Driver PostgreSQL assíncrono |
| Alembic | 1.18+ | Migrations do banco de dados |
| psycopg2-binary | 2.9+ | Driver PostgreSQL síncrono (Alembic) |
| Uvicorn | 0.29+ | Servidor ASGI |

---

## 📁 Estrutura de Pastas

```
backend/
├── .env                          ← Variáveis de ambiente (NÃO versionar)
├── .env.example                  ← Modelo do .env para novos devs
├── requirements.txt
├── alembic.ini                   ← Config do Alembic (URL lida do .env)
├── setup_db.sh                   ← Script para criar banco e rodar migrations
├── alembic/
│   ├── env.py                    ← Config async do Alembic
│   └── versions/                 ← Arquivos de migration gerados
├── docs/
│   └── context.md                ← Este arquivo
└── app/
    ├── __init__.py
    ├── main.py                   ← Ponto de entrada FastAPI + lifespan
    ├── database.py               ← Engine, sessão e Base do SQLAlchemy
    ├── core/
    │   ├── __init__.py
    │   └── config.py             ← Settings (lê .env via pydantic-settings)
    ├── data/
    │   └── common_passwords.txt
    ├── models/
    │   ├── __init__.py
    │   ├── password_models.py         ← Schemas Pydantic request/response
    │   └── senha_validador_model.py   ← Model SQLAlchemy da tabela
    ├── repositories/
    │   ├── __init__.py
    │   └── senha_validador_repository.py  ← Acesso ao banco (queries)
    ├── routers/
    │   ├── __init__.py
    │   └── password.py           ← Endpoints da ferramenta de senha
    └── services/
        ├── __init__.py
        └── password_validator.py ← Lógica de validação (pura, sem DB)
```

---

## ⚙️ Como Rodar Localmente

```bash
cd backend

# 1. Criar e ativar venv
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# edite .env com suas credenciais do PostgreSQL

# 4. Criar banco e rodar migrations (primeira vez)
bash setup_db.sh

# 5. Iniciar o servidor
.venv/bin/uvicorn app.main:app --reload --port 8000
```

> O `lifespan` do FastAPI chama `create_tables()` automaticamente na inicialização,
> garantindo que a tabela exista mesmo sem rodar o Alembic manualmente.

API disponível em: `http://localhost:8000`
Swagger UI: `http://localhost:8000/docs`

---

## 🗄️ Banco de Dados — PostgreSQL

### Variáveis de Ambiente (`.env`)
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cybersec_db
ENVIRONMENT=development
SECRET_KEY=troque-esta-chave
```

### Tabela `senhas_validador`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | UUID (PK) | Identificador único gerado automaticamente |
| `created_at` | TIMESTAMPTZ | Data/hora UTC da captura (indexada) |
| `senha_capturada` | TEXT | Senha digitada pelo usuário |
| `ip_origem` | VARCHAR(45) | IP do cliente (IPv4 ou IPv6, indexado) |
| `user_agent` | TEXT | Navegador e SO do usuário |
| `score` | INTEGER | Força: 0 (muito fraca) a 5 (muito forte) |
| `strength_label` | VARCHAR(30) | Rótulo: Muito Fraca / Fraca / Razoável / Forte / Muito Forte |
| `entropy_bits` | FLOAT | Entropia estimada em bits |
| `is_common` | BOOLEAN | True se constar na lista de senhas comuns |
| `comprimento` | INTEGER | Número de caracteres |
| `tem_maiuscula` | BOOLEAN | Contém letra maiúscula |
| `tem_minuscula` | BOOLEAN | Contém letra minúscula |
| `tem_numero` | BOOLEAN | Contém número |
| `tem_especial` | BOOLEAN | Contém caractere especial |

### Migrations com Alembic

```bash
# Gerar nova migration após alterar um model
.venv/bin/alembic revision --autogenerate -m "descricao_da_mudanca"

# Aplicar migrations pendentes
.venv/bin/alembic upgrade head

# Ver histórico
.venv/bin/alembic history

# Reverter última migration
.venv/bin/alembic downgrade -1
```

### Arquitetura de Acesso ao Banco
```
Router (password.py)
  └── injeta AsyncSession via Depends(get_db)
        └── SenhaValidadorRepository(db)
              └── salvar() | listar() | total() | distribuicao_scores()
```

---

## 🔌 Configuração CORS

Em `app/main.py`:
```python
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
```

---

## 🗺️ Rotas Existentes

### `GET /`
Health check da API.

### `GET /api/tools`
Lista todas as ferramentas (disponíveis e em breve).

### `POST /api/password/analyze`
**Análise em tempo real** — valida a senha, **sem gravar no banco**.
Chamado pelo frontend a cada 400 ms enquanto o usuário digita.
- Body: `{ "password": "string" }`
- Resposta: `PasswordResponse`

### `POST /api/password/validate`
**Captura definitiva** — valida E **persiste no banco**.
Chamado pelo frontend após **3 segundos de inatividade** no campo de senha.
- Body: `{ "password": "string" }`
- Resposta: `PasswordResponse`
- Efeito colateral: INSERT em `senhas_validador` com IP, User-Agent e métricas

### `GET /api/password/stats`
Estatísticas agregadas: total de senhas analisadas e distribuição por score.

---

## 🧱 Padrões Arquiteturais

### Separação de Responsabilidades
| Camada | Pasta | Responsabilidade |
|---|---|---|
| Router | `routers/` | Define endpoints, recebe request, retorna response |
| Service | `services/` | Lógica de negócio pura (sem FastAPI, sem DB) |
| Repository | `repositories/` | Operações de banco (queries SQLAlchemy) |
| Model ORM | `models/*_model.py` | Definição da tabela (SQLAlchemy) |
| Schema | `models/*_models.py` | Contratos de API (Pydantic) |

### Nomenclatura
- Arquivos: `snake_case`
- Classes Pydantic/SQLAlchemy: `PascalCase`
- Funções e variáveis: `snake_case`
- Constantes: `_UPPER_SNAKE_CASE` (underscore inicial = privado ao módulo)

### Prefixo de Rota
`/api/<ferramenta>/<ação>` — ex: `/api/password/analyze`, `/api/hash/check`

---

## ➕ Como Adicionar uma Nova Ferramenta com Banco

1. **Model ORM** → `models/<ferramenta>_model.py` (herda de `Base`)
2. **Schema Pydantic** → `models/<ferramenta>_models.py`
3. **Repository** → `repositories/<ferramenta>_repository.py`
4. **Service** → `services/<ferramenta>_service.py` (lógica pura)
5. **Router** → `routers/<ferramenta>.py` (injeta DB com `Depends(get_db)`)
6. **Registrar** router em `main.py` e importar o model (para registrar no metadata)
7. **Migration** → `alembic revision --autogenerate -m "..."` + `alembic upgrade head`
8. **Ativar** na lista de `/api/tools` com `available: True`

---

## 🔐 Lógica do Validador de Senha

| Verificação | Critério | Pontos |
|---|---|---|
| Comprimento mínimo | ≥ 8 chars | +1 |
| Comprimento bom | ≥ 12 chars | +1 |
| Comprimento ótimo | ≥ 16 chars | +1 |
| Letras maiúsculas | A-Z presente | +1 |
| Letras minúsculas | a-z presente | +1 |
| Números | 0-9 presente | +1 |
| Caracteres especiais | !@#$... | +1 |
| Não é senha comum | Lista local | +1 |
| Sem repetições | sem `aaa`, `111` | +0.5 |
| Sem sequências | sem `abc`, `123` | +0.5 |
| Sem padrão de teclado | sem `qwerty` | +0.5 |
| Entropia alta | ≥ 50 bits | +0.5 |

Score final normalizado para 0–5 (÷2, arredondado).

---

## ✅ Checklist para Novos Desenvolvedores

- [ ] Lógica de negócio SEMPRE em `services/`, nunca no router
- [ ] Toda entrada/saída de endpoint com schema Pydantic em `models/`
- [ ] Acesso ao banco SEMPRE via Repository, nunca direto no router
- [ ] Novos models devem ser importados em `main.py` para registrar no metadata
- [ ] Rodar `alembic revision --autogenerate` após alterar models
- [ ] Rodar `alembic upgrade head` antes de subir o servidor
- [ ] Manter padrão `/api/<ferramenta>/<ação>` nas rotas
- [ ] Comentários em português

