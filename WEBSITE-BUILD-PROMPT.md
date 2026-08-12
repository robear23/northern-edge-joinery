# Build Prompt — Northern Edge Joinery Ltd

> Paste everything below the line into your website builder / coding agent.
> It assumes the agent can read files in this directory.

---

## Mission

Build a complete, production-ready marketing website for **Northern Edge Joinery Ltd**, a bespoke joinery workshop in Leeds, West Yorkshire.

The target is not "a nice small-business site." The target is a site that looks like it was commissioned by a luxury interiors brand — dark, serif-led, image-forward, editorial. The kind of site where the whitespace itself signals that the work is expensive. A visitor should assume this joiner is out of their price range, and want them anyway.

**Reference the design system, do not invent one.** A complete visual identity has already been extracted and lives in `design-identity/`. Read all of it before writing a single line of code.

---

## Step 1 — Load the design system (do this first)

| File | What it is |
|---|---|
| `design-identity/DESIGN.md` | The design brain. Read this in full. It contains the colour law, type scale, spacing rhythm, component CSS, and a five-point reproduction checklist. |
| `design-identity/tokens.css` | CSS custom properties. Paste into the root stylesheet and reference by token name. |
| `design-identity/tokens.json` | W3C DTCG tokens, if your pipeline consumes them. |
| `design-identity/tailwind.config.js` | Pre-built Tailwind theme. Use this if building with Tailwind. |
| `design-identity/screenshot.png` | Full-page visual reference of the source aesthetic. Verify your build against it. |
| `logo.jpg` | The client's logo. See the logo section below — it needs work before use. |
| `business-info.md` | The only source of truth for facts about this business. |

**Never hardcode a hex value that exists as a token.** Write `var(--color-primary)`, not `#dec497`.

---

## Step 2 — The colour law

The palette is three colours and a neutral ramp. It is dark-first: the dark palette *is* the brand, not a mode.

| Role | Token | Hex | Where it goes |
|---|---|---|---|
| Page ground | `--color-charcoal` | `#2c2e2c` | `body` — the default surface |
| Section ground | `--color-ink` | `#131413` | Recessed sections, footer |
| **The only accent** | `--color-primary` | `#dec497` | Champagne gold — CTAs, hover states, the closing panel. Nothing else. |
| Heading text | `--color-neutral-100` | `#f0eeeb` | Warm bone |
| Body text | `--color-neutral-300` | `#ceccc5` | Warm stone |
| Text on gold | `--color-neutral-900` | `#131413` | Always ink. Never white. |

**Rules that are not negotiable:**

- **Gold is the only accent.** Do not introduce a second hue — no blue links, no green success states, no red error text that hasn't been restyled to the system. The champagne gold reads as brass hardware and warm timber, which is why it suits a joiner. Diluting it with a second accent destroys the identity.
- **Never set gold as body text on the charcoal ground.** Gold is for large display type, pill fills, and hairline accents only.
- **Hairlines are always 30% alpha of an existing colour** — `rgba(240, 238, 235, 0.3)` and `rgba(206, 204, 197, 0.3)` recur throughout. Never a solid neutral.
- `--color-neutral-700` (`#494949`) sits at ~1.9:1 on the page ground. It is for oversized decorative display prose **only**. Never at body size.

---

## Step 3 — Reconciling the logo

Read this carefully; there is a real problem to solve.

The supplied `logo.jpg` is a 150×150 raster with a **baked-in solid background**. Sampled values:

- **Logo ground: `#3E3C3D`** (62% of all pixels) — a *neutral* grey.
- **Wordmark: ≈`#E4E2E3`** — a soft near-white, JPEG-blurred, also neutral.

The design system's charcoal is `#2c2e2c` — noticeably **darker and green-tinted**. The logo's grey is lighter and tints slightly magenta. Dropping `logo.jpg` straight onto the page will produce **a visible pale rectangle floating in the header**, and the two greys will fight each other. This is the single most likely way to make an otherwise beautiful build look amateur.

**Required fix, in order of preference:**

1. **Redraw the wordmark as inline SVG.** It is two lines of letterspaced sans-serif caps — "NORTHERN EDGE" over "JOINERY LTD" with short flanking rules either side of the second line. Set the fill to `currentColor` so it inherits `--color-neutral-100` on dark grounds and `--color-ink` on the gold panel. This is a ~30-minute job and it is the correct answer.
2. If SVG is not possible, **knock the background out to a transparent PNG at 2× and 3×**, then recolour the wordmark to exactly `#f0eeeb` so it matches every other heading on the page.

**Do not** add `#3E3C3D` to the palette as a new surface colour. It is a JPEG artefact of the client's export, not a brand decision. The design system already has its greys.

**Note what the logo does *not* contain: gold.** That is fine and intended — the wordmark stays monochrome bone, and the champagne gold does its work everywhere else on the page. Do not tint the logo gold.

---

## Step 4 — The five rules that make or break this build

Straight from the reproduction checklist. Get any one of these wrong and it reads as a different, cheaper brand:

