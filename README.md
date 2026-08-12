# Northern Edge Joinery Ltd — website

A static marketing site for a bespoke joinery workshop in Leeds, West Yorkshire.
Dark, serif-led, image-forward — built against the design system in
`design-identity/`.

No framework, no build step, no dependencies. `site/` is the deployable
artefact: plain HTML, one stylesheet pair, one script.

---

## Run it locally

```bash
python server.py            # http://localhost:4321
python server.py 8080       # or pick a port
```

`server.py` serves `site/` **and** implements `POST /api/enquiry` with the same
server-side validation as production, so the contact form works end to end
locally. Submissions append to `enquiries.log`.

Any static server will serve the pages, but the form will fail without the
`/api/enquiry` route.

---

## Layout

```
site/                     the deployable site
  index.html              single-page scroll: hero → intro → services →
                          portfolio → process → gold CTA → contact → footer
  services/*.html         three service pages, one per SEO cluster
  thank-you.html          no-JS form fallback target
  404.html
  css/tokens.css          design tokens — the palette, scale and rhythm
  css/style.css           the site
  js/main.js              header, drawer, filter, lightbox, form, reveals
  assets/fonts/           self-hosted Cormorant 400 + Raleway 400–500 (woff2)
  assets/brand/           wordmark and favicon, as vector paths
  assets/img/             photography, WebP + JPEG at each width
  sitemap.xml, robots.txt

netlify/functions/        production form handler
netlify.toml              publish dir, /api/enquiry redirect, CSP, caching
server.py                 local dev server with the same form contract
build/                    authoring tooling — NOT required to run the site
design-identity/          the source design system (read-only reference)
```

### About `build/`

These scripts generated the assets and the repetitive pages. They are kept so
the work is reproducible, not because the site needs them. The shipped HTML is
self-contained and hand-editable.

| Script | What it does |
|---|---|
| `make_logo.py` / `make_brand.py` | Redraw the wordmark as outlined SVG paths; emit the favicon |
| `inject_wordmark.py` | Paste the wordmark `<symbol>` into each page (idempotent) |
| `make_images.py` | Grade, crop and export every responsive image |
| `make_service_pages.py` | Write the three service pages from one template |
| `make_small_pages.py` | Write `thank-you.html` and `404.html` |
| `shot.py` | Screenshot a page via Playwright for visual checks |

If you edit a service page by hand, either stop using
`make_service_pages.py` or port the edit back into it — it overwrites.

---

## The logo

The supplied `logo.jpg` is a 150×150 raster with a baked-in `#3E3C3D`
background — a lighter, magenta-leaning grey that fights the design system's
`#2c2e2c` charcoal. Dropped onto the page it would read as a pale rectangle
floating in the header.

It has been **redrawn as outlined SVG paths** (`assets/brand/wordmark.svg`),
inlined once per page as a `<symbol>` and referenced twice via `<use>`. Because
the type is converted to outlines there is no font dependency and no
`font-weight` reaches the compiled CSS. `fill="currentColor"` means it inherits
`--color-neutral-100` on dark grounds and would inherit `--color-ink` on the
gold panel.

The wordmark is drawn at Raleway 500 to match the nav. It stays monochrome
bone — the champagne gold does its work elsewhere. `#3E3C3D` was **not** added
to the palette; it is an artefact of the client's JPEG export, not a brand
decision.

To change it, edit `build/make_logo.py`, then run `make_brand.py` and
`inject_wordmark.py`.

---

## Forms

The enquiry form posts to `/api/enquiry` in every environment.

| Environment | Handler |
|---|---|
| Local | `server.py` → validates, appends to `enquiries.log` |
| Netlify | `netlify/functions/enquiry.js` via the redirect in `netlify.toml` |

Validation runs in three places with the same rules: `js/main.js` (client),
`server.py` (local) and `enquiry.js` (production). A filled honeypot field
(`company-website`) is accepted and silently discarded so bots learn nothing.

**Before launch:** set `ENQUIRY_FORWARD_URL` in the Netlify environment to an
email service endpoint (Formspree, Resend, Postmark). Without it the function
validates and returns 200 but **delivers nothing**.

