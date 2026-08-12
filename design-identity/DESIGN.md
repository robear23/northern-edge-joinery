# Noba & Stod — Design Identity

> **Source:** https://nobaandstod.co.uk/
> **Extracted:** 2026-08-12
> **Aesthetic:** Editorial (luxury editorial — dark, serif-led, flat, image-forward)

---

## Brand Personality

A dark-first luxury editorial identity built on three colours and two typefaces. The page sits on a warm charcoal (`#2c2e2c`), sections recede into near-black ink (`#131413`), and a single champagne gold (`#dec497`) carries every call to action. Display copy is set in a high-contrast serif (Cormorant) at enormous sizes — 88px hero, 128px display — with negative tracking and 100–120% leading, while all UI, navigation and body text runs in Raleway at just two weights.

The whitespace philosophy is the loudest signal: sections are padded 180px top and bottom, editorial grids use 180px column gaps, and prose is constrained to a 540px measure. Nothing is rounded except buttons, which are full pills; every card, image and panel is sharp-cornered. There is not a single box-shadow in the stylesheet — depth comes entirely from colour contrast and full-bleed photography, never elevation.

Interactions are uniform and restrained: one 300ms transition governs almost everything. Buttons do not darken on hover — they invert, dropping their fill to transparent and switching text and border to gold.

---

## Color System

### Core Palette

| Token | Hex | RGB | HSL | Semantic Role |
|-------|-----|-----|-----|---------------|
| `--color-primary` | `#dec497` | `rgb(222, 196, 151)` | `hsl(38, 52%, 73%)` | Champagne gold — CTAs, hover states, monogram, CTA panels |
| `--color-primary-dark` | `#cfa968` | `rgb(207, 169, 104)` | `hsl(38, 52%, 61%)` | Pressed / darker gold *(inferred — see Usage Rules)* |
| `--color-primary-light` | `#eddec5` | `rgb(237, 222, 197)` | `hsl(38, 53%, 85%)` | Tinted gold wash, focus rings *(inferred)* |
| `--color-secondary` | `#f0eeeb` | `rgb(240, 238, 235)` | `hsl(36, 14%, 93%)` | Warm bone — headings and text on dark, light panels |
| `--color-accent` | `#ceccc5` | `rgb(206, 204, 197)` | `hsl(47, 8%, 79%)` | Warm stone — default body text, hairline rules at 30% alpha |
| `--color-ink` | `#131413` | `rgb(19, 20, 19)` | `hsl(120, 3%, 8%)` | Deepest ink — section grounds, footer, text on gold |
| `--color-charcoal` | `#2c2e2c` | `rgb(44, 46, 44)` | `hsl(120, 2%, 18%)` | Page background |
| `--color-white` | `#ffffff` | `rgb(255, 255, 255)` | `hsl(0, 0%, 100%)` | Default outline-button text and nav links — deliberately *not* the warm bone |

### Neutral Scale

Warm, desaturated stone-to-ink ramp. **Note the inversion:** this is a dark-first system — 800/900 are the page grounds and 100/300 are the text colours.

| Token | Hex | Use | Provenance |
|-------|-----|-----|------------|
| `--color-neutral-50` | `#f9f9f9` | Pure light panels (rare) | extracted |
| `--color-neutral-100` | `#f0eeeb` | **Heading text on dark**; light section background | extracted |
| `--color-neutral-200` | `#dfddd8` | Light-panel dividers | inferred |
| `--color-neutral-300` | `#ceccc5` | **Default body text on dark** | extracted |
| `--color-neutral-400` | `#a2a29e` | Muted / de-emphasised text | inferred |
| `--color-neutral-500` | `#777777` | Placeholder text | extracted |
| `--color-neutral-600` | `#606060` | Disabled text | inferred |
| `--color-neutral-700` | `#494949` | Low-contrast display text, inactive states | extracted |
| `--color-neutral-800` | `#2c2e2c` | **Page background** | extracted |
| `--color-neutral-900` | `#131413` | **Section / footer background**, text on gold | extracted |

### Semantic Colors

Only the error colour is theme-authored. The rest come from the Contact Form 7 plugin's stylesheet — they render on the live site's form validation but were not chosen by the brand. Restyle them if you want a fully on-brand system.

