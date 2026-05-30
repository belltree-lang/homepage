"""絵文字をSVGアイコン (mask-image data URI) に全置換。
styles.cssの末尾にiconクラスを生成・追記、全HTMLの絵文字を <span class="icon icon-NAME" aria-hidden="true"></span> に置換。
☎ ✓ ☑ は文字記号として残す（CTA・チェックリスト機能）。
"""
import re
import urllib.parse
from pathlib import Path

ROOT = Path(r"c:/Users/sss_1/OneDrive/ドキュメント/GitHub/homepage - コピー")

# Lucide系SVG (1.5px stroke, viewBox 0 0 24 24)
ICONS = {
    "home":         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 2l9 7.5"/><path d="M5 8.5V21h14V8.5"/><path d="M9 21V12h6v9"/></svg>',
    "handshake":    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 17l2 2a1 1 0 1 0 3-3"/><path d="M14 14l2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="M21 3l-3 3 2 5"/><path d="M3 21l3-3-2-5"/><path d="M3 4l8.83.5a2 2 0 0 0 1.42-.25l.47-.28"/></svg>',
    "activity":     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
    "scale":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3.001 8A5.002 5.002 0 0 1 16 16"/><path d="m2 16 3-8 3.001 8A5.002 5.002 0 0 1 2 16"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>',
    "leaf":         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19.2 2.96c1.4 6.5.9 15.43-8.2 17.04Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/></svg>',
    "user":         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "users":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "clipboard":    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/></svg>',
    "alert":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "brain":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/></svg>',
    "footprints":   '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16v-2.38c0-.78.71-1.55 1.45-1.62l3.74-.4c.36-.04.7.13.84.41L11.4 16H4z"/><path d="M13 22V18s.95-1.5 1.05-2.45"/><path d="M14 14h6v6"/><path d="M14.1 8a1 1 0 0 1-1-1.5C13.84 5 14 2 14 2"/><path d="M4 8a1 1 0 0 0 1-1.5C4.16 5 4 2 4 2"/></svg>',
    "star":         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "stethoscope":  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>',
    "sprout":       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/></svg>',
    "filetext":     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/></svg>',
    "sparkles":     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/></svg>',
    "phone":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "shield":       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>',
    "needle":       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 3 3 21"/><path d="M14 8l-3-3"/><path d="M18 4l2 2"/></svg>',
    "flame":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/></svg>',
    "hands":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 11V6a2 2 0 0 0-4 0v6"/><path d="M14 10V4a2 2 0 0 0-4 0v6"/><path d="M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>',
    "pen":          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/></svg>',
    "dumbbell":     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.4 14.4 9.6 9.6"/><path d="M18.657 21.485a2 2 0 1 1-2.829-2.828l-1.767 1.768a2 2 0 1 1-2.829-2.829l6.364-6.364a2 2 0 1 1 2.829 2.829l-1.768 1.767a2 2 0 1 1 2.828 2.829z"/><path d="m21.5 21.5-1.4-1.4"/><path d="M3.9 3.9 2.5 2.5"/><path d="M6.404 12.768a2 2 0 1 1-2.829-2.829l1.768-1.767a2 2 0 1 1-2.828-2.829l2.828-2.828a2 2 0 1 1 2.829 2.828l1.767-1.768a2 2 0 1 1 2.829 2.829z"/></svg>',
    "mic":          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>',
    "heart":        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "yoga":         '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2"/><path d="M12 22V8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/><path d="M5 12c0 2 2 4 4 4"/><path d="M19 12c0 2-2 4-4 4"/></svg>',
}

EMOJI_MAP = {
    "🏠": "home", "🏡": "home",
    "🤝": "handshake",
    "🏃": "activity", "👟": "footprints", "🚶": "footprints", "🦵": "footprints", "🦶": "footprints",
    "⚖": "scale", "⚖️": "scale",
    "🍃": "leaf", "🌱": "sprout",
    "👤": "user",
    "👨": "users", "👩": "users", "👧": "users",
    "📋": "clipboard",
    "⚠": "alert", "⚠️": "alert",
    "🧠": "brain",
    "✦": "star", "✨": "sparkles",
    "🩺": "stethoscope",
    "📝": "filetext", "✍": "pen", "✍️": "pen",
    "📞": "phone",
    "🛡": "shield", "🛡️": "shield",
    "🪡": "needle",
    "🔥": "flame",
    "🙌": "hands",
    "💪": "dumbbell",
    "🎤": "mic",
    "🧡": "heart",
    "🧘": "yoga",
}

