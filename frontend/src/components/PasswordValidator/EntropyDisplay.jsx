export default function EntropyDisplay({ entropyBits }) {
  const getLevel = (bits) => {
    if (bits < 28) return { label: 'Muito baixa', color: '#ef4444' }
    if (bits < 36) return { label: 'Baixa', color: '#f97316' }
    if (bits < 50) return { label: 'Razoável', color: '#eab308' }
    if (bits < 70) return { label: 'Alta', color: '#22c55e' }
    return { label: 'Muito alta', color: '#06b6d4' }
  }

  const { label, color } = getLevel(entropyBits)
  const percentage = Math.min(100, (entropyBits / 100) * 100)

  return (
    <div className="entropy-display">
      <div className="entropy-display__header">
        <span className="entropy-display__title">🎲 Entropia</span>
        <span className="entropy-display__bits" style={{ color }}>
          {entropyBits} bits — {label}
        </span>
      </div>
      <div className="entropy-bar-bg">
        <div
          className="entropy-bar-fill"
          style={{ width: `${percentage}%`, backgroundColor: color, transition: 'width 0.4s ease' }}
        />
      </div>
      <p className="entropy-description">
        A entropia mede a imprevisibilidade da senha. O recomendado é ≥ 50 bits para resistir a
        ataques de força bruta modernos.
      </p>
    </div>
  )
}