| Token | Hex | Use | Provenance |
|-------|-----|-----|------------|
| `--color-success` | `#46b450` | Mail-sent confirmation | Contact Form 7 default |
| `--color-warning` | `#ffb900` | Validation warning | Contact Form 7 default |
| `--color-error` | `#e74c3c` | Invalid field, destructive | theme-authored |
| `--color-error-alt` | `#dc3232` | Form submission error | Contact Form 7 default |
| `--color-info` | `#00a0d2` | Informational notice | Contact Form 7 default |

### Surface Colors

| Token | Hex | Use |
|-------|-----|-----|
| `--color-surface` | `#2c2e2c` | Page background (`body`) |
| `--color-surface-sunken` | `#131413` | Section grounds (`.bg-color-basic`), footer, swiper controls |
| `--color-surface-gold` | `#dec497` | Full-width CTA panel (carries a subtle wood-grain contour pattern) |
| `--color-surface-light` | `#f0eeeb` | Inverted light sections |
| `--color-surface-overlay` | `rgba(0, 0, 0, 0.4)` | Image scrim over hero photography |

### Alpha Values

The source leans on alpha compositing rather than extra solid colours. These exact values recur:

| Value | Use |
|-------|-----|
| `rgba(255, 255, 255, 0.3)` | Default button border, nav top/bottom hairlines |
| `rgba(240, 238, 235, 0.3)` | Bone hairline rules under section labels |
| `rgba(206, 204, 197, 0.3)` | Stone hairline rules |
| `rgba(19, 20, 19, 0.7)` | Heavy ink scrim |
| `rgba(19, 20, 19, 0.2)` | Light ink scrim |
| `rgba(0, 0, 0, 0.4)` | Hero image overlay |

### Usage Rules

- **Gold is the only accent.** It appears on CTA fills, hover states, the monogram and the closing CTA panel — nowhere else. Do not introduce a second accent hue.
- **Buttons invert, they do not darken.** The source has no darker-gold hover state; `.btn--filled:hover` drops the background to `transparent` and switches text to gold. `--color-primary-dark` is provided as an inferred convenience token — using it will deviate from the source behaviour.
- **Never place gold text on the charcoal page background** at body size. Gold is reserved for large display text, pill fills and hairline accents; body copy is always `--color-neutral-300`.
- **Text on gold is always ink** (`#131413`), never white.
- **Hairlines are always a 30% alpha of an existing colour**, never a solid neutral.
- **Contrast note:** `--color-neutral-700` (`#494949`) on the charcoal page ground yields roughly 1.9:1 — well below WCAG AA. The source uses it deliberately for oversized decorative display prose. Do not use it for anything at body size.

---

## Typography

### Font Stack

| Role | Family | Weights | Import |
|------|--------|---------|--------|
| Display / Headings | Cormorant | 400 only | Self-hosted `cormorant_regular.woff2` (`font-display: swap`) |
| Body / UI | Raleway | 400, 500 | Self-hosted `raleway_regular.woff2`, `raleway_medium.woff2` |
| Monospace | *(none)* | — | Falls through to the browser `monospace` default |

> **Source quirk — read before copying:** the theme declares the serif as `font-family: "Сormorant"`, where the leading character is **U+0421 CYRILLIC CAPITAL LETTER ES**, not a Latin `C`. It only works because the `@font-face` rule repeats the same mis-typed string. The tokens in this kit use the **correct Latin spelling `Cormorant`**, which is the real Google Fonts family. If you self-host, name the family consistently in Latin; if you load from Google Fonts, use:
>
> ```
> @import url('https://fonts.googleapis.com/css2?family=Cormorant:wght@400&family=Raleway:wght@400;500&display=swap');
> ```

### Type Scale

Sizes marked ✎ are the ones the source actually uses; the ramp is otherwise continuous. Letter-spacing follows a strict rule: **display sizes track at `-0.02em`, body and UI sizes at `-0.01em`.**

