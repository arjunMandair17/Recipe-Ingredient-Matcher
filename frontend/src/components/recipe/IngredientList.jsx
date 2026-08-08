import { formatIngredientPrice } from '../../utils/ingredients.js'
import './IngredientList.css'

/**
 * Checklist of IngredientResponse objects for a recipe detail view.
 */
function IngredientList({ ingredients }) {
  if (!ingredients?.length) {
    return <p className="body-muted">No ingredients listed for this recipe.</p>
  }

  return (
    <ul className="ingredient-list">
      {ingredients.map((ingredient) => {
        const price = formatIngredientPrice(ingredient.price)
        return (
          <li key={ingredient.id} className="ingredient-list__item">
            <span className="ingredient-list__mark" aria-hidden="true">
              ○
            </span>
            <span className="ingredient-list__name">{ingredient.name}</span>
            <span
              className={`ingredient-list__price label${price.available ? '' : ' is-specialty'}`}
            >
              {price.text}
            </span>
          </li>
        )
      })}
    </ul>
  )
}

export default IngredientList
