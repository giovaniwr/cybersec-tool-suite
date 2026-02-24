import { useNavigate } from 'react-router-dom'

export default function ToolCard({ tool }) {
  const navigate = useNavigate()

  return (
    <div
      className={`tool-card ${!tool.available ? 'tool-card--disabled' : ''}`}
      onClick={() => tool.available && navigate(tool.route)}
      title={!tool.available ? 'Em breve...' : ''}
    >
      <div className="tool-card__icon">{tool.icon}</div>
      <div className="tool-card__content">
        <h3 className="tool-card__name">{tool.name}</h3>
        <p className="tool-card__description">{tool.description}</p>
      </div>
      {!tool.available && <span className="tool-card__badge">Em Breve</span>}
      {tool.available && <span className="tool-card__badge tool-card__badge--active">Disponível</span>}
    </div>
  )
}

