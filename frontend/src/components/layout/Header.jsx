import { NavLink } from 'react-router-dom'
import './Header.css'

const links = [
  { to: '/', label: 'Home', end: true },
  { to: '/match', label: 'Match' },
  { to: '/search', label: 'Recipes' },
]

/**
 * Top brand bar with desktop navigation (no fridge tab).
 */
function Header() {
  return (
    <header className="site-header">
      <NavLink to="/" className="site-brand">
        Kitchen Scraps
      </NavLink>
      <nav className="site-nav" aria-label="Primary">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              `site-nav__link${isActive ? ' is-active' : ''}`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  )
}

export default Header
