# 🛡️ CyberSec Tool Suite

Aplicação web full-stack com ferramentas de segurança cibernética.

Acesse para uma maior imersão 
https://cybersec-frontend.onrender.com/

**Stack:** Python (FastAPI) + React (Vite)

---

## 🚀 Como rodar

### Backend (Python / FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API disponível em: http://localhost:8000  
Documentação Swagger: http://localhost:8000/docs

### Frontend (React / Vite)

```bash
cd frontend
npm install
npm run dev
```

App disponível em: http://localhost:5173

---

## 🔐 Ferramentas disponíveis

### 1. Validador de Senha
Analisa a segurança da senha com base em:
- **NIST SP 800-63B** e **OWASP** guidelines
- Comprimento mínimo (12+) e ideal (16+)
- Presença de maiúsculas, minúsculas, números e símbolos
- Verificação contra lista de senhas mais comuns
- Detecção de caracteres repetidos (aaa, 111)
- Detecção de sequências óbvias (abc, 123)
- Detecção de padrões de teclado (qwerty, asdf)
- Cálculo de entropia (bits)
- Score de 0 a 5 estrelas com dicas de melhoria

---

## 📁 Estrutura do projeto

```
cybersec-tool-suite/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/password.py
│   │   ├── services/password_validator.py
│   │   ├── models/password_models.py
│   │   └── data/common_passwords.txt
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── ToolSelector/
    │   │   ├── PasswordValidator/
    │   │   └── shared/
    │   ├── services/api.js
    │   └── styles/index.css
    ├── package.json
    └── vite.config.js
```

