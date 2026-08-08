import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout.jsx'
import HomePage from './pages/HomePage.jsx'
import MatchPage from './pages/MatchPage.jsx'
import SearchPage from './pages/SearchPage.jsx'

/**
 * Root app router: Home, ingredient match, and name search.
 */
function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/match" element={<MatchPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Route>
    </Routes>
  )
}

export default App
