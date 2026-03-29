import os
import re

REPO_ROOT = r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー"

nav_map = {
    'ホーム': '/',
    '会社情報': '/about/',
    'サービス一覧': '/pages/services/',
    'お知らせ': '/news/',
    '採用情報': '/pages/recruit/',
    'ご相談窓口': '/contact/',
    'Home': '/',
    'About': '/about/',
    'Services': '/pages/services/',
    'News': '/news/',
    'Recruit': '/pages/recruit/',
    'Contact': '/contact/'
}

html_files = []
for root, _, files in os.walk(REPO_ROOT):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

# Required literal string
EXPECTED_CSS_LINK = '<link rel="stylesheet" href="/assets/css/style.css">'

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Skipping {f}: {e}")
        continue

    orig_content = content

    # 1 & 3: Fix CSS typo, remove duplicates, ensure correct path
    # Remove ALL <link ... style.css ... > tags completely and any trailing whitespace
    content = re.sub(r'[ \t]*<link[^>]*href=[\"\'][^\"\']*style\.css[\"\'][^>]*>\s*', '', content, flags=re.IGNORECASE)
    
    # Insert exactly one correct CSS link before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'  {EXPECTED_CSS_LINK}\n</head>', 1)
    
    # 2. Normalize Navigation Links
    # Update href of exactly matching anchor text nodes to ensure absolute path
    for text, url in nav_map.items():
        # Match <a ...>text</a>, preserving attributes like class, aria-current etc.
        # Group 1 (<a ... ) up to href attribute.
        # Group 2 ( ... > ) the rest of the anchor start tag.
        
        # We need a robust matching since the existing href could be anywhere in the attributes.
        # Best approach: find all anchors containing the exact text. Then string replace their href value.
        pattern = r'(<a\s+[^>]*?)href=[\"\'][^\"\']*[\"\']([^>]*>\s*)' + re.escape(text) + r'(\s*</a>)'
        replacement = r'\g<1>href="' + url + r'"\g<2>' + text + r'\g<3>'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    if orig_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated {os.path.relpath(f, REPO_ROOT)}")

print("Fix completed.")
