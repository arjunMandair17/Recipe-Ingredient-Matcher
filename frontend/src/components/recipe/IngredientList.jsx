import { Link } from 'react-router-dom'
import { formatIngredientPrice } from '../../utils/ingredients.js'
import './IngredientList.css'

/**
 * Checklist of IngredientResponse objects for a recipe detail view.
 * Name on top (linked), measure below in smaller type, price on the right.
 */
function IngredientList({ ingredients }) {
  if (!ingredients?.length) {
    return <p className="body-muted">No ingredients listed for this recipe.</p>
  }

  return (
    <ul className="ingredient-list">
      {ingredients.map((ingredient, index) => {
        const price = formatIngredientPrice(ingredient.price)
        const measure = ingredient.measure?.trim()
        return (
          <li
            key={`${ingredient.id}-${measure ?? 'x'}-${index}`}
            className="ingredient-list__item"
          >
            <span className="ingredient-list__mark" aria-hidden="true">
              ○
            </span>
            <span className="ingredient-list__main">
              <Link
                to={`/ingredients/${ingredient.id}`}
                className="ingredient-list__name"
              >
                {ingredient.name}
              </Link>
              {measure ? (
                <span className="ingredient-list__measure">{measure}</span>
              ) : null}
            </span>
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
