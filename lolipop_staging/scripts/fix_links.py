import os
import re

base_dir = r"c:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー"

def fix_all_files():
    for root, dirs, files in os.walk(base_dir):
        if '.git' in root or '.gemini' in root or '.venv' in root:
            continue
        for file in files:
            if not file.endswith('.html') and not file.endswith('.htm'):
                continue
            
            filepath = os.path.join(root, file)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(filepath, 'r', encoding='shift_jis') as f:
                        content = f.read()
                except Exception:
                    print(f"Skipping {filepath} due to encoding issues")
                    continue
            
            original_content = content
            
            # 1. Global replacements
            content = content.replace("pages/services/", "services/")
            content = content.replace("pages/recruit/", "recruit/")
            content = content.replace("solutions/end-of-life-preparation/index.html", "services/shukatsu/index.html")
            
            # 2. Fix inner paths for moved directories
            rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
            if rel_path.startswith("services/") or rel_path.startswith("recruit/"):
                def remove_one_up(m):
                    attr = m.group(1)
                    val = m.group(2)
                    if val.startswith("../"):
                        return f'{attr}="{val[3:]}"'
                    return m.group(0)

                content = re.sub(r'(href|src)="([^"]+)"', remove_one_up, content)

            if content != original_content:
                # Write back using original encoding or just utf-8. Let's use utf-8 as project standard.
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {rel_path}")

if __name__ == "__main__":
    fix_all_files()
