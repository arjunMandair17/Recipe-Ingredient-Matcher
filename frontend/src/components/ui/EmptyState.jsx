import './EmptyState.css'

/**
 * Friendly empty / error message for lists and search results.
 */
function EmptyState({ title, message, icon = 'note_stack' }) {
  return (
    <div className="empty-state paper paper-card--padded">
      <span className="material-symbols-outlined" aria-hidden="true">
        {icon}
      </span>
      {title ? <h3 className="headline-md">{title}</h3> : null}
      {message ? <p className="body-muted">{message}</p> : null}
    </div>
  )
}

export default EmptyState
