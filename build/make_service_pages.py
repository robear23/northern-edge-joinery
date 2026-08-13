"""Write the three service pages from one template.

Authoring convenience: the output is plain, self-contained static HTML with no
build step in the deliverable. Re-run after editing the template or the copy
below, then run inject_wordmark.py.
"""
import os
import html as htmllib

OUT = "../site/services"
SITE = "https://www.northernedgejoineryltd.com"

NAV = """    <nav class="header__nav" aria-label="Primary">
      <ul class="header__links">
        <li><a href="../index.html#work">Work</a></li>
        <li><a href="../index.html#services">Services</a></li>
        <li><a href="../index.html#process">Process</a></li>
        <li><a href="../index.html#contact">Contact</a></li>
      </ul>
    </nav>"""

DRAWER = """  <nav aria-label="Mobile">
    <ul class="drawer__links">
      <li><a href="../index.html#work">Work</a></li>
      <li><a href="../index.html#services">Services</a></li>
      <li><a href="../index.html#process">Process</a></li>
      <li><a href="../index.html#contact">Contact</a></li>
    </ul>
  </nav>"""


def work_card(n, cat, cat_label, caption, alt):
    """One portfolio tile, paths relative to /services/."""
    sizes = "(max-width: 767px) calc(100vw - 30px), (max-width: 1100px) 45vw, 24vw"
    return f"""        <button class="work" type="button" data-cat="{cat}" data-full="../assets/img/work-{n}-lg-1400.jpg" data-caption="{caption}" data-cat-label="{cat_label}">
          <picture>
            <source type="image/webp" sizes="{sizes}" srcset="../assets/img/work-{n}-400.webp 400w, ../assets/img/work-{n}-760.webp 760w, ../assets/img/work-{n}-1100.webp 1100w">
            <img src="../assets/img/work-{n}-760.jpg" sizes="{sizes}" srcset="../assets/img/work-{n}-400.jpg 400w, ../assets/img/work-{n}-760.jpg 760w, ../assets/img/work-{n}-1100.jpg 1100w" width="1100" height="1375" loading="lazy" decoding="async" alt="{alt}">
          </picture>
          <span class="work__caption"><span>{caption}</span><span class="work__cat">{cat_label}</span></span>
        </button>"""


