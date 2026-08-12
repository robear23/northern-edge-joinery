import asyncio, os
from playwright.async_api import async_playwright

SIZES = [
    (32, '../site/favicon-32.png'),
    (180, '../site/apple-touch-icon.png'),
    (512, '../site/assets/brand/icon-512.png'),
]


async def main():
    svg = open('../site/assets/brand/favicon.svg', encoding='utf8').read()
    html = ("<!doctype html><style>html,body{margin:0;padding:0}"
            "svg{display:block;width:100vw;height:100vh}</style>" + svg)
    open('fav.html', 'w', encoding='utf8').write(html)
    url = 'file:///' + os.path.abspath('fav.html').replace(os.sep, '/')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for s, out in SIZES:
            pg = await b.new_page(viewport={'width': s, 'height': s}, device_scale_factor=1)
            await pg.goto(url)
            await pg.screenshot(path=out)
            await pg.close()
            print('wrote', out, s)
        await b.close()

asyncio.run(main())