1. **180px section padding, top and bottom.** Not 64px. Not 96px. The `--section-y` rhythm is the single most identity-defining measurement in the system. It collapses to 100px (`--section-y-md`) and 80px (`--section-y-sm`) only where explicitly warranted, and on mobile.
2. **Only two font weights exist: 400 and 500.** Cormorant loads at 400 only; Raleway at 400 and 500. Setting a heading to 600 or 700 triggers synthetic faux-bold and instantly breaks it. **Emphasis comes from size and colour, never weight.**
3. **Zero border-radius on everything** — cards, images, panels, inputs, sections. The *only* curved elements are pill buttons (`--radius-pill`, 71px).
4. **No shadows. Anywhere.** The source stylesheet's only `box-shadow` declarations are `none`. Depth comes from colour contrast and full-bleed photography.
5. **One transition duration: 300ms.** And **buttons invert rather than darken** on hover — a filled gold button drops its background to `transparent` and switches its text and border to gold. It does not go a darker gold.

**Typography roles never swap:** Cormorant (serif) for headings and large editorial prose. Raleway (sans) for nav, buttons, body, labels, captions. Hero heading is 88px Cormorant at `line-height: 1.0`, `letter-spacing: -0.02em`. Prose is constrained to a **540px measure** — never let a paragraph run the full container width.

Google Fonts import:
```
@import url('https://fonts.googleapis.com/css2?family=Cormorant:wght@400&family=Raleway:wght@400;500&display=swap');
```

---

## Step 5 — Business facts (verbatim — this is the only source of truth)