PAGES = [
    {
        "slug": "bespoke-joinery-leeds",
        "title": "Bespoke Joinery Leeds | Custom Woodworking — Northern Edge Joinery Ltd",
        "meta": "Bespoke joinery in Leeds. Custom woodworking, alcove joinery, panelling and staircase work, measured and made to fit period and modern homes across West Yorkshire.",
        "h1": "Bespoke joinery in Leeds",
        "lead": "Custom woodworking tailored to unique architectural spaces and individual client specifications — drawn to the room you actually have, not to a catalogue.",
        "service_name": "Bespoke Joinery",
        "image": "service-joinery",
        "image_alt": "Built-in shelving and a reading chair set against a panelled timber wall in a period room.",
        "eyebrow": "What it is",
        "heading": "A survey first, a product range never.",
        "body": [
            "Most of the houses we work in were not built square. Terraces and semis across Leeds have settled for a century, and a wall that looks straight is rarely within ten millimetres of it over three metres. Off-the-shelf furniture assumes otherwise, which is why there is always a gap somewhere and a strip of scribe moulding covering it.",
            "Bespoke joinery starts from a measured survey. We record the room at several heights, note where it runs out of plumb and out of level, and draw the piece to those numbers. Scribes, packers and shadow gaps are decided at the drawing stage rather than improvised on the day.",
            "The result reads as part of the building rather than as something delivered to it. Panelling that lines through with the rail already on the wall. An alcove unit that finishes tight against a bowed chimney breast. New doors hung to match the ones you are keeping.",
        ],
        "included_label": "What we make",
        "included": [
            "Alcove and chimney-breast joinery",
            "Wall panelling and linings",
            "Doors, frames, architrave and skirting",
            "Staircases, balustrades and handrails",
            "Window seats and bay joinery",
            "Concealed and jib doors",
        ],
        "close_heading": "Materials and finish",
        "close_body": "We work in hardwood, veneered board and paint-grade timber, and we will tell you honestly which one suits the job. A painted MDF panel in the right place outlasts an oak one in the wrong place, and costs less. Finishes are sprayed or hand-applied to a colour you choose, and we leave samples with you before anything is ordered.",
        "cat": "joinery",
        "works": [
            ("01", "Full-height library shelving", "Floor-to-ceiling timber library shelving running the length of a hallway beside an exposed brick wall."),
            ("02", "Arched bookcase", "An arched timber bookcase built into a curved wall, filled with books from floor to ceiling."),
            ("03", "Timber slat screen", "A vertical timber slat screen forming a room divider behind an upholstered reading chair."),
            ("04", "Alcove shelving", "Slim open shelving fitted into a narrow alcove beside a tall panelled door."),
        ],
    },
    {
        "slug": "fitted-wardrobes-west-yorkshire",
        "title": "Custom Fitted Wardrobes West Yorkshire | Built-In Bedroom Storage — Northern Edge Joinery Ltd",
        "meta": "Custom fitted wardrobes across West Yorkshire. Built-in bedroom storage, walk-in wardrobes, sliding wardrobe systems and alcove fitting, made to measure by a Leeds joinery workshop.",
        "h1": "Custom fitted wardrobes across West Yorkshire",
        "lead": "Built-in bedroom storage, walk-in wardrobes, sliding wardrobes and alcove fitting — floor to ceiling, wall to wall, built for the room it stands in.",
        "service_name": "Custom Fitted Wardrobes",
        "image": "service-wardrobes",
        "image_alt": "A walk-in dressing room with full-height open shelving, hanging rails and integrated strip lighting.",
        "eyebrow": "What it is",
        "heading": "The space above a freestanding wardrobe is space you paid for.",
        "body": [
            "A freestanding wardrobe leaves three gaps: the one above it, the one behind it and the one at the side where the room stopped being straight. In a Leeds bedroom with a chimney breast and a sloping ceiling, that is easily a third of the storage you were entitled to.",
            "A fitted wardrobe takes all of it. It runs to the ceiling, follows the eaves, returns into the alcove and finishes flush against the wall. Where the floor falls away, the carcass is packed and the doors are hung to the finished line rather than the floor.",
            "The inside matters as much as the front. We set hanging heights against what you actually own — long coats and dresses need real height, shirts and jackets need half of it — and size drawers, shelves, shoe racks and pull-out rails around that rather than around a standard carcass.",
        ],
        "included_label": "What we make",
        "included": [
            "Floor-to-ceiling built-in wardrobes",
            "Walk-in wardrobes and dressing rooms",
            "Sliding door wardrobe systems",
            "Hinged and push-to-open doors",
            "Alcove, eaves and loft-room fitting",
            "Internal drawers, rails and shoe storage",
        ],
        "close_heading": "Doors and fronts",
        "close_body": "Shaker, flat slab, fluted, mirrored or panelled to match the room — the door style is the part everybody sees, so it is the part we draw first. Sliding systems suit narrow rooms where a hinged door would foul the bed; hinged doors give you the whole opening at once. We will say which we would fit in your room and why.",
        "cat": "wardrobes",
        "works": [
            ("05", "Walk-in dressing room", "A walk-in dressing room lined in pale timber with continuous hanging rails and recessed strip lighting."),
            ("06", "Wardrobe interior", "The open interior of a fitted wardrobe with oak shelving, graphite carcasses and pull-out shoe racks."),
            ("07", "Concealed door run", "A flush concealed door set into a full-height run of timber and painted wall panelling."),
            ("08", "Panelled headboard wall", "A bedroom with a full-width timber panelled headboard wall and integrated bedside shelving."),
        ],
    },
    {
        "slug": "fitted-furniture-leeds",
        "title": "Fitted Furniture Leeds | Media Walls, Shelving &amp; Home Office — Northern Edge Joinery Ltd",
        "meta": "Fitted furniture in Leeds. Made-to-measure shelving, media walls, home office storage and custom cabinetry, built into the room by a local joiner serving West Yorkshire.",
        "h1": "Fitted furniture in Leeds",
        "lead": "Made-to-measure shelving, media walls, home office storage and custom cabinetry — built into the room rather than placed in it.",
        "service_name": "Fitted Furniture",
        "image": "service-furniture",
        "image_alt": "A built-in home office with a full-width oak desk, drawer units and open shelving either side.",
        "eyebrow": "What it is",
        "heading": "Everything that should have been built in from the start.",
        "body": [
            "Fitted furniture is the quiet half of a house working properly: shelving that carries a full run of books without bowing in the middle, a desk that fits the return under the window, a media wall that swallows the cabling instead of trailing it down the plaster.",
            "The engineering is the point. Shelf spans, board thickness and fixing method are chosen for the load, not for the look — a 900mm span in 18mm board will sag under books inside a year, so we do not build it that way. Services, sockets and ventilation are designed in rather than cut in afterwards.",
            "Made to measure also means the piece finishes where the room finishes. No filler panel at the end of the run, no returns that stop 40mm short, no plinth riding over a floor that falls away.",
        ],
        "included_label": "What we make",
        "included": [
            "Media walls and TV units",
            "Home office desks and storage",
            "Bookcases and open shelving",
            "Utility and boot room cabinetry",
            "Under-stairs storage",
            "Bench seating and banquettes",
        ],
        "close_heading": "Working with a local joiner",
        "close_body": "We are a small West Yorkshire workshop, which means the person who measures your room is the person who draws it and the person who fits it. Nothing is passed to a subcontractor and nothing is ordered from a catalogue in another county. If something is not right, there is one number of people to talk to about it.",
        "cat": "furniture",
        "works": [
            ("09", "Library wall", "A floor-to-ceiling library wall behind a tan leather sofa, lit by a single table lamp."),
            ("10", "Hallway cabinetry", "A run of full-height hallway cabinetry in dark timber with a vertical fluted panel detail."),
            ("11", "Utility run", "A fitted utility run in graphite-stained timber with a stone worktop and wall-mounted rail."),
            ("12", "Island and storage", "A solid oak island top beside full-height dark timber storage and open shelving."),
        ],
    },
]


TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{site}/services/{slug}.html">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Northern Edge Joinery Ltd">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="{site}/services/{slug}.html">
<meta property="og:image" content="{site}/assets/img/og-northern-edge-joinery.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="../assets/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="../apple-touch-icon.png">
<meta name="theme-color" content="#2c2e2c">

<link rel="preload" href="../assets/fonts/raleway-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../assets/fonts/cormorant-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../css/tokens.css">
<link rel="stylesheet" href="../css/style.css">
<noscript><style>.reveal{opacity:1!important;transform:none!important}</style></noscript>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Service",
      "name": "{service_name}",
      "serviceType": "{service_name}",
      "description": "{meta}",
      "url": "{site}/services/{slug}.html",
      "provider": {{
        "@type": "LocalBusiness",
        "@id": "{site}/#business",
        "name": "Northern Edge Joinery Ltd",
        "email": "info@northernedgejoineryltd.com",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "Leeds",
          "addressRegion": "West Yorkshire",
          "addressCountry": "GB"
        }},
        "sameAs": ["https://instagram.com/northern_edge_joinery_ltd"]
      }},
      "areaServed": [
        {{ "@type": "City", "name": "Leeds" }},
        {{ "@type": "AdministrativeArea", "name": "West Yorkshire" }}
      ]
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{site}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "{site}/#services" }},
        {{ "@type": "ListItem", "position": 3, "name": "{service_name}", "item": "{site}/services/{slug}.html" }}
      ]
    }}
  ]
}}
</script>
</head>
<body>
<!--WORDMARK-SYMBOL-->

<a class="skip-link" href="#main">Skip to content</a>

<header class="header" id="site-header">
  <div class="container header__inner">
{nav}

    <a class="header__brand" href="../index.html" aria-label="Northern Edge Joinery Ltd — home">
      <svg viewBox="0 0 911.5 136.52" role="img" aria-hidden="true"><use href="#ne-wordmark"></use></svg>
    </a>

    <div class="header__cta">
      <a class="btn btn--filled" href="../index.html#contact">Request a Bespoke Consultation</a>
    </div>

    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer" hidden>
{drawer}
  <div class="drawer__foot">
    <p><a href="mailto:info@northernedgejoineryltd.com">info@northernedgejoineryltd.com</a></p>
    <p><a href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">Instagram — @northern_edge_joinery_ltd</a></p>
  </div>
</div>

