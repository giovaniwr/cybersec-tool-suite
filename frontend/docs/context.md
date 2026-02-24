# 🎨 Frontend — Contexto de Desenvolvimento

> Use este arquivo como referência sempre que for desenvolver ou expandir o frontend.
> Ele descreve a arquitetura de componentes, padrões de estilo, integração com a API e guias de como adicionar novas ferramentas.

---

## 🏗️ Stack & Tecnologias

| Tecnologia | Versão | Função |
|---|---|---|
| React | ^18.3.1 | Biblioteca de UI |
| Vite | ^5.3.1 | Build tool e servidor de dev |
| React Router DOM | ^6.23.0 | Navegação client-side (SPA) |
| Axios | ^1.7.2 | Requisições HTTP para a API |
| CSS puro (variáveis) | — | Estilização via `index.css` |

---

## 📁 Estrutura de Pastas

```
frontend/
├── index.html
├── package.json
├── vite.config.js                ← Config do Vite com proxy para o backend
├── docs/
│   └── context.md                ← Este arquivo
└── src/
    ├── main.jsx                  ← Ponto de entrada React
    ├── App.jsx                   ← Roteamento principal
    ├── components/
    │   ├── shared/               ← Componentes reutilizáveis em toda a aplicação
    │   │   ├── Navbar.jsx        ← Barra de navegação global
    │   │   └── ToolCard.jsx      ← Card de seleção de ferramenta (tela home)
    │   ├── ToolSelector/
    │   │   └── ToolSelector.jsx  ← Tela home — lista de ferramentas disponíveis
    │   └── PasswordValidator/    ← Ferramenta: Validador de Senha
    │       ├── PasswordValidator.jsx  ← Container principal (estado e lógica)
    │       ├── PasswordInput.jsx      ← Input com toggle show/hide
    │       ├── StrengthMeter.jsx      ← Barra + estrelas de força (score 0-5)
    │       ├── EntropyDisplay.jsx     ← Barra de entropia em bits
    │       └── FeedbackPanel.jsx      ← Checklist + dicas + pontos positivos
    ├── services/
    │   └── api.js                ← Todas as chamadas à API (axios)
    └── styles/
        └── index.css             ← Estilos globais + variáveis CSS + classes de todos os componentes
```

---

## ⚙️ Como Rodar Localmente

```bash
# Pré-requisito: backend deve estar rodando em http://localhost:8000

cd frontend

# Instalar dependências (primeira vez)
npm install

# Iniciar o servidor de desenvolvimento
npm run dev
```

A aplicação estará disponível em: `http://localhost:5173`

> **Proxy:** O Vite está configurado para redirecionar `/api/*` para `http://localhost:8000`.
> Isso significa que `axios.get('/api/tools')` no frontend vira `GET http://localhost:8000/api/tools`.
> Configurado em `vite.config.js`.

---

## 🗺️ Rotas (React Router)

| Rota | Componente | Descrição |
|---|---|---|
| `/` | `ToolSelector` | Tela home com cards de todas as ferramentas |
| `/password` | `PasswordValidator` | Ferramenta de validação de senha |
| `/hash` | *(a criar)* | Ferramenta de verificação de hash |
| `/phishing` | *(a criar)* | Ferramenta de detecção de phishing |

As rotas são definidas em `src/App.jsx`.

---

## 🔌 Integração com a API (`src/services/api.js`)

Todas as chamadas HTTP ficam centralizadas em `api.js`. A instância `axios` base já está configurada:

```js
const api = axios.create({
  baseURL: '/api',           // usa o proxy do Vite
  headers: { 'Content-Type': 'application/json' },
})
```

**Funções existentes:**

| Função | Endpoint | Quando usar |
|---|---|---|
| `validatePassword(pwd)` | `POST /password/analyze` | Tempo real (400 ms) — **não grava no banco** |
| `capturePassword(pwd)` | `POST /password/validate` | Captura definitiva (3 000 ms) — **grava no banco** |
| `getPasswordStats()` | `GET /password/stats` | Estatísticas agregadas |
| `getTools()` | `GET /tools` | Lista de ferramentas |

> ⚠️ **Importante:** `validatePassword` usa `/analyze` (sem DB) e `capturePassword` usa `/validate` (com DB).
> Nunca trocar os dois — isso causaria gravação a cada tecla digitada.

**Para adicionar uma nova chamada de API:**

```js
// services/api.js
export const checkHash = async (fileContent, algorithm = 'sha256') => {
  const response = await api.post('/hash/check', { file_content: fileContent, algorithm })
  return response.data
}
```

---

## 🧱 Padrões de Componentes

### Convenções Gerais
- Arquivos de componente: `PascalCase` (ex: `PasswordValidator.jsx`)
- Componentes são **functional components** com hooks do React
- Cada ferramenta vive em sua própria pasta dentro de `components/`
- Componentes **compartilhados** (usados por múltiplas ferramentas) ficam em `components/shared/`

### Padrão Container × Apresentação
- O componente principal da ferramenta (ex: `PasswordValidator.jsx`) é o **container**: gerencia estado, faz chamada à API, controla loading/error.
- Os sub-componentes (ex: `StrengthMeter`, `FeedbackPanel`) são **apresentacionais**: recebem apenas props e renderizam UI. Não fazem chamadas à API.

### Padrão de Dois Debounces (tempo real vs. captura)
O `PasswordValidator` usa **dois timers independentes** baseados em `useRef` (sem causar re-render extra):

