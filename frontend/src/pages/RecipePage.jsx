import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { fetchRecipe } from '../api/client.js'
import MatchBadge from '../components/ui/MatchBadge.jsx'
import IngredientList from '../components/recipe/IngredientList.jsx'
import LoadingState from '../components/ui/LoadingState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import WashiTape from '../components/ui/WashiTape.jsx'
import './RecipePage.css'

/**
 * Split instructions into readable steps when numbered or newline-separated.
 */
function instructionSteps(instructions) {
  if (!instructions?.trim()) return []
  const numbered = instructions
    .split(/\n+|(?<=\.)\s+(?=\d+\.)/)
    .map((s) => s.trim())
    .filter(Boolean)
  if (numbered.length > 1) return numbered
  return [instructions.trim()]
}

/**
 * Full-page recipe detail at /recipe/:recipeId.
 */
function RecipePage() {
  const { recipeId } = useParams()
  const [recipe, setRecipe] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    /**
     * Load a single recipe by id from the API.
     */
    async function load() {
      setLoading(true)
      setError('')
      setRecipe(null)
      try {
        const result = await fetchRecipe(recipeId)
        if (!cancelled) setRecipe(result)
      } catch (err) {
        if (!cancelled) setError(err.message || 'Could not load this recipe.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [recipeId])

  const steps = recipe ? instructionSteps(recipe.instructions) : []

  return (
    <div className="recipe-page">
      <Link to="/search" className="recipe-page__back label">
        ← Back to recipes
      </Link>

      {loading ? <LoadingState message="Loading recipe…" /> : null}
      {error ? (
        <EmptyState title="Recipe not found" message={error} icon="error" />
      ) : null}

      {!loading && !error && recipe ? (
        <article className="recipe-page__sheet paper">
          <WashiTape
            color="yellow"
            width="6.5rem"
            className="recipe-page__tape"
            style={{ top: 0, left: '50%', transform: 'translateX(-50%) rotate(-2deg)' }}
          />

          {recipe.image_url ? (
            <div className="recipe-page__hero">
              <img src={recipe.image_url} alt="" />
            </div>
          ) : null}

          <div className="recipe-page__body">
            <header className="recipe-page__header">
              <h1 className="headline-xl recipe-page__title">{recipe.name}</h1>
              {recipe.match_type ? <MatchBadge matchType={recipe.match_type} /> : null}
              {recipe.score ? (
                <p className="recipe-page__score label">
                  Uses {recipe.score.label} of this recipe&apos;s ingredients
                  {' '}({Math.round(recipe.score.ratio * 100)}% match)
                </p>
              ) : null}
            </header>

            <div className="recipe-page__columns">
              <section className="recipe-page__section" aria-labelledby="recipe-ingredients">
                <h2 id="recipe-ingredients" className="label recipe-page__section-title">
                  Ingredients
                </h2>
                <IngredientList ingredients={recipe.ingredients} />
              </section>

              <section className="recipe-page__section" aria-labelledby="recipe-instructions">
                <h2 id="recipe-instructions" className="label recipe-page__section-title">
                  Instructions
                </h2>
                {steps.length ? (
                  <ol className="recipe-page__steps">
                    {steps.map((step, index) => (
                      <li key={`${index}-${step.slice(0, 24)}`}>{step}</li>
                    ))}
                  </ol>
                ) : (
                  <p className="body-muted">No instructions provided.</p>
                )}
              </section>
            </div>
          </div>
        </article>
      ) : null}
    </div>
  )
}

export default RecipePage
