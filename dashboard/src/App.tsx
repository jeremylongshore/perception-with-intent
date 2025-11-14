import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Topics from './pages/Topics'
import DailyBriefs from './pages/DailyBriefs'
import About from './pages/About'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white">
        {/* Navigation */}
        <nav className="border-b border-zinc-100">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex items-center space-x-8">
                <h1 className="text-2xl font-bold text-primary">Perception</h1>
                <div className="hidden md:flex space-x-6">
                  <Link to="/" className="text-zinc-600 hover:text-primary transition-colors">
                    Dashboard
                  </Link>
                  <Link to="/topics" className="text-zinc-600 hover:text-primary transition-colors">
                    Topics
                  </Link>
                  <Link to="/briefs" className="text-zinc-600 hover:text-primary transition-colors">
                    Daily Briefs
                  </Link>
                  <Link to="/about" className="text-zinc-600 hover:text-primary transition-colors">
                    About
                  </Link>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <button className="btn-secondary text-sm">
                  Settings
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/topics" element={<Topics />} />
            <Route path="/briefs" element={<DailyBriefs />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
