"""全ページのFAB（floating action button）を電話+フォーム+約束コピーの3要素構造に一括置換"""
import re
from pathlib import Path

ROOT = Path(r"c:/Users/sss_1/OneDrive/ドキュメント/GitHub/homepage - コピー")

PAGES = [
    "index.html",
    "services/index.html",
    "services/acupuncture/index.html",
    "services/fitness/index.html",
    "services/home-care/index.html",
    "services/leaf/index.html",
    "services/legal/index.html",
    "solutions/fall-risk/index.html",
    "solutions/frailty/index.html",
    "solutions/home-care-start/index.html",
    "solutions/knee-pain/index.html",
    "solutions/lower-back-pain/index.html",
    "solutions/parkinson/index.html",
    "solutions/stroke/index.html",
    "team/index.html",
    "cases/index.html",
    "about/index.html",
]

# 既存FAB（fab-label「ご相談はこちら」+ contactリンク1本）
OLD_RE = re.compile(
    r'    <div class="fab-container">\s*'
    r'<div class="fab-label">ご相談はこちら</div>\s*'
    r'<a href="([^"]+)" class="fab-button">\s*'
    r'<svg[^>]*>.*?</svg>\s*'
    r'<span>相談窓口</span>\s*'
    r'</a>\s*'
    r'</div>',
    re.DOTALL
)

PHONE_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MAIL_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

def new_fab(contact_path: str) -> str:
    return (
        '    <div class="fab-container">\n'
        '      <div class="fab-promise">電話でも、ご家族からでも。15分、状況をうかがいます。</div>\n'
        '      <a href="tel:0426822839" class="fab-button fab-button--phone" aria-label="電話 042-682-2839 で相談する">\n'
        f'        {PHONE_SVG}\n'
        '        <span>042-682-2839</span>\n'
        '      </a>\n'
        f'      <a href="{contact_path}" class="fab-button fab-button--form" aria-label="フォームで相談する">\n'
        f'        {MAIL_SVG}\n'
        '        <span>フォーム</span>\n'
        '      </a>\n'
        '    </div>'
    )

updated = []
skipped = []
for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        skipped.append((rel, 'file not found'))
        continue
    text = p.read_text(encoding='utf-8')
    m = OLD_RE.search(text)
    if not m:
        skipped.append((rel, 'pattern not matched'))
        continue
    new = OLD_RE.sub(lambda mm: new_fab(mm.group(1)), text)
    p.write_text(new, encoding='utf-8')
    updated.append(rel)

print(f"Updated {len(updated)} files:")
for u in updated:
    print(f"  ✓ {u}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for s, r in skipped:
        print(f"  - {s}: {r}")
