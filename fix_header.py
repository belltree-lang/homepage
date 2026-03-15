import os
import re

def fix_utility_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the new utility nav HTML as requested by the user
    new_utility_nav = '''<div class="utility-nav">
            <a href="/community/" class="utility-link">
              医療・介護関係者の皆様へ
            </a>
            <a href="/recruit/" class="utility-link recruit">
              採用情報
            </a>
          </div>'''

    # Pattern to find the old utility nav (flexible for different relative paths or labels)
    # <nav class="site-utility-nav" ...> ... </nav>
    pattern = re.compile(r'<nav class="site-utility-nav".*?>.*?</nav>', re.DOTALL)
    
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
            if fix_utility_header(file_path):
                updated_count += 1

print(f"Updated header utility navigation in {updated_count} files.")
