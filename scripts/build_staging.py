import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING_DIR = os.path.join(ROOT_DIR, "lolipop_staging")

print("=== Staging Build Started ===")

# アップロード対象ディレクトリ
TARGET_DIRS = [
    "about", "assets", "cases", "community", "contact", 
    "family", "model", "news", "privacy-policy", "recruit", 
    "scripts", "services", "solutions", "team", "terms-of-service"
]

# アップロード対象ファイル
TARGET_FILES = [
    "index.html", 
    "styles.css", 
    "siteData.json", 
    ".htaccess"
]

# 1. 既存の staging ディレクトリをクリーンアップ
if os.path.exists(STAGING_DIR):
    print(f"Cleaning up existing {STAGING_DIR}...")
    shutil.rmtree(STAGING_DIR)

os.makedirs(STAGING_DIR)

# 2. ディレクトリのコピー
for d in TARGET_DIRS:
    src_dir = os.path.join(ROOT_DIR, d)
    dest_dir = os.path.join(STAGING_DIR, d)
    if os.path.exists(src_dir) and os.path.isdir(src_dir):
        shutil.copytree(src_dir, dest_dir)
        print(f"Copied directory: {d}/")
    else:
        print(f"Warning: Directory {d} not found, skipping.")

# 3. ファイルのコピー
for f in TARGET_FILES:
    src_file = os.path.join(ROOT_DIR, f)
    dest_file = os.path.join(STAGING_DIR, f)
    if os.path.exists(src_file) and os.path.isfile(src_file):
        shutil.copy2(src_file, dest_file)
        print(f"Copied file: {f}")
    else:
        print(f"Warning: File {f} not found, skipping.")

print("\n=== Staging Build Complete ===")
print("対象データは `lolipop_staging/` に配置されました。")
print("このフォルダの中身をそのまま本番の `/test/` フォルダ配下にアップロードしてください。")
