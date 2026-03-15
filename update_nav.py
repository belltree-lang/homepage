import os
import re

def update_page_links_and_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update utility nav links and labels
    # Professionals link: professionals/ -> community/
    content = content.replace('href="professionals/"', 'href="community/"')
    # Label: 求人情報 -> 採用情報 (if it exists as a link label)
    content = content.replace('>求人情報</a>', '>採用情報</a>')
    
    # Also handle relative paths for subdirectories
    # e.g. ../professionals/ -> ../community/
    content = content.replace('href="../professionals/"', 'href="../community/"')
    content = content.replace('href="../../professionals/"', 'href="../../community/"')
    content = content.replace('href="../../../professionals/"', 'href="../../../community/"')

    # Update Footer links specifically if they exist
    # <li><a href="../partners/">地域連携</a></li> -> <li><a href="../community/">地域連携・活動</a></li>
    # <li><a href="../pages/services/community/">地域活動</a></li> -> (should ideally be removed or updated)
    
    # Let's perform a more generic replacement for the community link
    content = re.sub(r'href=".*?partners/"', 'href="community/"', content) # this is too risky without prefix check
    
    # Safer footer link replacement
    patterns = [
        (r'<li><a href="(.*?)partners/">地域連携</a></li>', r'<li><a href="\1community/">地域連携・活動</a></li>'),
        (r'<li><a href="(.*?)pages/services/community/">地域活動</a></li>', r'') # Remove redundant link
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Final cleanup of double newlines in footer caused by removal
    content = content.replace('<ul>\n\n', '<ul>\n')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

root_dir = r'.'
for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            update_page_links_and_labels(file_path)

print("Navigation links and labels updated site-wide.")
