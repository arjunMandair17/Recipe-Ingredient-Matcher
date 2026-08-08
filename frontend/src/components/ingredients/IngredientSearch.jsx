import { useEffect, useId, useRef, useState } from 'react'
import { fetchIngredients } from '../../api/client.js'
import { formatIngredientPrice } from '../../utils/ingredients.js'
import StickyButton from '../ui/StickyButton.jsx'
import './IngredientSearch.css'

/**
 * Autocomplete search that adds IngredientResponse items from the API.
 */
function IngredientSearch({ selectedIds, onAdd }) {
  const inputId = useId()
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [open, setOpen] = useState(false)
  const wrapRef = useRef(null)

  useEffect(() => {
    const onPointerDown = (event) => {
      if (!wrapRef.current?.contains(event.target)) setOpen(false)
    }
    document.addEventListener('pointerdown', onPointerDown)
    return () => document.removeEventListener('pointerdown', onPointerDown)
  }, [])

  useEffect(() => {
    const trimmed = query.trim()
    if (trimmed.length < 1) {
      setSuggestions([])
      setLoading(false)
      setError('')
      setOpen(false)
      return undefined
    }

    const handle = window.setTimeout(async () => {
      setLoading(true)
      setError('')
      try {
        const results = await fetchIngredients({ name: trimmed, limit: 12 })
        const filtered = results.filter((item) => !selectedIds.includes(item.id))
        setSuggestions(filtered)
        setOpen(true)
        if (!filtered.length) {
          setError('No matching ingredients in the database.')
        }
      } catch (err) {
        setError(err.message || 'Could not search ingredients.')
        setSuggestions([])
        setOpen(false)
      } finally {
        setLoading(false)
      }
    }, 250)

    return () => window.clearTimeout(handle)
  }, [query, selectedIds])

  /**
   * Add an ingredient and clear the current query.
   */
  function handleSelect(ingredient) {
    onAdd?.(ingredient)
    setQuery('')
    setSuggestions([])
    setOpen(false)
    setError('')
  }

  /**
   * Add the first suggestion when pressing Enter / Add.
   */
  function handleSubmit(event) {
    event.preventDefault()
    if (suggestions[0]) {
      handleSelect(suggestions[0])
      return
    }
    if (query.trim() && !loading) {
      setError('Pick an ingredient from the suggestions list first.')
      setOpen(true)
    }
  }

  return (
    <div className="ingredient-search" ref={wrapRef}>
      <label className="sr-only" htmlFor={inputId}>
        Search ingredients
      </label>
      <form className="ingredient-search__form" onSubmit={handleSubmit}>
        <span className="material-symbols-outlined" aria-hidden="true">
          add
        </span>
        <input
          id={inputId}
          type="search"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          onFocus={() => suggestions.length && setOpen(true)}
          placeholder="scribble down an ingredient..."
          autoComplete="off"
        />
        <StickyButton type="submit" variant="dark" disabled={loading}>
          Add
        </StickyButton>
      </form>

      {error ? <p className="ingredient-search__error">{error}</p> : null}

      {open && (loading || suggestions.length > 0) ? (
        <ul className="ingredient-search__suggestions" role="listbox">
          {loading ? (
            <li className="ingredient-search__hint">Searching…</li>
          ) : (
            suggestions.map((ingredient) => {
              const price = formatIngredientPrice(ingredient.price)
              return (
                <li key={ingredient.id}>
                  <button
                    type="button"
                    className="ingredient-search__option"
                    onClick={() => handleSelect(ingredient)}
                  >
                    <span>{ingredient.name}</span>
                    <span className={`label${price.available ? '' : ' is-specialty'}`}>
                      {price.shortText}
                    </span>
                  </button>
                </li>
              )
            })
          )}
        </ul>
      ) : null}
    </div>
  )
}

export default IngredientSearch
