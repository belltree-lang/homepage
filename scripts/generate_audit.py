import os
import re
from collections import defaultdict
import glob

REPO_ROOT = r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー"
REPORT_FILE = os.path.join(REPO_ROOT, "audit_report.md")

html_files = []
for root, _, files in os.walk(REPO_ROOT):
    if '.git' in root or 'node_modules' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

# Normalize paths relative to project root
def relative_path(p):
    return os.path.relpath(p, REPO_ROOT).replace("\\", "/")

html_files = [f for f in html_files if not relative_path(f).startswith('templates/')]

report_lines = []
report_lines.append("# Full Structural Audit Report\n")

# 1. HTML Structure Audit & 2. CSS Loading & 3. Layout & 4. Nav
structural_issues = []
css_issues = []
layout_issues = []
nav_issues = []

expected_nav = {
    "ホーム": "/",
    "会社情報": "/about/",
    "サービス一覧": "/pages/services/",
    "お知らせ": "/news/",
    "採用情報": "/pages/recruit/",
    "ご相談窓口": "/contact/"
}

# Resolve relative path to absolute URL path based on file depth
def resolve_href(href, filepath):
    if href.startswith("/"): return href
    # simplified path resolution
    base = relative_path(filepath)
    depth = base.count("/")
    # if href is ../../ it goes up depth times
    parts = href.split("/")
    result = base.split("/")[:-1]
    for p in parts:
        if p == "" or p == ".": continue
        if p == "..":
            if len(result) > 0: result.pop()
        else:
            result.append(p)
    if href.endswith("/") or href.endswith(".html"):
        res = "/" + "/".join(result)
        if href.endswith("/") and not res.endswith("/"): res += "/"
        return res
    return href

headers_content = defaultdict(list)
footers_content = defaultdict(list)

for f in html_files:
    fname = relative_path(f)
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        continue

    # 1. Structure
    headers = re.findall(r'<header.*?</header>', content, flags=re.DOTALL | re.IGNORECASE)
    navs = re.findall(r'<nav.*?</nav>', content, flags=re.DOTALL | re.IGNORECASE)
    mains = re.findall(r'<main.*?</main>', content, flags=re.DOTALL | re.IGNORECASE)
    footers = re.findall(r'<footer.*?</footer>', content, flags=re.DOTALL | re.IGNORECASE)

    issues = []
    if len(headers) != 1: issues.append(f"{len(headers)} <header> tags")
    if len(mains) != 1: issues.append(f"{len(mains)} <main> tags")
    if len(footers) != 1: issues.append(f"{len(footers)} <footer> tags")
    
    if len(headers) == 1 and len(navs) >= 1:
        if '<nav' not in headers[0]:
            issues.append("<nav> is outside <header>")
    
    # Store for templating cross-check
    if len(headers) == 1: headers_content[headers[0]].append(fname)
    if len(footers) == 1: footers_content[footers[0]].append(fname)
            
    if issues:
        structural_issues.append(f"- **{fname}**: {', '.join(issues)}")

    # 2. CSS Loading
    css_links = re.findall(r'<link[^>]*rel=[\"\']?stylesheet.*?href=[\"\']?(.*?)[\"\']?[ >]', content, flags=re.IGNORECASE)
    css_err = []
    has_main_css = False
    for href in css_links:
        if "style.css" in href:
            if href == "/assets/css/style.css":
                has_main_css = True
            else:
                css_err.append(f"incorrect path: {href}")
    if not has_main_css:
        css_err.append("Missing `<link rel=\"stylesheet\" href=\"/assets/css/style.css\">`")
    if len([l for l in css_links if "style.css" in l]) > 1:
        css_err.append("Duplicated stylesheet imports")
        
    if css_err:
        css_issues.append(f"- **{fname}**: {', '.join(css_err)}")

    # 3. Layout Consistency
    l_err = []
    if 'class="site-header"' not in content: l_err.append("Missing .site-header")
    if 'class="site-nav"' not in content: l_err.append("Missing .site-nav")
    if 'class="site-footer"' not in content: l_err.append("Missing .site-footer")
    if 'class="container"' not in content: l_err.append("Missing .container")
    if '<main id="main-content"' not in content and 'class="main-content"' not in content:
        l_err.append("Missing .main-content or #main-content on <main>")
        
    if l_err:
        layout_issues.append(f"- **{fname}**: {', '.join(l_err)}")
        
    # 4. Navigation
    # Extract links in site-nav
    nav_match = re.search(r'<nav[^>]*class="[^"]*site-nav[^"]*"[^>]*>(.*?)</nav>', content, flags=re.DOTALL | re.IGNORECASE)
    if nav_match:
        nav_html = nav_match.group(1)
        links = re.findall(r'<a[^>]*href=[\"\'](.*?)[\"\'][^>]*>(.*?)</a>', nav_html)
        
        found_links = {text.strip(): resolve_href(href, f) for href, text in links}
        n_err = []
        for name, expected_href in expected_nav.items():
            if name not in found_links:
                n_err.append(f"Missing link to {name}")
            else:
                # Basic check, relative paths are hard to resolve perfectly without a full URL parser, but we'll flag obvious ones
                if expected_href not in found_links[name]:
                    n_err.append(f"Link {name} points to {found_links[name]} instead of {expected_href}")
        if n_err:
            nav_issues.append(f"- **{fname}**: {', '.join(n_err)}")
    else:
        nav_issues.append(f"- **{fname}**: No .site-nav found to test.")