- **Name:** Northern Edge Joinery Ltd
- **Location / service area:** Leeds, West Yorkshire, United Kingdom
- **Email:** info@northernedgejoineryltd.com
- **Instagram:** [@northern_edge_joinery_ltd](https://instagram.com/northern_edge_joinery_ltd) — 97 portfolio posts
- **Proposition:** Crafting high-quality bespoke joinery, custom wardrobes, and tailored fitted furniture solutions.
- **Primary CTA:** "Request a Bespoke Consultation" — secondary: "Get a Free Quote"

**Three services** (these are the portfolio pillars — give each its own block):

1. **Bespoke Joinery** — custom woodworking tailored to unique architectural spaces and individual client specifications.
2. **Custom Fitted Wardrobes** — built-in bedroom storage, walk-in wardrobes, sliding wardrobes, alcove fitting.
3. **Fitted Furniture** — made-to-measure shelving, media walls, home office storage, custom cabinetry.

**Positioning angle:** bespoke and fitted, *not* flat-pack or off-the-shelf. Every piece is made to the millimetre for the room it lives in, which is what makes it worth more than the alternative. Write to that.

### Honesty constraints — read before writing any copy

There is **no phone number** for this business. Do not invent one. Contact is by email form and Instagram DM, and the site must be designed so that this feels deliberate and premium — a consultation request, not a switchboard — rather than like something is missing.

Likewise, **do not fabricate**: testimonials or client quotes, review scores or star ratings, years in business or "established" dates, project counts beyond the 97 Instagram posts, employee numbers, trade accreditations or certifications, awards, or case-study details. None of these are known.

Where the layout wants social proof, either **build the slot and leave a clearly-marked placeholder** for the client to fill, or use what is genuinely true — a real portfolio of 97 completed projects, and work photographed in real Leeds homes. A gorgeous site built on invented credentials is a liability for the client, not an asset.

---

## Step 6 — Page architecture

Single-page scroll with anchored nav, or multi-page — your call, but keep the section sequence.

**Header** — `position: fixed`, transparent at rest, `z-index: 101`. Three-column grid: nav links left, logo centred, CTA right (no phone — the right slot holds the consultation CTA alone). Padding-top animates 56px → 14px on scroll over 300ms, header locking to 100px.

**1. Hero** — full-bleed photograph of finished joinery, `rgba(0,0,0,0.4)` scrim. Heading in Cormorant at 88px. One sentence of Raleway lead copy at 18px, capped to the 540px measure. One filled-gold pill CTA. Nothing else — no stat bars, no logo strips, no scroll indicators cluttering it.

**2. Introduction** — an editorial prose block. Cormorant at 48px, 540px measure, generous asymmetric whitespace. This is where the workshop's philosophy lands: made to measure, made in Leeds, made once and made properly.

**3. Services** — the three pillars. Each gets a large image, a section eyebrow (12px Raleway label above a 30%-alpha hairline), a Cormorant heading, and a short paragraph. Alternate image/text sides down the page. Sharp corners, hairline borders, images sitting at reduced brightness and animating to `brightness(1)` on hover.

**4. Portfolio grid** — the strongest asset this business has. Pull from the 97 Instagram posts. Sharp-cornered, no shadows, hairline `rgba(206,204,197,0.3)` borders, `40px` gutters, image brightens on hover, border goes bone. Include a lightbox. Consider a subtle filter by the three service categories.

**5. Process** — a three or four step "how we work" sequence (consultation → design & measure → workshop build → installation). Use the editorial grid with the signature **180px column gap**. This section does the heavy lifting on trust in the absence of testimonials: it shows the client exactly what buying from them is like.

**6. Closing CTA panel** — full-width **gold** (`#dec497`), 100px vertical padding, centred, text in ink. Cormorant heading at 66px, Raleway supporting copy at 16px, and the **Filled Ink** button variant. This is the one place the page goes bright, and it should feel like the site exhaling.

**7. Contact** — email form (name, email, project type, message), sharp-cornered inputs, hairline borders, no radius. Alongside it: the Leeds/West Yorkshire service area, the email address, and a prominent Instagram link framed as "see the last 97 projects."

**Footer** — ink ground (`#131413`), logo, nav, Instagram, service area, copyright at 12px.

---

## Step 7 — Component specifications

Take these verbatim from `DESIGN.md` — it contains the exact CSS for each:

- **Button, outline (default)** — 14px Raleway 500 uppercase, white, transparent fill, `1px solid rgba(255,255,255,0.3)`, `border-radius: 71px`, `padding: 10px 20px`. Hover: border and text go gold.
- **Button, filled gold (primary CTA)** — gold fill, ink text. Hover: **inverts** to transparent fill with gold text.
- **Button, filled ink (on gold panels)** — ink fill, bone text. Hover: inverts.
- **Section eyebrow** — 12px Raleway 400, bone, `padding-bottom: 16px`, `border-bottom: 1px solid rgba(240,238,235,0.3)`, `max-width: 360px`.
- **Card / portfolio item** — transparent, hairline stone border, zero radius, zero shadow, 300ms transition.
- **Editorial prose block** — Cormorant 48px/1.2, `-0.02em`, 540px measure, bone.

---

## Step 8 — Imagery

Photography carries this design — there are no shadows, no gradients, and no illustration to fall back on. If the images are weak, the site is weak.

Source from the Instagram portfolio. Grade everything consistently: warm, low-contrast, natural light, real interiors. Avoid stock photography of generic "carpentry" — sawdust close-ups and gloved hands holding chisels will undercut the luxury positioning immediately. Show **finished rooms**, not tools.

Full-bleed images cap at 1920px (`--container-wide`). Serve responsive `srcset`, lazy-load everything below the fold, prefer WebP with JPEG fallback.

---

## Step 9 — Technical requirements

- **Stack:** static-first. Astro, Eleventy, or hand-written HTML/CSS/JS. No heavyweight framework is warranted. If using Tailwind, consume the provided `tailwind.config.js`.
- **Responsive:** the source is desktop-first with `max-width` queries at 767px, 1100px, 1500px. Container is 1440px max with 15px gutters, switching to `calc(100vw - 80px)` → `calc(100vw - 60px)` → `calc(100vw - 30px)` as it narrows. Scale the 180px section rhythm down proportionally on mobile — but do not flatten it to 48px. Hero drops from 88px to roughly 48px.
- **Accessibility:** semantic landmarks, visible focus states (use gold), alt text on every portfolio image describing the actual work, form labels properly associated, keyboard-navigable lightbox. Verify body-size text meets WCAG AA against its ground — bone and stone on charcoal both pass comfortably; the decorative `#494949` does not and must stay decorative.
- **Performance:** target Lighthouse 95+. Self-host or preconnect fonts, `font-display: swap`, compress all imagery, inline critical CSS.
- **SEO:** target *bespoke joinery Leeds*, *custom wardrobes West Yorkshire*, *fitted furniture Leeds*, *local joiner West Yorkshire*. Write these into real sentences — never a keyword block. Add `LocalBusiness` schema with the Leeds service area and the email, unique title/meta per page, OpenGraph tags with a portfolio image, and a sitemap.
- **Forms:** the email form needs a real handler (Formspree, Netlify Forms, or similar), client and server-side validation, a success state styled in the system's own colours rather than the Contact Form 7 defaults listed in `DESIGN.md`, and honeypot spam protection.
- **Motion:** respect `prefers-reduced-motion`. Scroll-triggered reveals should be restrained — a fade and a small translate, at 300ms. No parallax, no counters, no carousels that move on their own.

---

## Acceptance checklist

Before calling it done, verify against `design-identity/screenshot.png`:

- [ ] Section padding is 180px, not a conventional 64–96px
- [ ] No element uses font-weight above 500 anywhere in the compiled CSS
- [ ] `grep` the stylesheet for `border-radius` — only pill buttons (71px) and the circular cursor should appear
- [ ] `grep` for `box-shadow` — should return nothing but `none`
- [ ] Every transition is 300ms; filled buttons invert on hover rather than darkening
- [ ] The logo is transparent SVG or knocked-out PNG — **no pale `#3E3C3D` rectangle anywhere on the page**
- [ ] Gold appears only on CTAs, hover states, and the closing panel — nowhere else
- [ ] No paragraph exceeds the 540px measure
- [ ] Zero fabricated facts: no phone number, no invented testimonials, no made-up years or accreditations
- [ ] Lighthouse ≥95 across the board, and the site is fully navigable by keyboard
