import { useState } from 'react'

export default function PasswordInput({ value, onChange }) {
  const [show, setShow] = useState(false)

  return (
    <div className="password-input-wrapper">
      <label className="input-label">Digite sua senha para análise</label>
      <div className="password-input-container">
        <input
          type={show ? 'text' : 'password'}
          className="password-input"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Ex: MinhaS3nh@Segur@!"
          autoComplete="off"
          spellCheck={false}
        />
        <button
          type="button"
          className="toggle-visibility"
          onClick={() => setShow((s) => !s)}
          aria-label={show ? 'Ocultar senha' : 'Mostrar senha'}
        >
          {show ? '🙈' : '👁️'}
        </button>
      </div>
      <p className="input-hint">
        🔒 Sua senha <strong>não é armazenada</strong>. Análise feita em tempo real.
      </p>
    </div>
  )
}

