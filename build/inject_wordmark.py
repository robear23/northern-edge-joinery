"""Paste the outlined wordmark <symbol> into every page that asks for it.

Authoring convenience only. The shipped HTML is plain, self-contained and
hand-editable — there is no build step in the deliverable. Re-run this after
regenerating the wordmark with make_brand.py.

  <!--WORDMARK-SYMBOL-->   is replaced with the symbol block
  <!--/WORDMARK-SYMBOL-->  marks the end of a previous injection
"""
import glob
import os
import re

SITE = "../site"
MARK = "<!--WORDMARK-SYMBOL-->"
END = "<!--/WORDMARK-SYMBOL-->"

symbol = open("wordmark-symbol.html", encoding="utf8").read().strip()
block = f"{MARK}{symbol}{END}"

pages = glob.glob(f"{SITE}/**/*.html", recursive=True)
touched = 0

for path in pages:
    html = open(path, encoding="utf8").read()
    if MARK not in html:
        continue
    # Decide on the presence of the end marker, not on whether the regex
    # changed anything — an unchanged symbol would otherwise fall through to
    # the bare-marker branch and nest a second copy on every run.
    if END in html:
        # greedy to the LAST end marker, so any earlier nesting collapses
        new = re.sub(
            re.escape(MARK) + ".*" + re.escape(END), block, html, flags=re.S
        )
    else:
        new = html.replace(MARK, block)
    if new != html:
        open(path, "w", encoding="utf8").write(new)
        touched += 1
        print(f"injected: {os.path.relpath(path, SITE)}")

print(f"{touched} page(s) updated, {len(pages)} scanned")
