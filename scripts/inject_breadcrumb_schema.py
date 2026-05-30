"""全ページの既存 <ol class='breadcrumb-list'> を解析し、BreadcrumbList JSON-LD を </head> 直前に注入"""
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(r"c:/Users/sss_1/OneDrive/ドキュメント/GitHub/homepage - コピー")
BASE_URL = "https://bellmfit.com"

PAGES = [
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

class BreadcrumbExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []  # list of (name, href_or_None)
        self.in_ol = False
        self.in_li = False
        self.in_a = False
        self.current_a_href = None
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == 'ol' and 'breadcrumb-list' in attrs_d.get('class', ''):
            self.in_ol = True
        elif self.in_ol and tag == 'li':
            self.in_li = True
            self.current_text = ""
            self.current_a_href = None
        elif self.in_li and tag == 'a':
            self.in_a = True
            self.current_a_href = attrs_d.get('href')

    def handle_endtag(self, tag):
        if tag == 'ol' and self.in_ol:
            self.in_ol = False
        elif tag == 'li' and self.in_li:
            self.in_li = False
            name = self.current_text.strip()
            if name:
                self.items.append((name, self.current_a_href))
        elif tag == 'a' and self.in_a:
            self.in_a = False

    def handle_data(self, data):
        if self.in_li:
            self.current_text += data

def resolve_href(href: str, current_dir_url: str) -> str:
    """相対パス -> 絶対URL"""
    if href.startswith(('http://', 'https://')):
        return href
    if href.startswith('/'):
        return BASE_URL + href
    # 相対パス（../../ など）
    parts = current_dir_url.rstrip('/').split('/')
    href_parts = href.split('/')
    i = 0
    while i < len(href_parts) and href_parts[i] == '..':
        parts.pop()
        i += 1
    rest = '/'.join(href_parts[i:])
    base = '/'.join(parts)
    return base + '/' + rest if rest else base + '/'

def page_url(rel: str) -> str:
    url = BASE_URL + '/' + rel
    if url.endswith('/index.html'):
        url = url[:-10]  # remove index.html, keep trailing /
    return url

def build_jsonld(items, current_url):
    """items: [(name, href_or_None)]"""
    list_items = []
    current_dir = current_url.rsplit('/', 1)[0] if not current_url.endswith('/') else current_url[:-1]
    for i, (name, href) in enumerate(items, start=1):
        entry = {"@type": "ListItem", "position": i, "name": name}
        if href:
            entry["item"] = resolve_href(href, current_dir)
        list_items.append(entry)
    if list_items and 'item' not in list_items[-1]:
        # current page has no href, use current URL
        list_items[-1]["item"] = current_url
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": list_items
    }

import json

updated = []
skipped = []
for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        skipped.append((rel, 'not found'))
        continue
    text = p.read_text(encoding='utf-8')
    # Skip if already has BreadcrumbList JSON-LD
    if 'BreadcrumbList' in text:
        skipped.append((rel, 'already has BreadcrumbList'))
        continue
    parser = BreadcrumbExtractor()
    parser.feed(text)
    if not parser.items:
        skipped.append((rel, 'no breadcrumb found'))
        continue
    url = page_url(rel)
    jsonld = build_jsonld(parser.items, url)
    json_str = json.dumps(jsonld, ensure_ascii=False, indent=6)
    script_block = (
        '\n    <!-- Schema.org JSON-LD: BreadcrumbList -->\n'
        '    <script type="application/ld+json">\n'
        f'    {json_str}\n'
        '    </script>\n'
    )
    # Insert before </head>
    new_text = text.replace('</head>', script_block + '</head>', 1)
    if new_text == text:
        skipped.append((rel, '</head> not found'))
        continue
    p.write_text(new_text, encoding='utf-8')
    updated.append((rel, [n for n, _ in parser.items]))

print(f"Updated {len(updated)} files:")
for rel, items in updated:
    print(f"  ✓ {rel}: {' > '.join(items)}")
if skipped:
    print(f"\nSkipped {len(skipped)}:")
    for s, r in skipped:
        print(f"  - {s}: {r}")