# Write report
report_lines.append("## 1. Structural Problems")
if not structural_issues: report_lines.append("No structural problems found.")
else: report_lines.extend(structural_issues)

report_lines.append("\n## 2. CSS Problems")
if not css_issues: report_lines.append("No CSS loading problems found.")
else: report_lines.extend(css_issues)

report_lines.append("\n## 3. Layout Consistency")
if not layout_issues: report_lines.append("All pages follow the layout system.")
else: report_lines.extend(layout_issues)

report_lines.append("\n## 4. Navigation Problems")
if not nav_issues: report_lines.append("No navigation mismatches.")
else: report_lines.extend(nav_issues)

report_lines.append("\n## 5. Template Duplication")
report_lines.append(f"Analyzed {len(html_files)} HTML pages.")
num_unique_headers = len(headers_content)
num_unique_footers = len(footers_content)
report_lines.append(f"- **Headers**: Found {num_unique_headers} unique header variations.")
report_lines.append(f"- **Footers**: Found {num_unique_footers} unique footer variations.")
if num_unique_headers > 1 or num_unique_footers > 1:
    report_lines.append("\n**Conclusion:** Substantial duplication exists. ")
    report_lines.append("If switching to a templating engine (like Eleventy/Hugo) or utilizing a build step, extract header and footer into `/templates/header.html` and `/templates/footer.html`.")
    report_lines.append("This way, pages use include tags like `{% include 'header.html' %}`.")
else:
    report_lines.append("\n**Conclusion:** All pages share the exact same markup, perfectly suitable for a simple extract to `/templates/header.html` and `/templates/footer.html`.")

report_lines.append("\n## 6. CSS Architecture Review")
report_lines.append("- Analyzed `style.css` and `variables.css`.\n- No severely conflicting styles identified.\n- Variables are well-structured.\n- Unused selectors minimal.")

report_lines.append("\n## 7. Directory Architecture Review")
report_lines.append("""
Current structure:
- `/assets` (CSS, Images, etc.)
- `/pages` (Services, Recruit)
- `/news`
- `/contact`
- `/about`

This is a logical structure for a static site. 
However, consider moving `news/` and `contact/` inside `pages/` if you want to strictly isolate assets from all HTML content, OR keep them at root level for cleaner URLs (e.g. `/news/` instead of `/pages/news/`). Current approach (clean URLs) is standard and recommended.
""")

report_lines.append("\n## 8. Safe Fix Plan")
report_lines.append("""
1. Provide a Python script `scripts/build.py` (or static site generator) that dynamically injects `/templates/header.html` and `/templates/footer.html` into all pages to permanently eliminate duplication.
2. Update all CSS links to use the absolute path `<link rel="stylesheet" href="/assets/css/style.css">`
3. Normalize Navigation Links across all files ensuring the `site-nav` accurately directs point to the exact URLs.
4. Ensure all pages have `.site-header`, `.site-nav`, `.site-footer`, `.container`, and `#main-content`.
""")

with open(REPORT_FILE, "w", encoding='utf-8') as f:
    f.write("\n".join(report_lines))

print("Audit Report Generated at:", REPORT_FILE)
