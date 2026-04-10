import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BASE_DOMAIN = "https://bellmfit.com"

# Generic Open Graph Image (Assume logo or generic hero image is at root)
DEFAULT_OG_IMAGE = f"{BASE_DOMAIN}/assets/images/og-image.jpg"

def get_clean_url(file_path):
    rel_path = os.path.relpath(file_path, PROJECT_ROOT)
    url_path = rel_path.replace("\\", "/")
    if url_path == "index.html":
        return BASE_DOMAIN + "/"
    if url_path.endswith("index.html"):
        url_path = url_path[:-10]
    return f"{BASE_DOMAIN}/{url_path}"

def sync_seo_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "株式会社べるつりー | 地域で人生後半を支える総合サポート企業"

    # Extract description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', content, re.IGNORECASE | re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else "株式会社べるつりーは、運動から介護、終活までを支える地域密着型の総合サポート企業です。"

    canonical_url = get_clean_url(file_path)

    # SEO and OGP block
    seo_block = f"""
    <!-- SEO & OGP Config -->
    <link rel="canonical" href="{canonical_url}" />
    <meta property="og:type" content="{"website" if canonical_url == BASE_DOMAIN + "/" else "article"}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical_url}" />
    <meta property="og:image" content="{DEFAULT_OG_IMAGE}" />
    <meta property="og:site_name" content="株式会社べるつりー" />
    <meta name="twitter:card" content="summary_large_image" />
    <!-- /SEO & OGP Config -->
"""

    # First, remove existing SEO & OGP blocks to avoid duplicates
    content = re.sub(r'<!-- SEO & OGP Config -->.*?<!-- /SEO & OGP Config -->\s*', '', content, flags=re.DOTALL)
    
    # Also remove any standalone <link rel="canonical"...> or <meta property="og:..." just to be safe
    content = re.sub(r'<link\s+rel=["\']canonical["\'].*?>\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+property=["\']og:.*?["\'].*?>\s*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+name=["\']twitter:.*?["\'].*?>\s*', '', content, flags=re.IGNORECASE)

    # Insert new SEO block before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'{seo_block}</head>')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return True

def main():
    updated = 0
    exclude_dirs = {"templates", "scripts", "agents", ".git", ".github", "governance", "node_modules", "lolipop_staging", "reports", "assets"}
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file.endswith(".html") and file != "maintenance.html":
                file_path = os.path.join(root, file)
                try:
                    sync_seo_tags(file_path)
                    updated += 1
                except Exception as e:
                    print(f"Error on {file_path}: {e}")
                    
    print(f"SEO tags injected into {updated} files.")

if __name__ == "__main__":
    main()