| Token | px | rem | Family | Weight | Line Height | Letter Spacing | Use |
|-------|----|-----|--------|--------|-------------|----------------|-----|
| `--text-xs` | 12px ✎ | 0.75rem | Raleway | 400 | 1.5 | -0.01em | Captions, legal, footer meta |
| `--text-sm` | 14px ✎ | 0.875rem | Raleway | 500 | 1.5 | 0 | **Nav links, buttons — uppercase** |
| `--text-base` | 16px ✎ | 1rem | Raleway | 400 | 1.6 | -0.01em | Body copy |
| `--text-lg` | 18px ✎ | 1.125rem | Raleway | 400 | 1.5 | -0.01em | Lead paragraphs |
| `--text-xl` | 20px ✎ | 1.25rem | Raleway | 400 | 1.5 | -0.01em | Large body, mobile nav (21px) |
| `--text-2xl` | 24px ✎ | 1.5rem | Cormorant | 400 | 1.2 | -0.02em | H4 |
| `--text-3xl` | 30px ✎ | 1.875rem | Cormorant | 400 | 1.2 | -0.02em | H3, mobile H2 |
| `--text-4xl` | 38px ✎ | 2.375rem | Cormorant | 400 | 1.2 | -0.02em | H2 |
| `--text-5xl` | 48px ✎ | 3rem | Cormorant | 400 | 1.2 | -0.02em | **Primary section heading** |
| `--text-6xl` | 66px ✎ | 4.125rem | Cormorant | 400 | 1.0 | -0.02em | Large section display |
| `--text-7xl` | 88px ✎ | 5.5rem | Cormorant | 400 | 1.0 | -0.02em | **Hero heading** |
| `--text-8xl` | 128px ✎ | 8rem | Cormorant | 400 | 1.0 | -0.02em | Oversized editorial display |

### Typographic Rules

- **There is no bold in this system.** Only two weights are loaded: Raleway 400 and 500, and Cormorant 400 only. Setting a heading to 600/700 will trigger synthetic faux-bold and immediately break the identity. Emphasis is created with *size* and *colour*, never weight.
- **Serif for statement, sans for function.** Cormorant is used exclusively for headings and large editorial prose. Raleway handles navigation, buttons, body copy, labels and captions. They never swap roles.
- **Uppercase labels track at 0**, not positive. Nav links and buttons are `text-transform: uppercase` at 14px/500 with no added letter-spacing.
- **Section eyebrows** are small Raleway labels sitting above a 1px hairline rule at 30% alpha, spanning roughly a third of the column.
- Body sets at `line-height: 1.6`; UI at `1.5`; headings at `1.2`; hero and display at `1.0`.

---

## Spacing System

**Base unit:** 4px, with an 8px working rhythm and a distinctive large-format section scale.

| Token | Value | Common Use |
|-------|-------|------------|
| `--space-1` | 4px | Tightest inline gaps |
| `--space-2` | 8px | Icon gaps |
| `--space-3` | 12px | Compact padding |
| `--space-4` | 16px | Standard component padding |
| `--space-5` | 20px | Button horizontal padding |
| `--space-6` | 24px | Mobile nav padding, burger icon width |
| `--space-7` | 28px | Medium gaps |
| `--space-8` | 32px | Component spacing |
| `--space-10` | 40px | List item separation |
| `--space-12` | 50px | Large component spacing |
| `--space-14` | 56px | Header top padding (desktop) |
| `--space-18` | 72px | Large block spacing |
| `--space-20` | 80px | Section gap (compact), desktop nav gap |
| `--space-22` | 90px | Large block spacing |
| `--space-25` | 100px | Section gap (medium), sticky offset |
| `--space-31` | 125px | Extra-large block spacing |
| `--space-45` | 180px | **Signature section rhythm** |

### Named Layout Tokens

The distinctive values, given semantic names because they carry the identity:

| Token | Value | Use |
|-------|-------|-----|
| `--gutter` | 15px | Container side padding |
| `--header-pad` | 56px | Header top padding at rest (collapses to 14px on scroll) |
| `--header-height` | 100px | Scrolled header / nav bar height |
| `--section-y` | 180px | Standard section padding top and bottom (`.pt-180` / `.pb-180`) |
| `--section-y-md` | 100px | Reduced section rhythm |
| `--section-y-sm` | 80px | Compact section rhythm |
| `--grid-gap-x` | 180px | Editorial grid column gap (3-col news archive, how-we-work) |
| `--grid-gap-y` | 80px | Editorial grid row gap |