```js
// Timer 1 — Análise visual: atualiza UI rapidamente, NÃO grava no banco
const debouncedAnalyze = useDebounceRef(analyze, 400)   // 400 ms

// Timer 2 — Captura definitiva: grava no banco PostgreSQL após inatividade
const debouncedCapture = useDebounceRef(capture, 3000)  // 3 000 ms

// Ambos disparados juntos no handleChange:
const handleChange = (pwd) => {
  setPassword(pwd)
  debouncedAnalyze(pwd)  // → POST /api/password/analyze  (sem DB)
  debouncedCapture(pwd)  // → POST /api/password/validate (com DB)
}
```

O hook `useDebounceRef` usa `useRef` para o timer, evitando o problema de closure stale
que ocorre com `useState`:

```js
function useDebounceRef(fn, delay) {
  const timerRef = useRef(null)
  return useCallback((...args) => {
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => fn(...args), delay)
  }, [fn, delay])
}
```

---

## 🎨 Estilização (`src/styles/index.css`)

Toda a estilização usa **CSS puro com variáveis CSS** (sem Tailwind, sem Styled Components).

### Variáveis CSS principais (definidas em `:root`)
```css
--color-bg           /* Fundo principal da página */
--color-surface      /* Fundo de cards e painéis */
--color-surface-2    /* Fundo de elementos internos */
--color-border       /* Cor de bordas */
--color-text         /* Texto principal */
--color-text-muted   /* Texto secundário */
--color-primary      /* Cor de destaque/ação */
--color-primary-hover
```

### Convenção de classes CSS
O projeto usa **BEM simplificado**:
- Bloco: `.password-validator`
- Elemento: `.password-validator__header`
- Modificador: `.tool-card--disabled`

### Onde adicionar novos estilos
Adicione os estilos do novo componente diretamente em `src/styles/index.css`, agrupados com um comentário de seção:

```css
/* =========================================
   NOVA FERRAMENTA — Hash Checker
   ========================================= */
.hash-checker { ... }
.hash-checker__input { ... }
```

---

## 🧩 Componentes Existentes — Referência Rápida

### `<Navbar />`
Barra de navegação global. Não recebe props. Usa `useLocation` para marcar o link ativo.
- Para adicionar um link: edite `src/components/shared/Navbar.jsx`

### `<ToolCard tool={} />`
Card clicável na tela home. Recebe um objeto `tool`:
```js
{
  id: string,
  name: string,
  description: string,
  icon: string,       // emoji
  route: string,      // rota React (ex: '/password')
  available: boolean  // false = exibe badge "Em Breve" e desabilita clique
}
```

### `<PasswordValidator />`
Container da ferramenta de senha. Gerencia: `password`, `result`, `loading`, `error`.

### `<PasswordInput value onChange />`
Input com botão de show/hide senha. `onChange(value: string)`.

### `<StrengthMeter score label color />`
Barra segmentada (5 segmentos) + estrelas. `score` de 0 a 5.

### `<EntropyDisplay entropyBits />`
Barra de progresso de entropia + descrição. `entropyBits: number`.

### `<FeedbackPanel checks tips positiveFeedbacks />`
Checklist de verificações + lista de dicas + lista de pontos positivos.
- `checks`: objeto com chaves booleanas (mesmo formato do backend)
- `tips`: `string[]`
- `positiveFeedbacks`: `string[]`

---

## ➕ Como Adicionar uma Nova Ferramenta

### Passo 1 — Criar a pasta do componente
```
src/components/HashChecker/
├── HashChecker.jsx          ← container
├── HashInput.jsx            ← input da ferramenta
└── HashResult.jsx           ← exibição do resultado
```

### Passo 2 — Adicionar a chamada de API em `services/api.js`
```js
export const checkHash = async (fileContent, algorithm) => {
  const response = await api.post('/hash/check', { file_content: fileContent, algorithm })
  return response.data
}
```

### Passo 3 — Registrar a rota em `App.jsx`
```jsx
import HashChecker from './components/HashChecker/HashChecker'

// dentro de <Routes>:
<Route path="/hash" element={<HashChecker />} />
```

### Passo 4 — Adicionar link na `Navbar.jsx`
```jsx
<Link to="/hash" className={`nav-link ${location.pathname === '/hash' ? 'active' : ''}`}>
  🔍 Hash
</Link>
```

### Passo 5 — Adicionar estilos em `index.css`
Agrupe os estilos com um comentário de seção claro.

---

## 📐 Resposta da API — Tipos de Dados

### `PasswordResponse` (retorno de `validatePassword`)
```ts
{
  score: number                  // 0–5
  strength_label: string         // ex: "Forte"
  strength_color: string         // hex, ex: "#22c55e"
  entropy_bits: number           // ex: 67.43
  is_common: boolean
  checks: {
    length_ok: boolean
    length_great: boolean
    has_uppercase: boolean
    has_lowercase: boolean
    has_digit: boolean
    has_special: boolean
    not_common: boolean
    no_repeated_chars: boolean
    no_sequential_chars: boolean
    no_keyboard_pattern: boolean
  }
  tips: string[]
  positive_feedbacks: string[]
}
```

### `Tool` (retorno de `getTools`)
```ts
{
  id: string
  name: string
  description: string
  icon: string
  route: string
  available: boolean
}
```

---

## ✅ Checklist para Novos Desenvolvedores

- [ ] Componentes containers gerenciam estado; componentes presentacionais só recebem props
- [ ] Todas as chamadas HTTP centralizadas em `src/services/api.js`
- [ ] Novas rotas registradas em `App.jsx`
- [ ] Novos links adicionados em `Navbar.jsx`
- [ ] Estilização via CSS puro em `index.css`, usando variáveis CSS do `:root`
- [ ] Seguir nomenclatura BEM simplificada nas classes CSS
- [ ] Inputs de análise em tempo real devem usar debounce (≥ 300ms)
- [ ] Sempre tratar estados de `loading` e `error` nas chamadas à API
- [ ] Comentários em português para manter consistência com o projeto

