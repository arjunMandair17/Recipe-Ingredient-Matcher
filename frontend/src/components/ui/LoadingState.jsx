import './LoadingState.css'

/**
 * Inline loading message for async API requests.
 */
function LoadingState({ message = 'Looking through the scraps…' }) {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <span className="material-symbols-outlined loading-state__icon" aria-hidden="true">
        progress_activity
      </span>
      <p>{message}</p>
    </div>
  )
}

export default LoadingState
