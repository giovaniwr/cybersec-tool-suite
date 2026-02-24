import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/shared/Navbar'
import ToolSelector from './components/ToolSelector/ToolSelector'
import PasswordValidator from './components/PasswordValidator/PasswordValidator'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ToolSelector />} />
            <Route path="/password" element={<PasswordValidator />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App

