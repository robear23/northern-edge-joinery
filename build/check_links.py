"""Resolve every internal href, src and srcset entry against the dev server."""
import glob, os, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = "http://localhost:4321"
SITE = "../site"

checked, bad = set(), []


def probe(page, raw, target):
    if target in checked:
        return
    checked.add(target)
    try:
        with urllib.request.urlopen(BASE + target, timeout=15) as r:
            if r.status != 200:
                bad.append((page, raw, r.status))
    except Exception as e:
        bad.append((page, raw, str(e)))


for p in glob.glob(f"{SITE}/**/*.html", recursive=True):
    rel = os.path.relpath(p, SITE).replace(os.sep, "/")
    d = os.path.dirname(rel)
    s = open(p, encoding="utf8").read()

    for attr in re.findall(r'(?:href|src)="([^"]+)"', s):
        if attr.startswith(("http", "mailto:", "data:", "#", "//")):
            continue
        u = attr.split("#")[0]
        if not u:
            continue
        target = u if u.startswith("/") else "/" + os.path.normpath(
            os.path.join(d, u)).replace(os.sep, "/")
        probe(rel, attr, target)

    for ss in re.findall(r'srcset="([^"]+)"', s):
        for part in ss.split(","):
            u = part.strip().split(" ")[0]
            if not u or u.startswith(("http", "data:")):
                continue
            target = "/" + os.path.normpath(os.path.join(d, u)).replace(os.sep, "/")
            probe(rel, u, target)

print(f"checked {len(checked)} unique internal URLs across "
      f"{len(glob.glob(f'{SITE}/**/*.html', recursive=True))} pages")
for b in bad:
    print("BROKEN:", b)
print("all resolve" if not bad else f"{len(bad)} broken")
sys.exit(1 if bad else 0)
