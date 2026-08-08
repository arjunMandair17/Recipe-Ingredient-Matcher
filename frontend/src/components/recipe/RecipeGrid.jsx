import RecipeCard from './RecipeCard.jsx'
import './RecipeGrid.css'

/**
 * Responsive scrapbook grid of RecipeCard components.
 */
function RecipeGrid({ recipes, onSelect }) {
  if (!recipes?.length) return null

  return (
    <div className="recipe-grid">
      {recipes.map((recipe, index) => (
        <RecipeCard
          key={recipe.id}
          recipe={recipe}
          index={index}
          onSelect={onSelect}
        />
      ))}
    </div>
  )
}

export default RecipeGrid
