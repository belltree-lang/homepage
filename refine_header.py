import os
import re

def refine_header_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The exact structure requested
    new_utility_nav = '''<div class="utility-nav">
            <a href="/community/index.html" class="utility-link">
              医療・介護関係者の皆様へ
            </a>
            <a href="/pages/recruit/index.html" class="utility-link recruit">
              採用情報
            </a>
          </div>'''

    # Find the existing utility-nav container (supporting both old nav and new div)
    pattern = re.compile(r'<(div|nav) class="(utility-nav|site-utility-nav)".*?>.*?</\1>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(new_utility_nav, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

root_dir = r'.'
updated_count = 0
for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            if refine_header_html(file_path):
                updated_count += 1

print(f"Refined header utility navigation in {updated_count} files.")