> The 180px section rhythm is the single most identity-defining measurement on this site. Reducing it to a conventional 64–96px will make a rebuild feel like a different, cheaper brand.

---

## Shape

**This design is deliberately sharp.** No card, image, panel or input carries a radius. The only curved elements are pill-shaped buttons and one circular cursor.

| Token | Value | Use |
|-------|-------|-----|
| `--radius-none` | 0 | **The default** — cards, images, panels, sections, inputs |
| `--radius-sm` | 0 | Intentionally 0 — kept for scale compatibility |
| `--radius-md` | 0 | Intentionally 0 — kept for scale compatibility |
| `--radius-lg` | 0 | Intentionally 0 — kept for scale compatibility |
| `--radius-xl` | 0 | Intentionally 0 — kept for scale compatibility |
| `--radius-2xl` | 0 | Intentionally 0 — kept for scale compatibility |
| `--radius-pill` | 71px | **Buttons** (`.btn`) — extracted verbatim |
| `--radius-control` | 50px | Swiper control cluster |
| `--radius-circle` | 50% | Custom cursor, avatars |
| `--radius-full` | 9999px | Equivalent pill for arbitrary widths |

### Borders

| Token | Value | Use |
|-------|-------|-----|
| `--border-width` | 1px | The only border width in the system |
| `--border-hairline` | `1px solid rgba(255, 255, 255, 0.3)` | Button outlines, nav rules |
| `--rule-height` | 2px | Burger icon bars |

---

## Shadows (Elevation)

**The source contains no shadows.** The only `box-shadow` declarations in the entire stylesheet are `box-shadow: none`. Depth is expressed through colour contrast and full-bleed photography.

| Token | Value | Use |
|-------|-------|-----|
| `--shadow-none` | `none` | **The system default — use this** |

If you genuinely need elevation in an extension of this system, the tokens below are **inferred, not extracted**. They are tinted with the brand ink (`19, 20, 19`) rather than pure black so they stay warm. Using them departs from the source design.

| Token | Value | Use |
|-------|-------|-----|
| `--shadow-sm` | `0 1px 3px 0 rgba(19,20,19,0.24), 0 1px 2px -1px rgba(19,20,19,0.24)` | *inferred* |
| `--shadow-md` | `0 4px 6px -1px rgba(19,20,19,0.28), 0 2px 4px -2px rgba(19,20,19,0.28)` | *inferred* |
| `--shadow-lg` | `0 10px 15px -3px rgba(19,20,19,0.32), 0 4px 6px -4px rgba(19,20,19,0.32)` | *inferred* |
| `--shadow-xl` | `0 20px 25px -5px rgba(19,20,19,0.38), 0 8px 10px -6px rgba(19,20,19,0.38)` | *inferred* |

---

## Motion

**One duration governs the entire site: 300ms.** It appears 24 times as a bare `transition: .3s` and in every scoped transition (`color .3s`, `opacity .3s ease`, `filter .3s`, `padding-top .3s`, `background-color .3s`, `border-bottom-color .3s`). No other duration exists in the source.

| Token | Value | Easing | Use | Provenance |
|-------|-------|--------|-----|------------|
| `--duration-instant` | 75ms | linear | Immediate feedback | *inferred* |
| `--duration-fast` | 150ms | ease-out | Micro-interactions | *inferred* |
| `--duration-normal` | **300ms** | ease | **The site standard — use this for everything** | extracted |
| `--duration-slow` | 400ms | ease-in-out | Enter / exit | *inferred* |
| `--ease-default` | `ease` | — | The source's implicit default | extracted |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | — | Colour transitions (`color .3s ease-in-out`) | extracted |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | — | Elements entering | *inferred* |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | — | Elements leaving | *inferred* |

### Motion Patterns

- **Image reveal:** images sit at reduced brightness and animate to `brightness(1)` on hover via `transition: filter .3s`.
- **Header collapse:** `padding-top` animates 56px → 14px over 300ms as the page scrolls, with the header height locking to 100px.
- **Nav drawer:** the full-width nav slides from `top: -100px` to `top: 100px` with `opacity` and `visibility` over 300ms.
- **Custom cursor:** a 120px circle in ink with gold text, fading via `opacity .3s ease` over interactive imagery.

