import os
import sys
import re

# Get absolute paths to the project root and templates
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
HEADER_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "header.html")
FOOTER_TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "footer.html")

# Read templates
with open(HEADER_TEMPLATE_PATH, "r", encoding="utf-8") as f:
    header_template = f.read()

with open(FOOTER_TEMPLATE_PATH, "r", encoding="utf-8") as f:
    footer_template = f.read()

def get_base_url(file_path):
    """Calculates the relative path back to the root directory for href base matching."""
    rel_path = os.path.relpath(PROJECT_ROOT, os.path.dirname(file_path))
    if rel_path == ".":
        return ""
    # Ensure forward slashes for URLs
    return rel_path.replace("\\", "/") + "/"

def sync_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    content = original_content
    base_url = get_base_url(file_path)
    
    # Rendered components for this specific file depth
    new_header = header_template.replace("{{base_url}}", base_url)
    new_footer = footer_template.replace("{{base_url}}", base_url)

    # 1. Update Header (and mobile menu)
    if "<!-- === HEADER_START === -->" in content and "<!-- === HEADER_END === -->" in content:
        # Easy path: markers already exist
        content = re.sub(
            r'<!-- === HEADER_START === -->.*?<!-- === HEADER_END === -->',
            new_header,
            content,
            flags=re.DOTALL
        )
    else:
        # Hard path: First run migration.
        # Remove old mobile menu precisely
        content = re.sub(
            r'<!-- Mobile Menu Drawer -->.*?<ul class="mobile-utility-list">.*?</ul>\s*</div>\s*</div>|<!-- Mobile Menu Drawer -->\s*<div id="mobile-menu" class="mobile-menu-overlay">.*?<a href="[^"]*">ホーム</a>.*?</div>\s*</div>',
            '',
            content,
            flags=re.DOTALL
        )
        # Verify alternative mobile menu removal
        content = re.sub(r'<div id="mobile-menu" class="mobile-menu-overlay">.*?<button class="mobile-close".*?</ul>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
        
        # Replace the old header with the new templated header (which includes the mobile menu inside)
        content = re.sub(
            r'<header class="site-header">.*?</header>',
            new_header,
            content,
            flags=re.DOTALL
        )

    # 2. Update Footer
    if "<!-- === FOOTER_START === -->" in content and "<!-- === FOOTER_END === -->" in content:
        content = re.sub(
            r'<!-- === FOOTER_START === -->.*?<!-- === FOOTER_END === -->',
            new_footer,
            content,
            flags=re.DOTALL
        )
    else:
        # First run migration for footer
        content = re.sub(
            r'<footer class="site-footer">.*?</footer>',
            new_footer,
            content,
            flags=re.DOTALL
        )

    # Write back if changed
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    updated_files = 0
    total_html_files = 0
    
    exclude_dirs = {"templates", "scripts", "agents", ".git", ".github", "governance", "node_modules"}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            if file.endswith(".html"):
                total_html_files += 1
                file_path = os.path.join(root, file)
                try:
                    updated = sync_file(file_path)
                    if updated:
                        rel_name = os.path.relpath(file_path, PROJECT_ROOT)
                        print(f"Updated: {rel_name}")
                        updated_files += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"--- Sync Complete ---")
    print(f"Total HTML files scanned: {total_html_files}")
    print(f"Files updated: {updated_files}")

if __name__ == "__main__":
    main()
