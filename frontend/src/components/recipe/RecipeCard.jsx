import { Link } from 'react-router-dom'
import MatchBadge from '../ui/MatchBadge.jsx'
import StickyButton from '../ui/StickyButton.jsx'
import WashiTape from '../ui/WashiTape.jsx'
import './RecipeCard.css'

const TILTS = ['tilt-n1', 'tilt-1', 'tilt-n2', 'tilt-2']
const TAPES = ['yellow', 'green', 'pink']

/**
 * Format a short instruction preview from recipe.instructions.
 */
function previewText(instructions, max = 110) {
  if (!instructions) return 'Open for full instructions and ingredients.'
  const clean = instructions.replace(/\s+/g, ' ').trim()
  if (clean.length <= max) return clean
  return `${clean.slice(0, max).trim()}…`
}

/**
 * Scrapbook recipe card mapped to RecipeResponse fields.
 */
function RecipeCard({ recipe, index = 0, onSelect }) {
  const tilt = TILTS[index % TILTS.length]
  const tapeColor = TAPES[index % TAPES.length]
  const ingredientCount = recipe.ingredients?.length ?? 0
  const score = recipe.score
  const href = `/recipe/${recipe.id}`

  return (
    <article className={`recipe-card paper ${tilt}`}>
      <WashiTape
        color={tapeColor}
        width="3.5rem"
        className="recipe-card__tape"
        style={{ top: '-0.4rem', right: '1rem' }}
      />
      <div className="recipe-card__polaroid">
        {recipe.image_url ? (
          <img src={recipe.image_url} alt="" loading="lazy" />
        ) : (
          <div className="recipe-card__placeholder" aria-hidden="true">
            <span className="material-symbols-outlined">restaurant</span>
          </div>
        )}
      </div>
      <h3 className="recipe-card__title">
        <Link to={href} className="recipe-card__title-link">
          {recipe.name}
        </Link>
      </h3>
      <p className="recipe-card__preview">{previewText(recipe.instructions)}</p>
      {recipe.match_type ? <MatchBadge matchType={recipe.match_type} /> : null}
      {score ? (
        <div className="recipe-card__score" role="status">
          <span className="material-symbols-outlined" aria-hidden="true">
            percent
          </span>
          <span>
            Uses {score.label} scraps
            <span className="recipe-card__score-pct">
              {' '}
              · {Math.round(score.ratio * 100)}%
            </span>
          </span>
        </div>
      ) : null}
      <div className="recipe-card__meta label">
        <span>
          <span className="material-symbols-outlined" aria-hidden="true">
            grocery
          </span>
          {ingredientCount} ingredient{ingredientCount === 1 ? '' : 's'}
        </span>
      </div>
      <StickyButton variant="ghost" onClick={() => onSelect?.(recipe)}>
        View Recipe
      </StickyButton>
    </article>
  )
}

export default RecipeCard
