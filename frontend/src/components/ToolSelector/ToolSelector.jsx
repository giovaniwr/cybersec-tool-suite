import { useEffect, useState } from 'react'
import { getTools } from '../../services/api'
import ToolCard from '../shared/ToolCard'
import DevProfile from '../shared/DevProfile'

const FALLBACK_TOOLS = [
  {
    id: 'password-validator',
    name: 'Validador de Senha',
    description: 'Verifique se sua senha é realmente segura com base nos padrões modernos de cibersegurança (NIST/OWASP).',
    icon: '🔐',
    route: '/password',
    available: true,
  },
  {
    id: 'hash-checker',
    name: 'Verificador de Hash',
    description: 'Verifique se um arquivo foi adulterado comparando seu hash.',
    icon: '🔍',
    route: '/hash',
    available: false,
  },
  {
    id: 'phishing-detector',
    name: 'Detector de Phishing',
    description: 'Analise URLs suspeitas para identificar tentativas de phishing.',
    icon: '🎣',
    route: '/phishing',
    available: false,
  },
]

export default function ToolSelector() {
  const [tools, setTools] = useState(FALLBACK_TOOLS)

  useEffect(() => {
    getTools()
      .then(setTools)
      .catch(() => setTools(FALLBACK_TOOLS))
  }, [])

  return (
    <div className="tool-selector">
      <div className="tool-selector__header">
        <h1 className="tool-selector__title">
          🛡️ CyberSec Tool Suite
        </h1>
        <p className="tool-selector__subtitle">
          Ferramentas de segurança cibernética para proteger você online.
          Selecione uma ferramenta abaixo para começar.
        </p>
      </div>
      <div className="tools-grid">
        {tools.map((tool) => (
          <ToolCard key={tool.id} tool={tool} />
        ))}
      </div>

      <DevProfile />
    </div>
  )
}
