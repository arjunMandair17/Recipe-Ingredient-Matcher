import { useNavigate } from 'react-router-dom'
import PaperCard from '../components/ui/PaperCard.jsx'
import StickyButton from '../components/ui/StickyButton.jsx'
import WashiTape from '../components/ui/WashiTape.jsx'
import './HomePage.css'

const HERO_IMAGE =
  'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=1200&q=80'

/**
 * Landing page: brand-forward hero and links into the two search flows.
 */
function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="home-page">
      <section className="home-hero">
        <div className="home-hero__copy">
          <PaperCard
            torn
            tape={{
              color: 'yellow',
              width: '6rem',
              style: { top: 0, left: '1rem' },
            }}
          >
            <p className="home-hero__brand label">Kitchen Scraps</p>
            <h1 className="headline-xl home-hero__title">Cook with what you have.</h1>
            <p className="body-muted home-hero__lede">
              Match recipes to ingredients in your kitchen, or search by name —
              exact and partial matches included.
            </p>
            <div className="home-hero__actions">
              <StickyButton variant="primary" onClick={() => navigate('/match')}>
                Match ingredients
              </StickyButton>
              <StickyButton variant="secondary" onClick={() => navigate('/search')}>
                <span className="material-symbols-outlined" aria-hidden="true">
                  search
                </span>
                Search recipes
              </StickyButton>
            </div>
          </PaperCard>
        </div>

        <div className="home-hero__media">
          <WashiTape
            color="green"
            width="7rem"
            style={{
              top: '-0.5rem',
              left: '50%',
              transform: 'translateX(-50%) rotate(1deg)',
            }}
          />
          <img
            className="home-hero__photo"
            src={HERO_IMAGE}
            alt="A rustic pot of vegetable stew on a wooden kitchen counter"
          />
        </div>
      </section>

      <section className="home-how" aria-labelledby="how-heading">
        <div className="home-how__heading">
          <WashiTape
            color="yellow"
            width="4.5rem"
            className="home-how__tape"
            style={{ top: 0, left: '50%', transform: 'translateX(-50%)' }}
          />
          <h2 id="how-heading" className="headline-lg">
            How it works
          </h2>
        </div>

        <div className="home-how__grid">
          <PaperCard
            tilt="tilt-n1"
            tape={{ color: 'green', width: '4rem', style: { top: 0, right: '1rem' } }}
          >
            <span className="material-symbols-outlined home-how__icon" aria-hidden="true">
              kitchen
            </span>
            <h3 className="headline-md">Match your scraps</h3>
            <p className="body-muted">
              Pick ingredients from the pantry database. We return recipes with
              exact or partial matches for each hit.
            </p>
            <button
              type="button"
              className="home-how__link label"
              onClick={() => navigate('/match')}
            >
              Open matcher →
            </button>
          </PaperCard>

          <PaperCard
            tilt="tilt-1"
            tape={{ color: 'yellow', width: '4rem', style: { top: 0, right: '1rem' } }}
          >
            <span className="material-symbols-outlined home-how__icon" aria-hidden="true">
              search
            </span>
            <h3 className="headline-md">Search by name</h3>
            <p className="body-muted">
              Know the dish? Search recipes by title and open full instructions
              plus nested ingredients.
            </p>
            <button
              type="button"
              className="home-how__link label"
              onClick={() => navigate('/search')}
            >
              Open search →
            </button>
          </PaperCard>
        </div>
      </section>

      <section className="home-price-note" aria-labelledby="price-note-heading">
        <PaperCard
          torn
          tilt="tilt-n1"
          className="home-price-note__card"
          tape={{
            color: 'pink',
            width: '5rem',
            style: { top: 0, left: '50%', transform: 'translateX(-50%) rotate(-1deg)' },
          }}
        >
          <span
            className="material-symbols-outlined home-price-note__icon"
            aria-hidden="true"
          >
            info
          </span>
          <h2 id="price-note-heading" className="headline-md">
            A note on prices
          </h2>
          <p className="body-muted">
            Ingredient prices may be inaccurate. Many were scraped from different
            sources and then normalized into a single value, so treat them as rough
            guides — not exact store prices. Items without a known price are marked
            as specialty items.
          </p>
        </PaperCard>
      </section>
    </div>
  )
}

export default HomePage