def encode_svg(svg: str) -> str:
    return urllib.parse.quote(svg, safe='/:?#[]@!$&()*+,;=')

# styles.cssに追加するicon CSS生成
def build_icon_css():
    lines = [
        "",
        "/* === Icon System (Lucide-style line icons, mask-image data URI) === */",
        ".icon {",
        "  display: inline-block;",
        "  width: 1em;",
        "  height: 1em;",
        "  vertical-align: -0.15em;",
        "  background-color: currentColor;",
        "  -webkit-mask-size: contain;",
        "  -webkit-mask-repeat: no-repeat;",
        "  -webkit-mask-position: center;",
        "  mask-size: contain;",
        "  mask-repeat: no-repeat;",
        "  mask-position: center;",
        "  flex-shrink: 0;",
        "}",
        ".icon-lg { width: 1.5em; height: 1.5em; }",
        ".icon-xl { width: 2em; height: 2em; }",
        ".icon-2xl { width: 3rem; height: 3rem; }",
        "",
    ]
    for name, svg in ICONS.items():
        encoded = encode_svg(svg)
        rule = f".icon-{name} {{ -webkit-mask-image: url(\"data:image/svg+xml,{encoded}\"); mask-image: url(\"data:image/svg+xml,{encoded}\"); }}"
        lines.append(rule)
    return "\n".join(lines) + "\n"

# styles.cssに追加（重複追加防止）
styles_path = ROOT / "styles.css"
styles_text = styles_path.read_text(encoding='utf-8')
if "/* === Icon System (Lucide-style line icons" not in styles_text:
    styles_text += build_icon_css()
    styles_path.write_text(styles_text, encoding='utf-8')
    print(f"styles.css に icon CSS 追加 (icons: {len(ICONS)})")
else:
    print("styles.css に既存の icon CSS あり (スキップ)")

# 全HTMLの絵文字を <span class="icon icon-XXX" aria-hidden="true"></span> に置換
import collections
PAGES = []
for sub in ['*.html', 'services/**/*.html', 'solutions/**/*.html']:
    PAGES.extend([str(p.relative_to(ROOT)).replace('\\', '/') for p in ROOT.glob(sub)])
PAGES += ['team/index.html', 'cases/index.html', 'community/index.html', 'family/index.html', 'contact/index.html', 'about/index.html']
PAGES = sorted(set(PAGES))

# 文字記号として残すもの
KEEP = {'☎', '✓', '☑', '☐'}

emoji_chars = set(EMOJI_MAP.keys())
# variation selector (FE0F) 対応のため、絵文字 + 任意のFE0Fも処理
emoji_re = re.compile('(' + '|'.join(re.escape(e) for e in sorted(EMOJI_MAP.keys(), key=len, reverse=True)) + ')(️)?')

def replace_one(m):
    e = m.group(1)
    name = EMOJI_MAP[e]
    return f'<span class="icon icon-{name}" aria-hidden="true"></span>'

per_file = {}
unknown_emojis = collections.Counter()
for rel in PAGES:
    p = ROOT / rel
    if not p.exists(): continue
    text = p.read_text(encoding='utf-8')
    orig = text
    text2 = emoji_re.sub(replace_one, text)
    # 残ったマッピング外絵文字をカウント
    rest = re.findall(r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F1FF\U0001F900-\U0001F9FF]', text2)
    for c in rest:
        if c not in KEEP:
            unknown_emojis[c] += 1
    if text2 != orig:
        p.write_text(text2, encoding='utf-8')
        per_file[rel] = orig.count('<span class="icon icon-')  # not exact but approximate
        diff = sum(1 for _ in emoji_re.finditer(orig))
        per_file[rel] = diff

print(f"\n置換完了: {len(per_file)} files, total {sum(per_file.values())} 件")
for rel, n in sorted(per_file.items(), key=lambda x: -x[1])[:10]:
    print(f"  {rel}: {n}件")
if unknown_emojis:
    print(f"\nマッピング外絵文字 (要追加): {dict(unknown_emojis)}")
