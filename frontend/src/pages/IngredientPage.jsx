import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchIngredient, searchRecipesByIngredients } from '../api/client.js'
import { formatIngredientPrice } from '../utils/ingredients.js'
import PaperCard from '../components/ui/PaperCard.jsx'
import RecipeGrid from '../components/recipe/RecipeGrid.jsx'
import RecipeDetail from '../components/recipe/RecipeDetail.jsx'
import LoadingState from '../components/ui/LoadingState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import './IngredientPage.css'

/**
 * Format an ISO / datetime string for display.
 */
function formatScrapedDate(value) {
  if (!value) return 'Never scraped'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

/**
 * Ingredient detail page at /ingredients/:id.
 */
function IngredientPage() {
  const { ingredientId } = useParams()
  const [ingredient, setIngredient] = useState(null)
  const [recipes, setRecipes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeRecipe, setActiveRecipe] = useState(null)

  useEffect(() => {
    let cancelled = false

    /**
     * Load ingredient details and a few related recipes.
     */
    async function load() {
      setLoading(true)
      setError('')
      setIngredient(null)
      setRecipes([])
      try {
        const id = Number(ingredientId)
        const [detail, related] = await Promise.all([
          fetchIngredient(id),
          searchRecipesByIngredients([id]),
        ])
        if (!cancelled) {
          setIngredient(detail)
          setRecipes(related.slice(0, 6))
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || 'Could not load this ingredient.')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [ingredientId])

  const price = ingredient ? formatIngredientPrice(ingredient.price) : null

  return (
    <div className="ingredient-page">
      <Link to="/search" className="ingredient-page__back label">
        ← Back to recipes
      </Link>

      {loading ? <LoadingState message="Loading ingredient…" /> : null}
      {error ? (
        <EmptyState title="Ingredient not found" message={error} icon="error" />
      ) : null}

      {!loading && !error && ingredient ? (
        <>
          <PaperCard
            torn
            className="ingredient-page__panel"
            tape={{
              color: 'green',
              width: '5.5rem',
              style: { top: 0, left: '50%', transform: 'translateX(-50%) rotate(-1deg)' },
            }}
          >
            <p className="ingredient-page__eyebrow label">Ingredient</p>
            <h1 className="headline-xl ingredient-page__title">{ingredient.name}</h1>

            <dl className="ingredient-page__meta">
              <div>
                <dt className="label">Price</dt>
                <dd className={price.available ? '' : 'is-specialty'}>{price.text}</dd>
              </div>
              <div>
                <dt className="label">Last scraped</dt>
                <dd>{formatScrapedDate(ingredient.last_scraped)}</dd>
              </div>
            </dl>
          </PaperCard>

          <section className="ingredient-page__recipes" aria-live="polite">
            <div className="ingredient-page__recipes-head">
              <h2 className="headline-lg">Recipes using this</h2>
              <p className="label ingredient-page__count">
                {recipes.length} shown
              </p>
            </div>

            {recipes.length === 0 ? (
              <EmptyState
                title="No recipes yet"
                message="Nothing in the catalog is linked to this ingredient."
                icon="restaurant"
              />
            ) : (
              <RecipeGrid recipes={recipes} onSelect={setActiveRecipe} />
            )}
          </section>
        </>
      ) : null}

      <RecipeDetail recipe={activeRecipe} onClose={() => setActiveRecipe(null)} />
    </div>
  )
}

export default IngredientPage
