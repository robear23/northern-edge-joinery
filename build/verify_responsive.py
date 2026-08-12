"""Responsive, drawer and reduced-motion verification."""
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

BASE = "http://localhost:4321"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


VIEWPORTS = [(390, "mobile"), (768, "tablet"), (1024, "tablet-lg"),
             (1280, "laptop"), (1440, "desktop"), (1920, "wide")]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()

        for w, label in VIEWPORTS:
            pg = await b.new_page(viewport={"width": w, "height": 900})
            await pg.goto(BASE, wait_until="networkidle")
            m = await pg.evaluate("""() => {
                const cs = n => getComputedStyle(n);
                const doc = document.documentElement;
                return {
                  hScroll: doc.scrollWidth - doc.clientWidth,
                  sectionY: cs(document.querySelector('#about')).paddingTop,
                  heroH1: cs(document.querySelector('.hero h1')).fontSize,
                  workCols: cs(document.querySelector('.grid-work')).gridTemplateColumns.split(' ').length,
                  navVisible: document.querySelector('.header__nav').offsetParent !== null,
                  burgerVisible: document.querySelector('.burger').offsetParent !== null,
                  widest: Math.max(...[...document.querySelectorAll('main p')]
                      .map(e => e.getBoundingClientRect().width)),
                  container: document.querySelector('.container').getBoundingClientRect().width,
                };
            }""")
            ok = m["hScroll"] <= 0
            check(f"{label} ({w}px) — no horizontal overflow", ok, f'{m["hScroll"]}px')
            check(f"{label} ({w}px) — section rhythm / hero / grid",
                  int(m["sectionY"].rstrip("px")) >= 80 and m["widest"] <= 545,
                  f'{m["sectionY"]} rhythm, h1 {m["heroH1"]}, {m["workCols"]}-col grid, '
                  f'container {round(m["container"])}px, widest p {round(m["widest"])}px')
            # nav and burger are mutually exclusive
            check(f"{label} ({w}px) — one navigation is shown",
                  m["navVisible"] != m["burgerVisible"],
                  "burger" if m["burgerVisible"] else "inline nav")
            await pg.close()

        # ── mobile drawer ────────────────────────────────────────────────
        pg = await b.new_page(viewport={"width": 390, "height": 844})
        await pg.goto(BASE, wait_until="networkidle")
        await pg.click(".burger")
        await pg.wait_for_timeout(450)
        d = await pg.evaluate("""() => ({
            open: document.getElementById('drawer').classList.contains('is-open'),
            expanded: document.querySelector('.burger').getAttribute('aria-expanded'),
            label: document.querySelector('.burger').getAttribute('aria-label'),
            locked: document.body.classList.contains('is-locked'),
            focusInside: document.getElementById('drawer').contains(document.activeElement)
        })""")
        check("Drawer opens, locks scroll and moves focus inside",
              d["open"] and d["expanded"] == "true" and d["locked"] and d["focusInside"],
              f'aria-label "{d["label"]}"')

        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(450)
        c = await pg.evaluate("""() => ({
            open: document.getElementById('drawer').classList.contains('is-open'),
            locked: document.body.classList.contains('is-locked'),
            onBurger: document.activeElement.classList.contains('burger')
        })""")
        check("Escape closes the drawer and returns focus to the burger",
              not c["open"] and not c["locked"] and c["onBurger"])
        await pg.close()

        # ── reduced motion ───────────────────────────────────────────────
        ctx = await b.new_context(viewport={"width": 1440, "height": 900},
                                  reduced_motion="reduce")
        pg = await ctx.new_page()
        await pg.goto(BASE, wait_until="networkidle")
        rm = await pg.evaluate("""() => {
            const hidden = [...document.querySelectorAll('.reveal')]
                .filter(e => getComputedStyle(e).opacity !== '1').length;
            const d = getComputedStyle(document.querySelector('.btn')).transitionDuration;
            return { hidden, duration: d,
                     scroll: getComputedStyle(document.documentElement).scrollBehavior };
        }""")
        check("Reduced motion: everything visible, transitions collapsed",
              rm["hidden"] == 0 and float(rm["duration"].rstrip("s")) < 0.001,
              f'{rm["hidden"]} hidden, {rm["duration"]}, scroll {rm["scroll"]}')
        await ctx.close()

        # ── no-JS ────────────────────────────────────────────────────────
        ctx = await b.new_context(viewport={"width": 1440, "height": 900},
                                  java_script_enabled=False)
        pg = await ctx.new_page()
        await pg.goto(BASE, wait_until="load")
        content = await pg.locator(".intro__statement").is_visible()
        works = await pg.locator(".work").count()
        check("Without JavaScript the content is still visible", content and works == 12,
              f"{works} portfolio tiles rendered")
        await ctx.close()

        await b.close()

    print(f"\n{sum(results)}/{len(results)} passed")
    sys.exit(0 if all(results) else 1)

asyncio.run(main())
