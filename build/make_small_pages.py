"""Write thank-you.html and 404.html — same chrome, minimal bodies."""
import os

OUT = "../site"
SITE = "https://www.northernedgejoineryltd.com"

SHELL = """<!DOCTYPE html>
<html lang="en-GB" class="js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<meta name="robots" content="noindex, follow">

<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#2c2e2c">

<link rel="preload" href="assets/fonts/raleway-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/cormorant-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/tokens.css">
<link rel="stylesheet" href="css/style.css">
<noscript><style>.reveal{opacity:1!important;transform:none!important}</style></noscript>
</head>
<body>
<!--WORDMARK-SYMBOL-->

<a class="skip-link" href="#main">Skip to content</a>

<header class="header is-scrolled" id="site-header">
  <div class="container header__inner">
    <nav class="header__nav" aria-label="Primary">
      <ul class="header__links">
        <li><a href="index.html#work">Work</a></li>
        <li><a href="index.html#services">Services</a></li>
        <li><a href="index.html#process">Process</a></li>
        <li><a href="index.html#contact">Contact</a></li>
      </ul>
    </nav>

    <a class="header__brand" href="index.html" aria-label="Northern Edge Joinery Ltd — home">
      <svg viewBox="0 0 911.5 136.52" role="img" aria-hidden="true"><use href="#ne-wordmark"></use></svg>
    </a>

    <div class="header__cta">
      <a class="btn btn--filled" href="index.html#contact">Request a Bespoke Consultation</a>
    </div>

    <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">
      <span></span><span></span>
    </button>
  </div>
</header>

<div class="drawer" id="drawer" hidden>
  <nav aria-label="Mobile">
    <ul class="drawer__links">
      <li><a href="index.html#work">Work</a></li>
      <li><a href="index.html#services">Services</a></li>
      <li><a href="index.html#process">Process</a></li>
      <li><a href="index.html#contact">Contact</a></li>
    </ul>
  </nav>
  <div class="drawer__foot">
    <p><a href="mailto:info@northernedgejoineryltd.com">info@northernedgejoineryltd.com</a></p>
    <p><a href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">Instagram — @northern_edge_joinery_ltd</a></p>
  </div>
</div>

<main id="main">
  <section class="section section--below-header">
    <div class="container">
      <span class="section-label">{eyebrow}</span>
      <h1 class="page-title">{h1}</h1>
      <p class="lead mt-8">{lead}</p>
      <p class="actions mt-12">
{actions}
      </p>
    </div>
  </section>
</main>

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
          <li><a href="services/bespoke-joinery-leeds.html">Bespoke joinery</a></li>
          <li><a href="services/fitted-wardrobes-west-yorkshire.html">Fitted wardrobes</a></li>
          <li><a href="services/fitted-furniture-leeds.html">Fitted furniture</a></li>
        </ul>
      </div>

      <div>
        <h2>Site</h2>
        <ul class="footer__list">
          <li><a href="index.html#work">Work</a></li>
          <li><a href="index.html#process">Process</a></li>
          <li><a href="index.html#contact">Contact</a></li>
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

<script src="js/main.js" defer></script>
</body>
</html>
"""

PAGES = [
    {
        "file": "thank-you.html",
        "title": "Thank you — Northern Edge Joinery Ltd",
        "meta": "Your enquiry has reached Northern Edge Joinery Ltd in Leeds. We will reply by email to the address you gave us.",
        "eyebrow": "Enquiry received",
        "h1": "Thank you — your enquiry is with us.",
        "lead": "We will reply to the email address you gave us. If you want to add photographs of the room in the meantime, send them straight to info@northernedgejoineryltd.com — the more we can see, the more useful the first reply will be.",
        "actions": [
            ('<a class="btn btn--filled" href="index.html">Back to the site</a>'),
            ('<a class="btn" href="https://instagram.com/northern_edge_joinery_ltd" rel="noopener">See the last 97 projects</a>'),
        ],
    },
    {
        "file": "404.html",
        "title": "Page not found — Northern Edge Joinery Ltd",
        "meta": "That page does not exist on the Northern Edge Joinery website.",
        "eyebrow": "404",
        "h1": "That page is not here.",
        "lead": "The link may be out of date, or the page may have moved. The work, the services and the contact form are all one click away.",
        "actions": [
            ('<a class="btn btn--filled" href="index.html">Back to the site</a>'),
            ('<a class="btn" href="index.html#work">See the work</a>'),
            ('<a class="btn" href="index.html#contact">Contact</a>'),
        ],
    },
]

if __name__ == "__main__":
    for p in PAGES:
        html = SHELL.format(
            title=p["title"], meta=p["meta"], eyebrow=p["eyebrow"],
            h1=p["h1"], lead=p["lead"],
            actions="\n".join("        " + a for a in p["actions"]),
        )
        path = os.path.join(OUT, p["file"])
        open(path, "w", encoding="utf8").write(html)
        print(f"wrote {path} ({len(html)} bytes)")
