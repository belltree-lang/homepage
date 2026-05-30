"""全ページのheader-ctaとmobile-menu-footerに電話CTAを追加"""
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

# Desktop header-cta（PCナビ右上）
HEADER_RE = re.compile(
    r'<div class="header-cta">\s*<a class="nav-cta" href="([^"]+)">ご相談窓口</a>\s*</div>',
    re.DOTALL
)
def new_header(m):
    return (
        '<div class="header-cta">\n'
        '          <a class="nav-cta nav-cta--phone" href="tel:0426822839" aria-label="電話 042-682-2839">☎ 042-682-2839</a>\n'
        f'          <a class="nav-cta" href="{m.group(1)}">ご相談窓口</a>\n'
        '        </div>'
    )

# Mobile menu footer（ドロワー最下部）
MOBILE_RE = re.compile(
    r'<a href="([^"]+)" class="nav-cta mobile-menu-cta">ご相談窓口</a>',
    re.DOTALL
)
def new_mobile(m):
    return (
        '<a href="tel:0426822839" class="nav-cta mobile-menu-cta mobile-menu-cta--phone" aria-label="電話 042-682-2839">☎ 042-682-2839</a>\n'
        f'        <a href="{m.group(1)}" class="nav-cta mobile-menu-cta">ご相談フォーム</a>'
    )

updated = []
skipped = []
for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        skipped.append((rel, 'not found'))
        continue
    text = p.read_text(encoding='utf-8')
    orig = text
    if HEADER_RE.search(text):
        text = HEADER_RE.sub(new_header, text)
    if MOBILE_RE.search(text):
        text = MOBILE_RE.sub(new_mobile, text)
    if text == orig:
        skipped.append((rel, 'no patterns matched'))
        continue
    p.write_text(text, encoding='utf-8')
    updated.append(rel)

print(f"Updated {len(updated)} files")
for u in updated:
    print(f"  ✓ {u}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for s, r in skipped:
        print(f"  - {s}: {r}")
