import './MatchBadge.css'

/**
 * Show API match_type as an exact or partial scrapbook badge.
 */
function MatchBadge({ matchType }) {
  if (!matchType) return null

  const isExact = matchType === 'exact'
  return (
    <div
      className={`match-badge match-badge--${isExact ? 'exact' : 'partial'}`}
      role="status"
    >
      <span className="material-symbols-outlined" aria-hidden="true">
        {isExact ? 'check_circle' : 'contrast'}
      </span>
      <span className="label">
        {isExact ? 'Exact match' : 'Partial match'}
      </span>
    </div>
  )
}

export default MatchBadge
