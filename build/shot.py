"""Screenshot a page. Scrolls the whole document first so IntersectionObserver
reveals have fired before capture.

    python shot.py <url> <out.png> [width] [full|viewport]
"""
import sys, asyncio
from playwright.async_api import async_playwright


async def main():
    url, out = sys.argv[1], sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    full = len(sys.argv) > 4 and sys.argv[4] == "full"

    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": width, "height": 900}, device_scale_factor=1)
        await pg.goto(url, wait_until="networkidle")
        # scroll-behavior:smooth would animate every hop and never arrive,
        # so step through with instant scrolls to fire the reveal observer
        await pg.evaluate("""async () => {
            const html = document.documentElement;
            const prev = html.style.scrollBehavior;
            html.style.scrollBehavior = 'auto';
            const step = window.innerHeight * 0.8;
            for (let y = 0; y < html.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 80));
            }
            window.scrollTo(0, 0);
            html.style.scrollBehavior = prev;
            await new Promise(r => setTimeout(r, 400));
        }""")
        await pg.wait_for_timeout(500)
        await pg.screenshot(path=out, full_page=full)
        await b.close()
    print("saved", out)

asyncio.run(main())
