import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <span className="navbar-icon">🛡️</span>
        <span className="navbar-title">CyberSec Tool Suite</span>
      </Link>
      <div className="navbar-links">
        <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
          🏠 Ferramentas
        </Link>
        <Link to="/password" className={`nav-link ${location.pathname === '/password' ? 'active' : ''}`}>
          🔐 Senha
        </Link>
      </div>
    </nav>
  )
}

