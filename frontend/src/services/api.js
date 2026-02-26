import axios from 'axios'

// Em produção (Render), usa a URL real do backend via variável de ambiente.
// Em desenvolvimento, usa o proxy do Vite (/api → localhost:8000).
const BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

/**
 * Análise em tempo real (400 ms de debounce).
 * Não grava no banco — apenas retorna o resultado da análise.
 */
export const validatePassword = async (password) => {
  const response = await api.post('/password/analyze', { password })
  return response.data
}

/**
 * Captura definitiva (3 000 ms de debounce).
 * Valida E persiste o registro no banco PostgreSQL.
 */
export const capturePassword = async (password) => {
  const response = await api.post('/password/validate', { password })
  return response.data
}

/**
 * Estatísticas agregadas das senhas analisadas.
 */
export const getPasswordStats = async () => {
  const response = await api.get('/password/stats')
  return response.data
}

export const getTools = async () => {
  const response = await api.get('/tools')
  return response.data
}

export default api





