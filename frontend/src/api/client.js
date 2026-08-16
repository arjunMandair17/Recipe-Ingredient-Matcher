/**
 * Thin fetch helpers for the Recipe API.
 * Response shapes match backend RecipeResponse / IngredientResponse.
 */

const API_BASE = import.meta.env.VITE_API_BASE ?? ''

/**
 * Perform a JSON request against the API and throw on non-OK responses.
 */
async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      Accept: 'application/json',
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let detail = response.statusText
    try {
      const body = await response.json()
      detail = body.detail ?? detail
    } catch {
      /* ignore parse errors */
    }
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }

  return response.json()
}

/**
 * List recipes with optional case-insensitive name filter and pagination.
 */
export function fetchRecipes({ name, limit = 50, offset = 0 } = {}) {
  const params = new URLSearchParams()
  if (name?.trim()) params.set('name', name.trim())
  params.set('limit', String(limit))
  params.set('offset', String(offset))
  return request(`/recipes/?${params}`)
}

/**
 * Fetch a single recipe by id, including nested ingredients.
 */
export function fetchRecipe(recipeId) {
  return request(`/recipes/${recipeId}`)
}

/**
 * Search recipes that use any of the given ingredient ids.
 * Returns recipes annotated with match_type: "exact" | "partial".
 */
export function searchRecipesByIngredients(ingredientIds) {
  return request('/recipes/search', {
    method: 'POST',
    body: JSON.stringify({ ingredient_ids: ingredientIds }),
  })
}

/**
 * List ingredients with optional name filter and pagination.
 */
export function fetchIngredients({ name, limit = 50, offset = 0 } = {}) {
  const params = new URLSearchParams()
  if (name?.trim()) params.set('name', name.trim())
  params.set('limit', String(limit))
  params.set('offset', String(offset))
  return request(`/ingredients/?${params}`)
}

/**
 * Fetch a single ingredient by id.
 */
export function fetchIngredient(ingredientId) {
  return request(`/ingredients/${ingredientId}`)
}

/**
 * Fetch API health (recipe and ingredient counts).
 */
export function fetchHealth() {
  return request('/health')
}
