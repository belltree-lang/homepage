import os

root_dir = r'.'
for root, dirs, files in os.walk(root_dir):
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update footer label
            # Search for the specific footer link structure
            content = content.replace('community/">地域連携</a>', 'community/">地域連携・活動</a>')
            content = content.replace('community/">地域連携・地域活動</a>', 'community/">地域連携・活動</a>') # normalization
            
            # Double check recruitment label
            content = content.replace('>求人情報</a>', '>採用情報</a>')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

print("Final label polishing complete.")
