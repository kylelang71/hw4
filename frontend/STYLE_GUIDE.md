# Style Guide

Reference: visual style review of [yalebulldogblue.com](https://yalebulldogblue.com/). Use this as the styling guide for the rest of this project.

## Color Palette

- **Yale Blue / Navy** — dominant brand color, used across navigation, buttons, product cards, and headline text
- **White** — primary background and contrast element
- **Gold/Yellow accents** — traditional Yale institutional accent color, used sparingly (logo elements, highlights)
- **Neutral grays** — secondary text, dividers, muted UI elements

## Typography

- Clean, modern sans-serif throughout
- Large, bold headings for section titles (e.g. "Big Pride, Big Yale")
- Medium-weight text for product/content names
- Smaller regular-weight text for descriptions, prices, and navigation items
- Maintain a consistent type scale across device sizes

## Layout Patterns

**Header/Navigation**
- Top nav bar with logo on the left, links/icons on the right (search, login, cart-equivalent)
- Supports multi-level dropdowns for grouped categories
- Collapses to a hamburger menu on mobile

**Content Grid**
- Content/products arranged in a responsive grid (4-5 columns on desktop, fewer on smaller screens)
- Consistent card styling: image, name, price/details
- Secondary actions (e.g. "Quick shop," "View product") appear on hover or below the image

**Product Card Contents (order, top to bottom)**
1. Product thumbnail image
2. Product title (as a link)
3. Short material/fit detail line (e.g. "100% Organic Cotton Front Pouch Pocket, Oversized Relaxed Fit")
4. Price (shown as a single value, or a range when the product has variant pricing)
5. "Quick shop" link/action
6. "Choose options" button

- No color swatches, size indicators, star ratings/review counts, or vendor names are shown directly on the card — detail is kept minimal and price/fit-focused
- Cards follow this same structure consistently across the whole catalogue

## Buttons & Links

- Primary buttons: navy background, white text
- Secondary actions: outline or text-only style
- Hover states lighten the background or add a subtle shadow
- Consistent styling for call-to-action phrases ("Shop All," "View product")

## Imagery

- Clean photography against neutral backgrounds
- Multiple angles/views for products where relevant
- Lifestyle banners emphasizing school pride

## Overall Tone

Heritage-driven and school-pride-focused, balancing institutional authority (Yale Blue, collegiate branding) with an approachable, premium e-commerce feel.

## Application to Campus Customs

- Navbar: navy background, white text, bold/underline on active link (already implemented in [Navbar.css](src/components/Navbar.css))
- Primary buttons: navy fill, white text, subtle hover lightening
- Secondary buttons/links: outline or text-only navy
- Product grid: card-based layout with image, name, price
- Product card content, top to bottom: thumbnail image → product name → short description/fit detail line → price → "Quick shop" link → "Choose options"/add-to-cart button
- Keep product cards minimal: no swatches, ratings, or vendor labels — rely on `catalogue.name`, `catalogue.description`, and `catalogue.price` from the database
- Accent color (gold) reserved for highlights/badges, not large surfaces
- Keep typography clean sans-serif with a clear heading/body hierarchy
