import { useEffect } from 'react'
import MatchBadge from '../ui/MatchBadge.jsx'
import StickyButton from '../ui/StickyButton.jsx'
import IngredientList from './IngredientList.jsx'
import './RecipeDetail.css'

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
 * Modal detail view for a RecipeResponse (image, match, ingredients, instructions).
 */
function RecipeDetail({ recipe, onClose }) {
  useEffect(() => {
    if (!recipe) return undefined
    const onKey = (event) => {
      if (event.key === 'Escape') onClose?.()
    }
    document.body.style.overflow = 'hidden'
    window.addEventListener('keydown', onKey)
    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('keydown', onKey)
    }
  }, [recipe, onClose])

  if (!recipe) return null

  const steps = instructionSteps(recipe.instructions)

  return (
    <div className="recipe-detail-overlay" role="presentation" onClick={onClose}>
      <div
        className="recipe-detail paper"
        role="dialog"
        aria-modal="true"
        aria-labelledby="recipe-detail-title"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          className="recipe-detail__close"
          onClick={onClose}
          aria-label="Close recipe"
        >
          <span className="material-symbols-outlined" aria-hidden="true">
            close
          </span>
        </button>

        {recipe.image_url ? (
          <div className="recipe-detail__image">
            <img src={recipe.image_url} alt="" />
          </div>
        ) : null}

        <div className="recipe-detail__body">
          <h2 id="recipe-detail-title" className="headline-lg">
            {recipe.name}
          </h2>
          {recipe.match_type ? <MatchBadge matchType={recipe.match_type} /> : null}
          {recipe.score ? (
            <p className="recipe-detail__score label">
              Uses {recipe.score.label} of this recipe&apos;s ingredients
              {' '}({Math.round(recipe.score.ratio * 100)}% match)
            </p>
          ) : null}

          <section className="recipe-detail__section">
            <h3 className="label recipe-detail__section-title">Ingredients</h3>
            <IngredientList ingredients={recipe.ingredients} />
          </section>

          <section className="recipe-detail__section">
            <h3 className="label recipe-detail__section-title">Instructions</h3>
            {steps.length ? (
              <ol className="recipe-detail__steps">
                {steps.map((step, index) => (
                  <li key={`${index}-${step.slice(0, 24)}`}>{step}</li>
                ))}
              </ol>
            ) : (
              <p className="body-muted">No instructions provided.</p>
            )}
          </section>

          <StickyButton variant="secondary" onClick={onClose}>
            Close
          </StickyButton>
        </div>
      </div>
    </div>
  )
}

export default RecipeDetail
