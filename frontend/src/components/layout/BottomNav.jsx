import { NavLink } from 'react-router-dom'
import './BottomNav.css'

const links = [
  { to: '/', label: 'Home', icon: 'home', end: true },
  { to: '/match', label: 'Match', icon: 'kitchen' },
  { to: '/search', label: 'Recipes', icon: 'search' },
]

/**
 * Mobile-only bottom navigation for the three main sections.
 */
function BottomNav() {
  return (
    <nav className="bottom-nav" aria-label="Mobile">
      {links.map((link) => (
        <NavLink
          key={link.to}
          to={link.to}
          end={link.end}
          className={({ isActive }) =>
            `bottom-nav__link${isActive ? ' is-active' : ''}`
          }
        >
          <span className="material-symbols-outlined" aria-hidden="true">
            {link.icon}
          </span>
          <span>{link.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}

export default BottomNav
