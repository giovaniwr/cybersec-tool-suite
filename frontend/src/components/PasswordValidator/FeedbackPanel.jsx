const CHECK_LABELS = {
  length_ok: { label: 'Mínimo de 12 caracteres', icon: '📏' },
  length_great: { label: '16 ou mais caracteres (ideal)', icon: '📐' },
  has_uppercase: { label: 'Letras maiúsculas (A-Z)', icon: '🔠' },
  has_lowercase: { label: 'Letras minúsculas (a-z)', icon: '🔡' },
  has_digit: { label: 'Números (0-9)', icon: '🔢' },
  has_special: { label: 'Caracteres especiais (!@#$...)', icon: '✨' },
  not_common: { label: 'Não é uma senha comum', icon: '📋' },
  no_repeated_chars: { label: 'Sem repetições excessivas (aaa, 111)', icon: '🔄' },
  no_sequential_chars: { label: 'Sem sequências óbvias (abc, 123)', icon: '📶' },
  no_keyboard_pattern: { label: 'Sem padrões de teclado (qwerty)', icon: '⌨️' },
}

export default function FeedbackPanel({ checks, tips, positiveFeedbacks }) {
  return (
    <div className="feedback-panel">
      {/* Checklist */}
      <div className="checklist">
        <h3 className="checklist__title">📋 Verificações de Segurança</h3>
        <div className="checklist__items">
          {Object.entries(checks).map(([key, passed]) => {
            const info = CHECK_LABELS[key]
            if (!info) return null
            return (
              <div
                key={key}
                className={`checklist__item ${passed ? 'checklist__item--pass' : 'checklist__item--fail'}`}
              >
                <span className="checklist__status">{passed ? '✅' : '❌'}</span>
                <span className="checklist__icon">{info.icon}</span>
                <span className="checklist__label">{info.label}</span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Tips */}
      {tips.length > 0 && (
        <div className="tips-panel">
          <h3 className="tips-panel__title">💡 Como melhorar sua senha</h3>
          <ul className="tips-list">
            {tips.map((tip, i) => (
              <li key={i} className="tip-item">
                <span className="tip-bullet">→</span>
                {tip}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Positives */}
      {positiveFeedbacks.length > 0 && (
        <div className="positive-panel">
          <h3 className="positive-panel__title">🏆 Pontos positivos</h3>
          <ul className="positive-list">
            {positiveFeedbacks.map((fb, i) => (
              <li key={i} className="positive-item">
                <span className="positive-bullet">✓</span>
                {fb}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