---

## Layout & Breakpoints

| Token | Value | Use |
|-------|-------|-----|
| `--container-max` | 1440px | Container max width (`.container`, with 15px gutters) |
| `--container-wide` | 1920px | Full-bleed media ceiling |
| `--measure` | 540px | Prose column max width — the editorial measure |
| `--measure-sm` | 360px | Narrow card text |

### Breakpoints

The source is authored **desktop-first** using `max-width` queries. Both forms are given below; the Tailwind config uses the `min-width` equivalents.

| Token | Source query (`max-width`) | Tailwind (`min-width`) | Use |
|-------|---------------------------|------------------------|-----|
| `--breakpoint-sm` | `767px` / `768px` | `768px` | Mobile → tablet |
| `--breakpoint-md` | `1100px` | `1100px` | Tablet → desktop |
| `--breakpoint-lg` | `1500px` | `1500px` | Desktop |
| `--breakpoint-xl` | `1520px` | `1520px` | Wide desktop |
| `--breakpoint-2xl` | `1920px` | `1920px` | Full-bleed ceiling |

At `≤1100px` the container switches to `calc(100vw - 80px)`, then `calc(100vw - 60px)`, then `calc(100vw - 30px)` at the smallest sizes.

### Z-Index

| Token | Value | Use |
|-------|-------|-----|
| `--z-nav` | 100 | Nav drawer |
| `--z-header` | 101 | Fixed header (above the drawer) |
| `--z-cursor` | 1000 | Custom cursor |

---

## Component Patterns

### Button — Outline (default)

```css
display: flex;
align-items: center;
justify-content: center;
width: max-content;
font-family: var(--font-body);
font-size: var(--text-sm);        /* 14px */
font-weight: var(--font-medium);  /* 500 */
line-height: 1.5;
text-transform: uppercase;
color: #ffffff;
background: transparent;
border: 1px solid rgba(255, 255, 255, 0.3);
border-radius: var(--radius-pill); /* 71px */
padding: 10px 20px;
transition: 0.3s;
```
```css
/* Hover — border and text go gold, background stays transparent */
.btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}
```

### Button — Filled Gold (primary CTA)

```css
background-color: var(--color-primary);   /* #dec497 */
border: 1px solid var(--color-primary);
color: var(--color-neutral-900);          /* #131413 */
border-radius: var(--radius-pill);
padding: 10px 20px;
font-size: var(--text-sm);
font-weight: var(--font-medium);
text-transform: uppercase;
transition: 0.3s;
```
```css
/* Hover — INVERTS to outline. Does not darken. */
.btn--filled:hover {
  background-color: transparent;
  color: var(--color-primary);
}
```

### Button — Filled Ink (on gold panels)

```css
background-color: var(--color-neutral-900); /* #131413 */
border: 1px solid var(--color-neutral-900);
color: var(--color-neutral-100);            /* #f0eeeb */
border-radius: var(--radius-pill);
padding: 10px 20px;
transition: 0.3s;
```
```css
.btn--filled--2:hover {
  background-color: transparent;
  color: var(--color-neutral-900);
  border-color: var(--color-neutral-900);
}
```

### Section Eyebrow (label + rule)

```css
/* The recurring "About us" / "Services" label above each section */
.section-label {
  font-family: var(--font-body);
  font-size: var(--text-xs);       /* 12px */
  font-weight: var(--font-normal);
  color: var(--color-neutral-100);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid rgba(240, 238, 235, 0.3);
  max-width: 360px;
}
```

### Card / Portfolio Item

```css
/* Sharp corners, no shadow, hairline border, image brightens on hover */
background: transparent;
border: 1px solid rgba(206, 204, 197, 0.3);
border-radius: var(--radius-none);  /* 0 — never rounded */
box-shadow: var(--shadow-none);     /* none */
transition: 0.3s;
```
```css
.card:hover { border-color: var(--color-neutral-100); }
.card:hover img { filter: brightness(1); }
.card:hover .desc { color: var(--color-neutral-100); }
.card:not(:last-child) { margin-bottom: 40px; }
```

### Editorial Prose Block

