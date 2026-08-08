---
name: Kitchen Scraps & Notes
colors:
  surface: '#fbf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fbf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae8e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#42493e'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0f0'
  outline: '#72796e'
  outline-variant: '#c2c9bb'
  surface-tint: '#3b6934'
  primary: '#154212'
  on-primary: '#ffffff'
  primary-container: '#2d5a27'
  on-primary-container: '#9dd090'
  inverse-primary: '#a1d494'
  secondary: '#b6171e'
  on-secondary: '#ffffff'
  secondary-container: '#da3433'
  on-secondary-container: '#fffbff'
  tertiary: '#705d00'
  on-tertiary: '#ffffff'
  tertiary-container: '#caa910'
  on-tertiary-container: '#4c3e00'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bcf0ae'
  primary-fixed-dim: '#a1d494'
  on-primary-fixed: '#002201'
  on-primary-fixed-variant: '#23501e'
  secondary-fixed: '#ffdad6'
  secondary-fixed-dim: '#ffb3ac'
  on-secondary-fixed: '#410003'
  on-secondary-fixed-variant: '#930010'
  tertiary-fixed: '#ffe174'
  tertiary-fixed-dim: '#e7c433'
  on-tertiary-fixed: '#221b00'
  on-tertiary-fixed-variant: '#554500'
  background: '#fbf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
typography:
  headline-xl:
    fontFamily: Bricolage Grotesque
    fontSize: 40px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Bricolage Grotesque
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Bricolage Grotesque
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  body-md:
    fontFamily: Bricolage Grotesque
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Work Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  data-number:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.0'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  paper-padding: 24px
---

## Brand & Style
The brand personality is tactile, domestic, and warm—evoking the organized chaos of a home kitchen. It targets home cooks who find digital recipe apps too clinical. The emotional response should be one of "effortless inspiration," like finding a cherished family recipe tucked into a cookbook.

The design style is **Tactile / Skeuomorphic** with a lean toward **Minimalism**. It uses physical metaphors—paper scraps, washi tape, and pencil markings—to create a "layered" interface. While it mimics a physical refrigerator or corkboard, it maintains high-fidelity usability by ensuring alignment and legibility are never sacrificed for the aesthetic.

## Colors
The palette is rooted in the "Kitchen Cream" (`#FDFCF0`) of a paper scrap. 
- **Primary:** "Leafy Green" (`#2D5A27`) is used for success states and primary navigation, representing fresh produce.
- **Secondary:** "Tomato Red" (`#D32F2F`) is used for alerts, hearting recipes, and accents.
- **Tertiary:** "Washi Yellow" (`#F4D03F` at 60% opacity) is used for highlight effects and "taped" accents.
- **Neutral:** "Pencil Grey" (`#333333`) is the primary ink color, providing high contrast without the harshness of pure black.
- **Surface:** The global background should be a very light cool grey (`#F2F2F2`) to simulate the enamel of a refrigerator door.

## Typography
This design system uses a dual-font strategy. **Bricolage Grotesque** provides the "handwritten" charm; its quirky, expressive terminals mimic ink on paper while maintaining excellent digital legibility. It is used for all narrative and structural content.

**Work Sans** serves as the technical companion. Its neutral, systematic forms are used for prices, cooking times, calorie counts, and button labels—ensuring that critical data is processed quickly by the user. 

Headlines should occasionally use a "slight tilt" (1-2 degrees) in CSS to enhance the "taped-on" feel.

## Layout & Spacing
The layout uses a **Fluid Grid** that mimics a collection of notes on a magnetic surface. Elements are not strictly aligned to a rigid grid but follow a 12-column structure with generous gutters (`24px`).

- **Mobile:** A single-column "stack" of paper scraps.
- **Desktop:** A masonry-style layout that allows cards of different heights to sit side-by-side, mimicking a bulletin board.
- **Internal Spacing:** Content inside "paper" components should use `24px` padding to ensure text doesn't hit the "torn" edges of the container.

## Elevation & Depth
Depth is achieved through **Tonal Layers** and **Ambient Shadows**. 
1. **Level 0 (The Fridge):** The base background layer, solid and flat.
2. **Level 1 (The Note):** The paper scrap. It uses a very subtle, soft shadow (`offset: 2px 2px, blur: 4px, color: rgba(0,0,0,0.05)`) to appear slightly lifted.
3. **Level 2 (The Tape):** Semi-transparent yellow overlays that appear to "hold" the Level 1 notes to Level 0.
4. **Level 3 (Interactive):** When hovered or dragged, paper scraps should lift higher with a larger, more diffused shadow to indicate interactivity.

Avoid using heavy borders; use the contrast between the cream paper and the grey background to define boundaries.

## Shapes
Shapes are "imperfectly geometric." While the base `roundedness` is set to `1` (Soft), individual components should use CSS `clip-path` or SVG masks to create "torn edge" effects on the bottom or top of containers. 

Buttons should feel like "sticky notes" (square with a tiny lift at one corner) or "postage stamps" (perforated edges). Accents like "Washi Tape" are rectangular but should have irregular, jagged ends.

## Components
- **Paper Cards:** The primary container. Use a subtle paper texture SVG overlay. The bottom edge should be slightly irregular or "torn."
- **Sticky Note Buttons:** Primary actions use the Tertiary color (Yellow). They are square or rectangular with a slight drop shadow. Text is uppercase **Work Sans**.
- **Underline Search:** Instead of a boxed input, use a simple Pencil Grey horizontal line with a handwritten-style placeholder text.
- **Washi Chips:** Category tags (e.g., "Vegan," "15-min") look like small strips of semi-transparent colored tape.
- **Checklists:** Use a custom "X" mark or "Circle" that looks like a hand-drawn pencil stroke for ingredients.
- **The "Fridge Magnet" Toggle:** Switch components should look like small colorful plastic magnets that slide across a horizontal path.
- **Photo Scraps:** Food photography should have a thin white border (Polaroid style) and appear "taped" onto the recipe card.