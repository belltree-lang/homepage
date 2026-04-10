import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEASUREMENT_ID = "G-RQRJ45S3V3"

ANALYTICS_BLOCK = f"""
    <!-- Analytics Config -->
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{MEASUREMENT_ID}');
    </script>
    <!-- /Analytics Config -->
"""

def inject_analytics(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove existing analytics block to avoid duplicates
    content = re.sub(r'<!-- Analytics Config -->.*?<!-- /Analytics Config -->\s*', '', content, flags=re.DOTALL)
    
    # Also remove any standing Google tags if they somehow exist outside the block
    content = re.sub(r'<script async src="https://www.googletagmanager.com/gtag/js\?id=.*?"></script>\s*', '', content)

    # Insert new analytics block before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'{ANALYTICS_BLOCK}</head>')
    else:
        print(f"Warning: </head> tag not found in {file_path}")
        return False

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    return True

def main():
    updated = 0
    # Following the exclusion pattern in inject_seo.py, but including templates might be useful for new pages.
    # However, to be safe and consistent with existing patterns, we'll exclude them but maybe specifically target the shell.
    exclude_dirs = {"scripts", "agents", ".git", ".github", "governance", "node_modules", "lolipop_staging", "reports", "assets"}
    
    target_templates = {"service-detail-shell.html"}

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
        
        for file in files:
            is_html = file.endswith(".html") and file != "maintenance.html"
            is_in_templates = os.path.basename(root) == "templates"
            
            if is_html:
                if is_in_templates and file not in target_templates:
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    if inject_analytics(file_path):
                        updated += 1
                except Exception as e:
                    print(f"Error on {file_path}: {e}")
                    
    print(f"Analytics tags injected into {updated} files.")

if __name__ == "__main__":
    main()