To use Formspree directly instead, add `data-endpoint="https://formspree.io/f/XXXX"`
to the `<form>` in `index.html` and skip the function entirely.

Without JavaScript the form falls back to a native POST to `thank-you.html`;
Netlify Forms attributes (`data-netlify`, `netlify-honeypot`) are present so
that path is captured too.

---

## Honesty constraints

The copy was written under a hard rule: **invent nothing**. There is no phone
number, no testimonial, no review score, no founding year, no accreditation, no
employee count and no award anywhere on the site, because none of those are
known. The only quantity used is the 97 posts on Instagram, described as posts.

The absence of a phone number is treated as a positioning choice rather than a
gap — the contact section says enquiries come by email or Instagram so the
dimensions and photographs can be read properly before replying.

If the client supplies real testimonials or credentials later, the contact and
portfolio sections have room for them. Do not fill those slots with anything
unverified.

**All photography is placeholder.** See [IMAGERY.md](IMAGERY.md) — this is the
one thing that must be resolved before launch.

---

## Design system rules

Five things carry the identity. Breaking any one makes it read as a cheaper
brand:

1. **180px section padding**, top and bottom. Not 64px, not 96px. Steps down to
   120px at 1100px and 80px at 767px — never flattened.
2. **Only two font weights, 400 and 500.** Cormorant loads at 400 only; Raleway
   at 400–500 as a variable range, so a heavier request clamps instead of
   synthesising. `font-synthesis: none` on `body` makes faux-bold impossible.
3. **Zero border-radius** except pill buttons (71px).
4. **No shadows.** Depth is colour contrast and full-bleed photography.
5. **One 300ms transition**, and filled buttons **invert** on hover — the fill
   drops to transparent and the text goes gold. They never darken.

Gold (`--color-primary`) appears only on CTAs, hover and focus states, and the
closing panel. Hairlines are always a 30% alpha of an existing colour.
`--color-neutral-700` is decorative display only — it fails WCAG AA at body
size and is used for the process step numerals and nothing else.

Never hardcode a hex that exists as a token.

---

## Accessibility

- Semantic landmarks, one `h1` per page, ordered headings
- Skip link, visible gold focus rings on every interactive element
- Keyboard-navigable lightbox: arrows page, `Esc` closes, focus is trapped and
  restored to the tile that opened it
- Drawer traps focus and closes on `Esc`
- Every portfolio image has alt text describing the work, not the filename
- Form labels are associated, errors are announced via `aria-describedby` and
  `aria-invalid`, filter changes announce a count through a live region
- `prefers-reduced-motion` collapses every transition and disables reveals
- Content is never hidden behind JavaScript — reveals are scoped to `.js` with
  a `<noscript>` override

## Performance

- Self-hosted woff2, subset to latin + latin-ext, `font-display: swap`, preloaded
- WebP with JPEG fallback, `srcset`/`sizes` on everything, lazy below the fold
- `width`/`height` on every image so nothing shifts
- One stylesheet pair, one deferred script, no third-party requests at runtime

## SEO

Targets *bespoke joinery Leeds*, *custom wardrobes West Yorkshire*, *fitted
furniture Leeds* and *local joiner West Yorkshire* — written into real
sentences, never a keyword block. Unique title and meta per page,
`LocalBusiness` schema with the Leeds service area and email (no `telephone`
property, correctly), `Service` and `BreadcrumbList` schema on service pages,
OpenGraph tags with a portfolio image, sitemap and robots.

Update the domain in the canonical tags, OG URLs, JSON-LD, `sitemap.xml` and
`robots.txt` if it differs from `www.northernedgejoineryltd.com`.

---

## Deploying

**Netlify** — connect the repo. `netlify.toml` sets `site/` as the publish
directory, wires `/api/enquiry` to the function, and sets a CSP with no
`unsafe-inline` plus immutable caching on fonts and images. Set
`ENQUIRY_FORWARD_URL`.

**Anywhere else** — upload `site/`. Point `404.html` at the host's not-found
handler and provide an `/api/enquiry` endpoint, or switch the form to Formspree
as above.