```css
font-family: var(--font-heading);   /* Cormorant */
font-size: var(--text-5xl);         /* 48px */
font-weight: var(--font-normal);    /* 400 */
line-height: 1.2;
letter-spacing: -0.02em;
max-width: var(--measure);          /* 540px */
color: var(--color-neutral-100);
margin-top: 0;
margin-bottom: 0;
```

### Navigation

- **Background:** transparent at rest; the drawer sits on the page ground with `1px solid rgba(255,255,255,0.3)` rules top and bottom
- **Header height:** 100px when scrolled; `padding-top` 56px → 14px on scroll (300ms)
- **Layout:** 3-column CSS grid (`1fr 1fr 1fr`) — links left, logo centre, phone + CTA right
- **Link style:** Raleway, 14px, weight 500, `line-height: 1.5`, uppercase, `#ffffff`
- **Desktop drawer:** flex row, `gap: 80px`, centred, full viewport width, 100px tall
- **Mobile drawer:** flex column, `gap: 15px`, `padding: 24px`, left-aligned, links at 21px
- **Position:** `position: fixed; top: 0; left: 0; z-index: 101`

### Closing CTA Panel

```css
/* Full-width gold panel with a subtle wood-grain contour pattern */
background-color: var(--color-surface-gold);  /* #dec497 */
border-radius: var(--radius-none);
padding: var(--section-y-md) 0;               /* 100px */
text-align: center;
color: var(--color-neutral-900);
```
Heading sets in Cormorant at `--text-6xl` (66px), supporting copy in Raleway at `--text-base`, and the button is the **Filled Ink** variant.

---

## Dark Mode

**Not detected — and not applicable.** There are no `prefers-color-scheme` blocks, no `[data-theme]` selectors and no `.dark` class overrides anywhere in the source (verified across the theme stylesheet, the theme root stylesheet, the Contact Form 7 stylesheet and the page HTML).

This site is **dark-only by design**. The dark palette is not a mode — it *is* the brand. If you need a light variant, invert deliberately using the tokens already in this system:

- Page ground → `--color-neutral-100` (`#f0eeeb`)
- Body text → `--color-neutral-900` (`#131413`)
- Primary CTA → unchanged gold with ink text (the **Filled Ink** button already exists for exactly this case)

The source itself does this for the closing CTA panel, so a light section is on-brand — a full light *mode* is not.

---

## Reproduction Checklist

Getting these five things right reproduces most of the identity; getting any of them wrong breaks it:

1. **180px section padding.** Not 64px, not 96px.
2. **Only two weights — 400 and 500.** No bold, anywhere.
3. **Zero border-radius on everything except pill buttons.**
4. **No shadows at all.**
5. **One 300ms transition, and buttons invert rather than darken on hover.**

---

## Screenshot

`screenshot.png` — full-page capture at 1280×9991px via Playwright (Chromium), 2026-08-12.

---

## Extraction Notes & Limitations

- **Source stylesheets:** `front-end/dist/css/style.min.css` (41KB, compiled — the sole source of the design system), `style.css` (3KB, WordPress theme header), and Contact Form 7 `styles.css` (3KB, plugin defaults).
- **No CSS custom properties exist in the source.** The theme is compiled SCSS with hardcoded literal values throughout; every token in this kit was recovered by frequency analysis and selector-context inspection, then verified against the rendered screenshot.
- **Swiper 11** (`cdn.jsdelivr.net/npm/swiper@11`) supplies carousel styles. Its default tokens are not part of the brand system and were excluded.
- **Fonts are self-hosted woff2** at `front-end/fonts/`. Only three files are loaded: `cormorant_regular.woff2`, `raleway_regular.woff2`, `raleway_medium.woff2`. The font binaries were not downloaded.
- **Logo:** wordmark and monogram are inline SVG in the header. Favicon: `https://nobaandstod.co.uk/wp-content/uploads/2024/11/favicon-1.png` (248×248).
- The gold CTA panel's contour/wood-grain texture is a background image asset, not CSS — reproduce it separately if needed.

---

## How to Use This File

Load this file into your AI context. Reference tokens by their `--token-name` when writing CSS or component code. For Tailwind projects, use `tailwind.config.js` alongside this file. For raw CSS, paste `tokens.css` into your project root stylesheet. Verify any rebuild against `screenshot.png`.