<main id="main">

  <section class="page-head">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="../index.html">Home</a><span aria-hidden="true">/</span>
        <a href="../index.html#services">Services</a><span aria-hidden="true">/</span>
        <span aria-current="page">{service_name}</span>
      </nav>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
  </section>

  <section class="section">
    <div class="container service">
      <div class="service__media">
        <picture>
          <source type="image/webp" sizes="(max-width: 1100px) calc(100vw - 60px), 42vw"
            srcset="../assets/img/{image}-560.webp 560w, ../assets/img/{image}-860.webp 860w, ../assets/img/{image}-1200.webp 1200w">
          <img src="../assets/img/{image}-860.jpg" sizes="(max-width: 1100px) calc(100vw - 60px), 42vw"
            srcset="../assets/img/{image}-560.jpg 560w, ../assets/img/{image}-860.jpg 860w, ../assets/img/{image}-1200.jpg 1200w"
            width="1200" height="900" loading="lazy" decoding="async" alt="{image_alt}">
        </picture>
      </div>
      <div class="service__body reveal">
        <span class="section-label">{eyebrow}</span>
        <h2>{heading}</h2>
{body}
      </div>
    </div>
  </section>

  <section class="section section--sunken">
    <div class="container process__grid">
      <div class="reveal">
        <span class="section-label">{included_label}</span>
        <ul class="service__list measure-none">
{included}
        </ul>
      </div>
      <div class="reveal">
        <h2>{close_heading}</h2>
        <p class="mt-6">{close_body}</p>
        <p class="mt-10">
          <a class="btn btn--filled" href="../index.html#contact">Request a Bespoke Consultation</a>
        </p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="portfolio__head reveal">
        <div>
          <span class="section-label">Related work</span>
          <h2>{service_name}, as installed.</h2>
        </div>
        <a class="btn" href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">See the full portfolio</a>
      </div>

      <!-- PLACEHOLDER IMAGERY — licensed stock interiors graded to the brand,
           standing in for Northern Edge Joinery's own project photographs.
           Captions describe the piece shown and claim no specific project.
           See IMAGERY.md before launch. -->
      <div class="grid-work grid-work--4" id="work-grid">
{works}
      </div>
    </div>
  </section>

  <section class="cta-panel">
    <div class="container">
      <h2>Tell us about the room.</h2>
      <p>Send the dimensions, a photograph, or just a rough idea of what you want it to do. We will come back to you with an honest view of what is possible and what it costs.</p>
      <div class="cta-panel__actions">
        <a class="btn btn--ink btn--lg" href="../index.html#contact">Request a Bespoke Consultation</a>
        <a class="btn btn--lg" href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">See the portfolio</a>
      </div>
    </div>
  </section>
</main>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Portfolio image" hidden>
  <button class="btn lightbox__close" type="button" data-lb="close">Close</button>
  <figure class="lightbox__figure">
    <img id="lightbox-img" width="1400" height="1867" alt="">
    <figcaption>
      <span id="lightbox-caption"></span>
      <span id="lightbox-cat" class="work__cat"></span>
    </figcaption>
  </figure>
  <div class="lightbox__controls">
    <button class="btn" type="button" data-lb="prev">Previous</button>
    <span class="lightbox__count" id="lightbox-count"></span>
    <button class="btn" type="button" data-lb="next">Next</button>
  </div>
</div>

<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <svg viewBox="0 0 911.5 136.52" role="img" aria-label="Northern Edge Joinery Ltd"><use href="#ne-wordmark"></use></svg>
        <p>Bespoke joinery, custom fitted wardrobes and made-to-measure fitted furniture, built in Leeds for homes across West Yorkshire.</p>
      </div>

      <div>
        <h2>Services</h2>
        <ul class="footer__list">
          <li><a href="bespoke-joinery-leeds.html">Bespoke joinery</a></li>
          <li><a href="fitted-wardrobes-west-yorkshire.html">Fitted wardrobes</a></li>
          <li><a href="fitted-furniture-leeds.html">Fitted furniture</a></li>
        </ul>
      </div>

      <div>
        <h2>Site</h2>
        <ul class="footer__list">
          <li><a href="../index.html#work">Work</a></li>
          <li><a href="../index.html#process">Process</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </div>

      <div>
        <h2>Contact</h2>
        <ul class="footer__list">
          <li><a href="mailto:info@northernedgejoineryltd.com">info@northernedgejoineryltd.com</a></li>
          <li><a href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">@northern_edge_joinery_ltd</a></li>
          <li>Leeds, West Yorkshire</li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom">
      <span>&copy; 2026 Northern Edge Joinery Ltd</span>
      <span>Leeds &middot; West Yorkshire &middot; United Kingdom</span>
    </div>
  </div>
</footer>

<script src="../js/main.js" defer></script>
</body>
</html>
"""

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for p in PAGES:
        body = "\n".join(
            f'        <p{"" if i == 0 else " style=\"margin-top:var(--space-6)\""}>{t}</p>'
            for i, t in enumerate(p["body"])
        )
        included = "\n".join(f"          <li>{i}</li>" for i in p["included"])
        works = "\n".join(
            work_card(n, p["cat"], p["service_name"], cap, alt)
            for n, cap, alt in p["works"]
        )
        html = TEMPLATE.format(
            site=SITE, nav=NAV, drawer=DRAWER,
            body=body, included=included, works=works,
            **{k: v for k, v in p.items()
               if k not in ("body", "included", "works", "cat")},
        )
        path = f"{OUT}/{p['slug']}.html"
        open(path, "w", encoding="utf8").write(html)
        print(f"wrote {path} ({len(html)} bytes)")
