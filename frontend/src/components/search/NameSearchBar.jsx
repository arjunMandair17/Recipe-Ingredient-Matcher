import { useId } from 'react'
import WashiTape from '../ui/WashiTape.jsx'
import './NameSearchBar.css'

/**
 * Underline-style search input for recipe name queries.
 */
function NameSearchBar({ value, onChange, onSubmit, placeholder }) {
  const inputId = useId()

  return (
    <div className="name-search-shell">
      <WashiTape
        color="yellow"
        width="5.5rem"
        className="name-search__tape"
        style={{ top: 0, left: '50%', transform: 'translateX(-50%) rotate(-2deg)' }}
      />
      <form
        className="name-search paper paper--torn"
        onSubmit={(event) => {
          event.preventDefault()
          onSubmit?.(value)
        }}
      >
        <label className="sr-only" htmlFor={inputId}>
          Search recipes by name
        </label>
        <div className="name-search__row">
          <span className="material-symbols-outlined" aria-hidden="true">
            search
          </span>
          <input
            id={inputId}
            type="search"
            value={value}
            onChange={(event) => onChange?.(event.target.value)}
            placeholder={placeholder ?? 'Search recipes by name...'}
            autoComplete="off"
          />
          <button type="submit" className="name-search__submit label">
            Search
          </button>
        </div>
      </form>
    </div>
  )
}

export default NameSearchBar
