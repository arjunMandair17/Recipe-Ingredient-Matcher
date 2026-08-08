import IngredientChip from './IngredientChip.jsx'
import './SelectedScraps.css'

const TILTS = ['tilt-n2', 'tilt-1', 'tilt-n1', 'tilt-2']

/**
 * Selected ingredient chips ("My Scraps") before recipe search.
 */
function SelectedScraps({ ingredients, onRemove }) {
  return (
    <section className="selected-scraps">
      <h2 className="headline-lg selected-scraps__title">
        <span className="material-symbols-outlined" aria-hidden="true">
          compost
        </span>
        My Scraps
      </h2>
      {ingredients.length === 0 ? (
        <p className="body-muted">
          Add ingredients above to find recipes that use them.
        </p>
      ) : (
        <div className="selected-scraps__chips">
          {ingredients.map((ingredient, index) => (
            <IngredientChip
              key={ingredient.id}
              ingredient={ingredient}
              onRemove={onRemove}
              tilt={TILTS[index % TILTS.length]}
            />
          ))}
        </div>
      )}
    </section>
  )
}

export default SelectedScraps
