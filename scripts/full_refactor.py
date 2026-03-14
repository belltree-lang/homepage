import os
import re

# Standard Header HTML
header_html = """    <header class="site-header">
      <div class="container site-header-inner">
        <a class="site-logo" href="/">BellTree</a>
        <nav class="site-nav" aria-label="主要ナビゲーション">
          <a href="/">ホーム</a>
          <a href="/about/">会社情報</a>
          <a href="/pages/services/">サービス一覧</a>
          <a href="/news/">お知らせ</a>
          <a href="/pages/recruit/">採用情報</a>
          <a class="nav-cta" href="/contact/">ご相談窓口</a>
        </nav>
      </div>
    </header>"""

# Standard Footer HTML
footer_html = """    <footer class="site-footer">
      <div class="container">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="footer-logo">BellTree</div>
            <p style="opacity: 0.8; line-height: 1.6;">株式会社べるつりー<br/>運動から介護、終活までを横断し、地域で人生後半を支える総合サポート企業です。</p>
            <p style="opacity: 0.8; font-size: var(--font-size-sm); margin-top: auto;">東京都町田市<br/><a href="mailto:info@example.com">info@example.com</a></p>
          </div>
          <div class="footer-nav">
            <h3>企業情報</h3>
            <ul>
              <li><a href="/">ホーム</a></li>
              <li><a href="/about/">会社概要・理念</a></li>
              <li><a href="/news/">お知らせ・地域活動</a></li>
              <li><a href="/pages/recruit/">採用情報</a></li>
              <li><a href="/contact/">お問い合わせ</a></li>
            </ul>
          </div>
          <div class="footer-nav">
            <h3>サービス</h3>
            <ul>
              <li><a href="/pages/services/">サービス一覧</a></li>
              <li><a href="/pages/services/fitness/">べるフィット (運動支援)</a></li>
              <li><a href="/pages/services/acupuncture/">訪問鍼灸マッサージ (在宅支援)</a></li>
              <li><a href="/pages/services/home-care/">居宅介護支援 (制度活用)</a></li>
              <li><a href="/pages/services/legal/">べるリーガル (行政書士)</a></li>
            </ul>
          </div>
          <div class="footer-nav">
            <h3>コミュニティ</h3>
            <ul>
              <li><a href="/pages/services/community/">地域活動</a></li>
              <li><a href="/pages/services/community/#partners">パートナーシップ</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; BellTree Inc. All Rights Reserved.</p>
        </div>
      </div>
    </footer>"""

def fix_html_content(content):
    # 1. Standardize stylesheet link
    content = re.sub(r'<link rel="stylesheet" href="[^"]*?assets/css/style\.css">', r'<link rel="stylesheet" href="/assets/css/style.css">', content)
    
    # 2. Standardize Header
    content = re.sub(r'<header[^>]*?class="site-header"[^>]*>.*?</header>', header_html, content, flags=re.DOTALL)
    
    # 3. Standardize Footer
    content = re.sub(r'<footer[^>]*?class="site-footer"[^>]*>.*?</footer>', footer_html, content, flags=re.DOTALL)
    
    # 4. Correct conversion of relative paths to absolute root paths
    # Matches href="../", href="../../", href="../../../" etc., and replaces with /
    content = re.sub(r'href="\.\.(?:/\.\.)*/*', 'href="/', content)
    content = re.sub(r'src="\.\.(?:/\.\.)*/*', 'src="/', content)
    
    # Special fix for cases where my previous script added /../
    content = re.sub(r'href="/\.\./+', 'href="/', content)
    content = re.sub(r'src="/\.\./+', 'src="/', content)

    # Ensure all local paths for specific folders start with /
    # This avoids adding / to external links (http)
    folders = ['pages', 'news', 'about', 'contact', 'assets']
    for folder in folders:
        content = re.sub(rf'href="{re.escape(folder)}/', rf'href="/{folder}/', content)
        content = re.sub(rf'src="{re.escape(folder)}/', rf'src="/{folder}/', content)
        
    return content

def run_refactor(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Skip internal directories
        if any(skip in root for skip in ['.git', 'agents', 'governance', 'tasks', 'reports', 'scripts']):
            continue
            
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = fix_html_content(content)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Standardized: {file_path}")

if __name__ == "__main__":
    base_dir = r"c:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー"
    run_refactor(base_dir)
