import { useMemo, useState } from 'react'
import { searchRecipesByIngredients } from '../api/client.js'
import {
  scoreRecipeAgainstSelected,
  sortRecipesByName,
  sortRecipesByScore,
} from '../utils/ingredients.js'
import IngredientSearch from '../components/ingredients/IngredientSearch.jsx'
import SelectedScraps from '../components/ingredients/SelectedScraps.jsx'
import RecipeGrid from '../components/recipe/RecipeGrid.jsx'
import RecipeDetail from '../components/recipe/RecipeDetail.jsx'
import PaperCard from '../components/ui/PaperCard.jsx'
import StickyButton from '../components/ui/StickyButton.jsx'
import LoadingState from '../components/ui/LoadingState.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import './MatchPage.css'

/**
 * Annotate API search hits with a matched/total scrap score.
 */
function withScores(recipes, selected) {
  return recipes.map((recipe) => ({
    ...recipe,
    score: scoreRecipeAgainstSelected(recipe, selected),
  }))
}

/**
 * Apply the active ranking mode to scored recipes.
 */
function rankRecipes(recipes, sortBy) {
  return sortBy === 'name' ? sortRecipesByName(recipes) : sortRecipesByScore(recipes)
}

/**
 * Ingredient-driven recipe matcher using POST /recipes/search.
 */
function MatchPage() {
  const [selected, setSelected] = useState([])
  const [recipes, setRecipes] = useState([])
  const [hasSearched, setHasSearched] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeRecipe, setActiveRecipe] = useState(null)
  const [sortBy, setSortBy] = useState('score')

  const selectedIds = useMemo(() => selected.map((item) => item.id), [selected])
  const rankedRecipes = useMemo(
    () => rankRecipes(recipes, sortBy),
    [recipes, sortBy],
  )
  const exactCount = recipes.filter((r) => r.match_type === 'exact').length
  const partialCount = recipes.filter((r) => r.match_type === 'partial').length

  /**
   * Add an ingredient if it is not already selected.
   */
  function handleAdd(ingredient) {
    setSelected((prev) =>
      prev.some((item) => item.id === ingredient.id) ? prev : [...prev, ingredient],
    )
  }

  /**
   * Remove a selected ingredient chip.
   */
  function handleRemove(ingredient) {
    setSelected((prev) => prev.filter((item) => item.id !== ingredient.id))
  }

  /**
   * Request recipe matches for the current ingredient selection.
   */
  async function handleFindRecipes() {
    if (!selectedIds.length) return
    setLoading(true)
    setError('')
    setHasSearched(true)
    try {
      const results = await searchRecipesByIngredients(selectedIds)
      setRecipes(withScores(results, selected))
      setSortBy('score')
    } catch (err) {
      setRecipes([])
      setError(err.message || 'Could not find matching recipes.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="match-page">
      <PaperCard
        torn
        className="match-page__panel"
        tape={{
          color: 'yellow',
          width: '7rem',
          style: { top: 0, left: '50%', transform: 'translateX(-50%) rotate(-2deg)' },
        }}
      >
        <h1 className="headline-xl match-page__title">What&apos;s in the fridge?</h1>
        <p className="body-muted match-page__lede">
          Add ingredients from the database. Matches are tagged exact or partial
          by the API, and scored by how many of your scraps the recipe uses.
        </p>

        <IngredientSearch selectedIds={selectedIds} onAdd={handleAdd} />
        <SelectedScraps ingredients={selected} onRemove={handleRemove} />

        <div className="match-page__actions">
          <StickyButton
            variant="dark"
            onClick={handleFindRecipes}
            disabled={!selected.length || loading}
          >
            Find recipes
          </StickyButton>
        </div>
      </PaperCard>

      <section className="match-page__results" aria-live="polite">
        <div className="match-page__results-head">
          <h2 className="headline-lg">
            <span className="material-symbols-outlined" aria-hidden="true">
              auto_awesome
            </span>
            Recipe Matches
          </h2>
          {hasSearched && !loading ? (
            <p className="label match-page__counts">
              {recipes.length} found
              {recipes.length
                ? ` · ${exactCount} exact · ${partialCount} partial`
                : ''}
            </p>
          ) : null}
        </div>

        {recipes.length > 0 ? (
          <div className="match-page__sort">
            <label className="label" htmlFor="match-sort">
              Rank by
            </label>
            <select
              id="match-sort"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
            >
              <option value="score">Score (exact first, then best match)</option>
              <option value="name">Name (A–Z)</option>
            </select>
          </div>
        ) : null}

        {loading ? <LoadingState message="Matching your scraps…" /> : null}
        {error ? (
          <EmptyState title="Something went wrong" message={error} icon="error" />
        ) : null}
        {!loading && !error && hasSearched && recipes.length === 0 ? (
          <EmptyState
            title="No recipes matched"
            message="Try adding different ingredients or fewer specialty items."
            icon="search_off"
          />
        ) : null}
        {!loading && rankedRecipes.length > 0 ? (
          <RecipeGrid recipes={rankedRecipes} onSelect={setActiveRecipe} />
        ) : null}
      </section>

      <RecipeDetail recipe={activeRecipe} onClose={() => setActiveRecipe(null)} />
    </div>
  )
}

export default MatchPage
