import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout.jsx'
import HomePage from './pages/HomePage.jsx'
import MatchPage from './pages/MatchPage.jsx'
import SearchPage from './pages/SearchPage.jsx'
import IngredientPage from './pages/IngredientPage.jsx'
import RecipePage from './pages/RecipePage.jsx'

/**
 * Root app router: Home, match, name search, ingredient + recipe detail.
 */
function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/match" element={<MatchPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/ingredients/:ingredientId" element={<IngredientPage />} />
        <Route path="/recipe/:recipeId" element={<RecipePage />} />
      </Route>
    </Routes>
  )
}

export default App
