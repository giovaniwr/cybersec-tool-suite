export default function StrengthMeter({ score, label, color }) {
  const segments = [1, 2, 3, 4, 5]

  return (
    <div className="strength-meter">
      <div className="strength-meter__label">
        <span>Força da senha:</span>
        <span className="strength-meter__value" style={{ color }}>
          {label}
        </span>
      </div>
      <div className="strength-meter__bar">
        {segments.map((seg) => (
          <div
            key={seg}
            className="strength-meter__segment"
            style={{
              backgroundColor: seg <= score ? color : 'var(--color-surface-2)',
              transition: 'background-color 0.3s ease',
            }}
          />
        ))}
      </div>
      <div className="strength-meter__stars">
        {segments.map((seg) => (
          <span key={seg} className={`star ${seg <= score ? 'star--filled' : ''}`}>
            {seg <= score ? '⭐' : '☆'}
          </span>
        ))}
      </div>
    </div>
  )
}

