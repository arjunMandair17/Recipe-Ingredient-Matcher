import WashiTape from './WashiTape.jsx'
import './PaperCard.css'

/**
 * Paper scrap container with optional torn edge and overhanging tape.
 * Tape sits outside the masked paper so it is not clipped.
 */
function PaperCard({
  children,
  className = '',
  torn = false,
  tilt = '',
  tape,
  padding = true,
}) {
  const paperClasses = [
    'paper',
    'paper-card',
    torn ? 'paper--torn' : '',
    padding ? 'paper-card--padded' : '',
  ]
    .filter(Boolean)
    .join(' ')

  const shellClasses = ['paper-shell', tilt, className].filter(Boolean).join(' ')

  return (
    <div className={shellClasses}>
      {tape ? (
        <WashiTape
          color={tape.color}
          width={tape.width}
          className={tape.className}
          style={tape.style}
        />
      ) : null}
      <div className={paperClasses}>{children}</div>
    </div>
  )
}

export default PaperCard
