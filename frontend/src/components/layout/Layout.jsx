import { Outlet } from 'react-router-dom'
import Header from './Header.jsx'
import Footer from './Footer.jsx'
import BottomNav from './BottomNav.jsx'

/**
 * Shared page chrome: header, main outlet, footer, and mobile bottom nav.
 */
function Layout() {
  return (
    <div className="app-shell">
      <Header />
      <main className="app-main">
        <Outlet />
      </main>
      <Footer />
      <BottomNav />
    </div>
  )
}

export default Layout
