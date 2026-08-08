import './WashiTape.css'

/**
 * Decorative washi-tape accent used on paper scraps.
 */
function WashiTape({
  color = 'yellow',
  width = '5rem',
  className = '',
  style,
}) {
  return (
    <span
      className={`washi-tape washi-tape--${color} ${className}`.trim()}
      style={{ width, ...style }}
      aria-hidden="true"
    />
  )
}

export default WashiTape
