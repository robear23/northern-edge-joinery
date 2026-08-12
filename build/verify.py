"""Functional verification of the built site against the acceptance checklist."""
import asyncio, sys, json

sys.stdout.reconfigure(encoding="utf-8")
from playwright.async_api import async_playwright

BASE = "http://localhost:4321"
results = []


def check(name, ok, detail=""):
    results.append((ok, name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))

        await pg.goto(BASE, wait_until="networkidle")

        # ── computed design-system values ────────────────────────────────
        m = await pg.evaluate("""() => {
            const cs = n => getComputedStyle(n);
            const sec = document.querySelector('#about');
            const btn = document.querySelector('.hero .btn--filled');
            const eyebrow = document.querySelector('.section-label');
            const lead = document.querySelector('.hero .lead');
            const h1 = document.querySelector('.hero h1');
            const grid = document.querySelector('.grid-work');
            const proc = document.querySelector('.process__grid');
            const panel = document.querySelector('.cta-panel');
            const bad = [];
            document.querySelectorAll('*').forEach(el => {
                const s = cs(el);
                if (parseInt(s.fontWeight, 10) > 500) bad.push(el.tagName + '.' + el.className);
                if (s.boxShadow && s.boxShadow !== 'none') bad.push('shadow:' + el.tagName);
                const r = s.borderRadius;
                if (r && r !== '0px' && !r.startsWith('71px') && !r.startsWith('50%')) {
                    bad.push('radius:' + el.tagName + '.' + el.className + '=' + r);
                }
            });
            return {
              sectionPadTop: cs(sec).paddingTop,
              sectionPadBottom: cs(sec).paddingBottom,
              heroH1: cs(h1).fontSize,
              heroH1Family: cs(h1).fontFamily,
              heroH1LineHeight: cs(h1).lineHeight,
              heroH1Tracking: cs(h1).letterSpacing,
              leadSize: cs(lead).fontSize,
              leadWidth: lead.getBoundingClientRect().width,
              btnRadius: cs(btn).borderRadius,
              btnBg: cs(btn).backgroundColor,
              btnColor: cs(btn).color,
              btnTransition: cs(btn).transitionDuration,
              eyebrowSize: cs(eyebrow).fontSize,
              eyebrowBorder: cs(eyebrow).borderBottomColor,
              gridGap: cs(grid).gap,
              procGap: cs(proc).columnGap,
              panelBg: cs(panel).backgroundColor,
              panelPad: cs(panel).paddingTop,
              badCount: bad.length, bad: bad.slice(0, 8),
              maxParaWidth: Math.max(...[...document.querySelectorAll('main p')]
                  .map(el => el.getBoundingClientRect().width)),
            };
        }""")

        check("Section padding is 180px", m["sectionPadTop"] == "180px" and m["sectionPadBottom"] == "180px",
              f'{m["sectionPadTop"]} / {m["sectionPadBottom"]}')
        check("Hero h1 is 88px Cormorant, lh 1.0, -0.02em",
              m["heroH1"] == "88px" and "Cormorant" in m["heroH1Family"]
              and m["heroH1LineHeight"] == "88px" and m["heroH1Tracking"] == "-1.76px",
              f'{m["heroH1"]} / {m["heroH1LineHeight"]} / {m["heroH1Tracking"]}')
        check("Hero lead is 18px within the 540px measure",
              m["leadSize"] == "18px" and m["leadWidth"] <= 540.5,
              f'{m["leadSize"]}, {round(m["leadWidth"])}px')
        check("No paragraph exceeds the 540px measure", m["maxParaWidth"] <= 540.5,
              f'widest {round(m["maxParaWidth"])}px')
        check("Buttons are 71px pills", m["btnRadius"] == "71px", m["btnRadius"])
        check("Filled CTA is gold with ink text",
              m["btnBg"] == "rgb(222, 196, 151)" and m["btnColor"] == "rgb(19, 20, 19)",
              f'{m["btnBg"]} / {m["btnColor"]}')
        check("Transitions are 300ms", m["btnTransition"] == "0.3s", m["btnTransition"])
        check("Eyebrow is 12px on a 30% bone hairline",
              m["eyebrowSize"] == "12px" and "0.3" in m["eyebrowBorder"],
              f'{m["eyebrowSize"]}, {m["eyebrowBorder"]}')
        check("Portfolio gutter is 40px", m["gridGap"] == "40px", m["gridGap"])
        check("Process column gap is 180px", m["procGap"] == "180px", m["procGap"])
        check("Closing panel is gold at 100px padding",
              m["panelBg"] == "rgb(222, 196, 151)" and m["panelPad"] == "100px",
              f'{m["panelBg"]} / {m["panelPad"]}')
        check("No computed weight >500, no shadow, no stray radius",
              m["badCount"] == 0, json.dumps(m["bad"]))

        # ── button inverts rather than darkens ───────────────────────────
        await pg.hover(".hero .btn--filled")
        await pg.wait_for_timeout(450)
        hov = await pg.evaluate("""() => {
            const s = getComputedStyle(document.querySelector('.hero .btn--filled'));
            return { bg: s.backgroundColor, color: s.color };
        }""")
        check("Filled button inverts on hover",
              hov["bg"] == "rgba(0, 0, 0, 0)" and hov["color"] == "rgb(222, 196, 151)",
              f'{hov["bg"]} / {hov["color"]}')

        # ── header collapse ──────────────────────────────────────────────
        rest = await pg.evaluate("getComputedStyle(document.getElementById('site-header')).paddingTop")
        await pg.evaluate("document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,600)")
        await pg.wait_for_timeout(500)
        scrolled = await pg.evaluate("getComputedStyle(document.getElementById('site-header')).paddingTop")
        check("Header padding collapses 56px → 14px", rest == "56px" and scrolled == "14px",
              f"{rest} → {scrolled}")
        await pg.evaluate("window.scrollTo(0,0)")

        # ── portfolio filter ─────────────────────────────────────────────
        await pg.click('.filter[data-filter="wardrobes"]')
        await pg.wait_for_timeout(200)
        vis = await pg.evaluate("""() => ({
            shown: [...document.querySelectorAll('.work')].filter(w => !w.classList.contains('is-hidden')).length,
            allCats: [...document.querySelectorAll('.work:not(.is-hidden)')].map(w => w.dataset.cat),
            status: document.getElementById('filter-status').textContent
        })""")
        check("Filter narrows the grid and announces it",
              vis["shown"] == 4 and set(vis["allCats"]) == {"wardrobes"} and "4" in vis["status"],
              f'{vis["shown"]} shown — "{vis["status"]}"')
        await pg.click('.filter[data-filter="all"]')

        # ── lightbox, by keyboard ────────────────────────────────────────
        await pg.click(".work")
        await pg.wait_for_timeout(400)
        lb = await pg.evaluate("""() => ({
            open: document.getElementById('lightbox').classList.contains('is-open'),
            focus: document.activeElement.textContent.trim(),
            src: document.getElementById('lightbox-img').getAttribute('src'),
            alt: document.getElementById('lightbox-img').alt.length,
            count: document.getElementById('lightbox-count').textContent
        })""")
        check("Lightbox opens with focus moved and alt text carried",
              lb["open"] and lb["focus"] == "Close" and "-lg-" in lb["src"] and lb["alt"] > 20,
              f'{lb["count"]}, alt {lb["alt"]} chars')
        await pg.keyboard.press("ArrowRight")
        await pg.wait_for_timeout(200)
        after = await pg.evaluate("document.getElementById('lightbox-count').textContent")
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(400)
        closed = await pg.evaluate("""() => ({
            open: document.getElementById('lightbox').classList.contains('is-open'),
            restored: document.activeElement.classList.contains('work')
        })""")
        check("Arrow keys page, Escape closes and restores focus",
              after == "2 / 12" and not closed["open"] and closed["restored"],
              f'{after}, focus restored: {closed["restored"]}')

        # ── form: validation then a real submission ──────────────────────
        await pg.click('#enquiry-form [type="submit"]')
        await pg.wait_for_timeout(250)
        inv = await pg.evaluate("""() => ({
            invalid: document.querySelectorAll('.field[data-invalid="true"]').length,
            firstMsg: document.getElementById('name-error').textContent,
            focused: document.activeElement.id,
            aria: document.getElementById('name').getAttribute('aria-invalid')
        })""")
        check("Empty submit blocks and marks every field",
              inv["invalid"] == 4 and inv["focused"] == "name" and inv["aria"] == "true",
              f'{inv["invalid"]} fields — "{inv["firstMsg"]}"')

        await pg.fill("#email", "not-an-email")
        await pg.evaluate("document.getElementById('email').blur()")
        await pg.wait_for_timeout(150)
        bad_email = await pg.evaluate("document.getElementById('email-error').textContent")
        check("Bad email is rejected in the system's own voice",
              "does not look like" in bad_email, bad_email)

        await pg.fill("#name", "Test Enquiry")
        await pg.fill("#email", "test@example.com")
        await pg.select_option("#project", "Custom fitted wardrobes")
        await pg.fill("#message", "Alcove either side of the chimney breast, roughly 900mm wide and 2.6m to the ceiling.")
        await pg.click('#enquiry-form [type="submit"]')
        await pg.wait_for_timeout(1200)
        ok = await pg.evaluate("""() => ({
            ok: document.getElementById('form-ok').classList.contains('is-visible'),
            fail: document.getElementById('form-fail').classList.contains('is-visible'),
            cleared: document.getElementById('name').value === ''
        })""")
        check("Valid submission reaches the endpoint and shows the success state",
              ok["ok"] and not ok["fail"] and ok["cleared"],
              f'ok={ok["ok"]} fail={ok["fail"]} reset={ok["cleared"]}')

        # ── honeypot ─────────────────────────────────────────────────────
        hp = await pg.evaluate("""async () => {
            const r = await fetch('/api/enquiry', {
                method: 'POST',
                headers: {'Content-Type':'application/x-www-form-urlencoded'},
                body: new URLSearchParams({'company-website':'http://spam.example','name':'','email':'','project':'','message':''}).toString()
            });
            return r.status;
        }""")
        check("Honeypot submission is accepted and discarded server-side", hp == 200, f"HTTP {hp}")

        srv = await pg.evaluate("""async () => {
            const r = await fetch('/api/enquiry', {
                method: 'POST',
                headers: {'Content-Type':'application/x-www-form-urlencoded'},
                body: new URLSearchParams({name:'x',email:'nope',project:'Bad',message:'short'}).toString()
            });
            return {status: r.status, body: await r.json()};
        }""")
        check("Server rejects invalid input independently of the client",
              srv["status"] == 422 and len(srv["body"]["errors"]) >= 3,
              f'HTTP {srv["status"]}, {list(srv["body"]["errors"])}')

        # ── keyboard reachability ────────────────────────────────────────
        await pg.goto(BASE, wait_until="networkidle")
        reach = await pg.evaluate("""() => {
            const sel = 'a[href], button:not([disabled]), input, select, textarea';
            const all = [...document.querySelectorAll(sel)]
                .filter(e => !e.closest('.hp'))          // honeypot is -1 by design
                .filter(e => e.offsetParent !== null || e.classList.contains('skip-link'));
            const unreachable = all.filter(e => e.tabIndex < 0);
            return { total: all.length, unreachable: unreachable.length };
        }""")
        check("Every visible control is keyboard reachable",
              reach["unreachable"] == 0, f'{reach["total"]} controls')

        errors.clear()
        await pg.reload(wait_until="networkidle")
        check("No console errors on load", len(errors) == 0, "; ".join(errors[:3]))

        # ── the other pages ──────────────────────────────────────────────
        for path in ["/services/bespoke-joinery-leeds.html",
                     "/services/fitted-wardrobes-west-yorkshire.html",
                     "/services/fitted-furniture-leeds.html",
                     "/thank-you.html", "/404.html"]:
            errors.clear()
            r = await pg.goto(BASE + path, wait_until="networkidle")
            info = await pg.evaluate("""() => ({
                h1: document.querySelectorAll('h1').length,
                title: document.title,
                desc: (document.querySelector('meta[name=description]')||{}).content || '',
                logo: !!document.querySelector('#ne-wordmark'),
                broken: [...document.images].filter(i => i.getAttribute('src') && (!i.complete || i.naturalWidth === 0)).length
            })""")
            check(f"{path}", r.status == 200 and info["h1"] == 1 and len(info["title"]) > 20
                  and len(info["desc"]) > 60 and info["logo"] and info["broken"] == 0
                  and not errors,
                  f'one h1, title {len(info["title"])}ch, meta {len(info["desc"])}ch, {info["broken"]} broken imgs')

        await b.close()

    bad = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(bad)}/{len(results)} passed")
    sys.exit(1 if bad else 0)

asyncio.run(main())
