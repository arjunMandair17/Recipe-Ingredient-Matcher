import './StickyButton.css'

/**
 * Sticky-note style button for primary and secondary actions.
 */
function StickyButton({
  children,
  variant = 'primary',
  type = 'button',
  className = '',
  ...props
}) {
  return (
    <button
      type={type}
      className={`sticky-btn sticky-btn--${variant} ${className}`.trim()}
      {...props}
    >
      {children}
    </button>
  )
}

export default StickyButton
