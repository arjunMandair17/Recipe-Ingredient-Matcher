import { useEffect, useState } from 'react'
import { fetchRecipes } from '../api/client.js'
import NameSearchBar from '../components/search/NameSearchBar.jsx'
import RecipeGrid from '../components/recipe/RecipeGrid.jsx'
import RecipeDetail from '../components/recipe/RecipeDetail.jsx'
import LoadingState from '../components/ui/LoadingState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import './SearchPage.css'

/**
 * Name-based recipe search using GET /recipes/?name=...
 * Debounces query changes so typing hits the API without relying only on Search.
 */
function SearchPage() {
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [recipes, setRecipes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeRecipe, setActiveRecipe] = useState(null)

  useEffect(() => {
    const handle = window.setTimeout(() => {
      setDebouncedQuery(query.trim())
    }, 300)
    return () => window.clearTimeout(handle)
  }, [query])

  useEffect(() => {
    let cancelled = false

    /**
     * Load recipes for the current name filter (or browse all when empty).
     */
    async function load() {
      setLoading(true)
      setError('')
      try {
        const results = await fetchRecipes({
          name: debouncedQuery || undefined,
          limit: 60,
        })
        if (!cancelled) setRecipes(results)
      } catch (err) {
        if (!cancelled) {
          setRecipes([])
          setError('Could not load recipes.')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [debouncedQuery])

  return (
    <div className="search-page">
      <header className="search-page__intro">
        <h1 className="headline-xl">Find recipes by name</h1>
        <p className="body-muted">
          Browse the catalog or filter by title. Each card shows the recipe image,
          instructions preview, and ingredient count from the API.
        </p>
      </header>

      <NameSearchBar
        value={query}
        onChange={setQuery}
        onSubmit={(value) => setDebouncedQuery(value.trim())}
      />

      <section className="search-page__results" aria-live="polite">
        <div className="search-page__results-head">
          <h2 className="headline-lg">Recipes</h2>
          {!loading ? (
            <p className="label search-page__count">
              {debouncedQuery
                ? `${recipes.length} result${recipes.length === 1 ? '' : 's'} for “${debouncedQuery}”`
                : `${recipes.length} recipes`}
            </p>
          ) : null}
        </div>

        {loading ? <LoadingState /> : null}
        {error ? (
          <EmptyState title="Something went wrong" message={"Server Error"} icon="error" />
        ) : null}
        {!loading && !error && recipes.length === 0 ? (
          <EmptyState
            title="No recipes found"
            message={
              debouncedQuery
                ? 'Try a shorter name or a different spelling.'
                : 'The recipe catalog looks empty. Seed the database if you have not yet.'
            }
          />
        ) : null}
        {!loading && recipes.length > 0 ? (
          <RecipeGrid recipes={recipes} onSelect={setActiveRecipe} />
        ) : null}
      </section>

      <RecipeDetail recipe={activeRecipe} onClose={() => setActiveRecipe(null)} />
    </div>
  )
}

export default SearchPage
