import { formatIngredientPrice } from '../../utils/ingredients.js'
import './IngredientChip.css'

/**
 * Removable washi-style chip for a selected IngredientResponse.
 */
function IngredientChip({ ingredient, onRemove, tilt = '' }) {
  const price = formatIngredientPrice(ingredient.price)

  return (
    <div className={`ingredient-chip ${tilt}`.trim()}>
      <span className="ingredient-chip__name">{ingredient.name}</span>
      <span
        className={`ingredient-chip__price${price.available ? '' : ' is-specialty'}`}
      >
        {price.shortText}
      </span>
      <button
        type="button"
        className="ingredient-chip__remove"
        onClick={() => onRemove?.(ingredient)}
        aria-label={`Remove ${ingredient.name}`}
      >
        <span className="material-symbols-outlined" aria-hidden="true">
          close
        </span>
      </button>
    </div>
  )
}

export default IngredientChip
