"""全ページの Google Fonts <link> を Shippori Mincho B1 入りに統一"""
import re
from pathlib import Path

ROOT = Path(r"c:/Users/sss_1/OneDrive/ドキュメント/GitHub/homepage - コピー")

PAGES = [
    "index.html",
    "services/index.html",
    "services/acupuncture/index.html",
    "services/fitness/index.html",
    "services/fitness/seed/index.html",
    "services/fitness/night/index.html",
    "services/home-care/index.html",
    "services/leaf/index.html",
    "services/legal/index.html",
    "services/shukatsu/index.html",
    "solutions/index.html",
    "solutions/fall-risk/index.html",
    "solutions/frailty/index.html",
    "solutions/home-care-start/index.html",
    "solutions/knee-pain/index.html",
    "solutions/lower-back-pain/index.html",
    "solutions/parkinson/index.html",
    "solutions/stroke/index.html",
    "team/index.html",
    "cases/index.html",
    "community/index.html",
    "family/index.html",
    "contact/index.html",
    "about/index.html",
]

# 既存 Google Fonts <link>
OLD_LINK_RE = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?family=Noto\+Sans\+JP:wght@400;500;600;700&display=swap" rel="stylesheet" />'
)
NEW_LINK = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&family=Shippori+Mincho+B1:wght@500;700;800&display=swap" rel="stylesheet" />'

updated = []
skipped = []
for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        skipped.append((rel, 'not found'))
        continue
    text = p.read_text(encoding='utf-8')
    if 'Shippori+Mincho+B1' in text:
        skipped.append((rel, 'already loaded'))
        continue
    if not OLD_LINK_RE.search(text):
        skipped.append((rel, 'pattern not matched'))
        continue
    new = OLD_LINK_RE.sub(NEW_LINK, text)
    p.write_text(new, encoding='utf-8')
    updated.append(rel)

print(f"Updated {len(updated)} files")
for u in updated:
    print(f"  ✓ {u}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for s, r in skipped:
        print(f"  - {s}: {r}")
