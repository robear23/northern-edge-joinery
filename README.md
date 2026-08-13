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
known.

**No project count appears anywhere either.** The site points at Instagram as
the portfolio without putting a number on it — "See the full portfolio", not a
tally. A count printed into static HTML is wrong the day after the next post,
and stale numbers read worse than no number at all. If the client wants one
later it belongs in the Instagram bio, not here.

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

## Motion

Four effects, all scoped to `.js` and all undone by `prefers-reduced-motion`.

| Effect | Driven by | What it does |
|---|---|---|
| `.reveal` | Scroll | Fade and 40px rise on first intersection, once |
| `.hero h1` | **Load** | Resolves a word at a time out of 30% bone into heading colour, 850ms end to end |
| `.intro__statement` | Scroll | Resolves a word at a time out of `--color-neutral-700` into heading colour |
| `.step` | Scroll | Each step's top hairline draws in as solid stone; the numeral lifts out of the recess at the halfway point |

The two scroll-linked reveals share one scroll listener and one
`requestAnimationFrame`, in `main.js` under *Scroll progress*.
`trackProgress(el, from, to, fn)` maps an element's travel through the viewport
onto 0…1 and calls `fn` with it; adding another scroll-linked effect costs a
subscriber, not a listener.

**The hero is the one thing on the site that moves without being asked.** The
hero fills the viewport at scroll 0, so there is no travel to hang a
scroll-linked reveal on — it is a timer or it is nothing. If the "nothing moves
on its own" principle matters more than the effect, delete the *Hero headline*
block in `main.js` and the `hero-word-resolve` keyframes; nothing else depends
on either.

Its timing lives in the stylesheet, not in JS: the script carries a
`--word-index` per word and CSS turns that into an `animation-delay`. There are
no timers to leak or fall out of step. The keyframes declare only `from`, so
the animation resolves to whatever colour the headline already computes to and
the end state cannot drift from the base rule.

Four rules govern all of this, and breaking any one is a regression:

1. **A recessed colour is never the resting state of real copy.**
   `--color-neutral-700` is ~2:1 on the ground and fails AA at every size. Both
   word reveals are enhancements on top of legible text: without the script, or
   under reduced motion, every word renders at full heading colour. The recess
   lives on the word spans, which exist only if the split ran — a script that
   throws leaves a heading at full colour rather than stranding it mid-reveal.
2. **The word reveal is monotonic.** A word that has resolved never recedes,
   including on the way back up. Scrubbing it in both directions — which is
   what the reference implementation does — lets a reader park the viewport
   and sit reading half-lit text.
3. **No gold.** The step rule is the solid `--color-accent` that the
   `--color-alpha-stone-30` hairline is a 30% alpha of. Gold stays on CTAs,
   hover and focus, and the closing panel.

4. **The hero recesses to 30% bone, not to `--color-neutral-700`.** It sits on
   a photograph. The flat recess grey that reads as "held back" on the solid
   ground reads as muddy over an image; 30% of the final colour fades up
   cleanly against anything underneath it.

The scroll ranges are tuned so an effect **finishes while its element is still
on screen**. `.intro__statement` completes when its bottom edge is 75% down
the viewport; ending it later lights the closing words as they leave the top,
which is precisely when nobody is reading them.

One timing constraint on the hero: `main.js` is deferred, so the split must
land before first contentful paint or the headline paints at full colour, snaps
to the recess and resolves — a flash on every load. Measured on localhost the
split lands at ~83ms against an FCP of ~140ms. If the script ever grows enough
to push past that, the hero reveal is the first thing that will show it.

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
