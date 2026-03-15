import os

# Target absolute paths we want to convert to relative
targets = {
    '/community/index.html': 'community/index.html',
    '/pages/recruit/index.html': 'pages/recruit/index.html'
}

root_dir = os.getcwd()

def get_rel_path(src_file, target_rel_root):
    # target_rel_root is something like 'community/index.html'
    # src_file is absolute path to the file we are editing
    src_dir = os.path.dirname(src_file)
    # Calculate relative back to root
    back_to_root = os.path.relpath(root_dir, src_dir)
    # Join and normalize
    # rel_link = os.path.normpath(os.path.join(back_to_root, target_rel_root)).replace('\\', '/')
    # Actually, os.path.relpath from src_dir to the absolute target path is better
    abs_target = os.path.join(root_dir, target_rel_root)
    rel_link = os.path.relpath(abs_target, src_dir).replace('\\', '/')
    return rel_link

for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for abs_path, rel_root_path in targets.items():
                rel_link = get_rel_path(file_path, rel_root_path)
                # We look for href="/path" or href='/path'
                content = content.replace(f'href="{abs_path}"', f'href="{rel_link}"')
                content = content.replace(f"href='{abs_path}'", f"href='{rel_link}'")
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed paths in {file_path}")

print("Path correction complete.")
