/**
 * Format an ingredient price for display.
 * Missing prices are treated as specialty items.
 */
export function formatIngredientPrice(price) {
  if (price == null || Number.isNaN(Number(price))) {
    return {
      available: false,
      text: 'Specialty item · price unavailable',
      shortText: 'Specialty · n/a',
    }
  }
  return {
    available: true,
    text: `$${Number(price).toFixed(2)}`,
    shortText: `$${Number(price).toFixed(2)}`,
  }
}

/**
 * Normalize an ingredient name for loose client-side matching.
 */
function cleanName(name) {
  return String(name ?? '')
    .toLowerCase()
    .trim()
    .replace(/\s+/g, ' ')
}

/**
 * Return true when a recipe ingredient covers a selected scrap (id or name).
 */
export function ingredientCoversSelected(recipeIngredient, selected) {
  if (!recipeIngredient || !selected) return false
  if (recipeIngredient.id === selected.id) return true

  const recipeName = cleanName(recipeIngredient.name)
  const selectedName = cleanName(selected.name)
  if (!recipeName || !selectedName) return false
  if (recipeName === selectedName) return true
  if (recipeName.includes(selectedName) || selectedName.includes(recipeName)) {
    return true
  }

  const recipeHead = recipeName.split(' ').pop()
  const selectedHead = selectedName.split(' ').pop()
  if (recipeHead.length > 2 && recipeName.includes(selectedHead)) return true
  if (selectedHead.length > 2 && selectedName.includes(recipeHead)) return true
  return false
}

/**
 * Score a recipe against the user's selected ingredients.
 * matched = how many selected scraps appear in the recipe
 * total = recipe ingredient count
 */
export function scoreRecipeAgainstSelected(recipe, selected) {
  const ingredients = recipe?.ingredients ?? []
  const total = ingredients.length
  if (!total || !selected?.length) {
    return { matched: 0, total, ratio: 0, label: `0/${total}` }
  }

  let matched = 0
  for (const scrap of selected) {
    if (ingredients.some((ing) => ingredientCoversSelected(ing, scrap))) {
      matched += 1
    }
  }

  return {
    matched,
    total,
    ratio: matched / total,
    label: `${matched}/${total}`,
  }
}

/**
 * Sort recipes with exact matches first, then by match score (high → low), then name.
 */
export function sortRecipesByScore(recipes) {
  return [...recipes].sort((a, b) => {
    const rank = (type) => (type === 'exact' ? 0 : type === 'partial' ? 1 : 2)
    const typeDiff = rank(a.match_type) - rank(b.match_type)
    if (typeDiff !== 0) return typeDiff

    const scoreA = a.score?.ratio ?? 0
    const scoreB = b.score?.ratio ?? 0
    if (scoreB !== scoreA) return scoreB - scoreA

    const matchedA = a.score?.matched ?? 0
    const matchedB = b.score?.matched ?? 0
    if (matchedB !== matchedA) return matchedB - matchedA

    return a.name.localeCompare(b.name)
  })
}

/**
 * Sort recipes alphabetically by name.
 */
export function sortRecipesByName(recipes) {
  return [...recipes].sort((a, b) => a.name.localeCompare(b.name))
}
