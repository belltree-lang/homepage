# Bellmfit SEO Quick Wins Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** bellmfit.com の既存9ページに、代表確認済みのSEO文言、駐車場情報、リーフ満員時の代替導線を追加し、`staging` の `/test/` 環境で安全性と表示を検証する。

**Architecture:** 静的HTML9ファイルだけを直接編集し、既存のページ固有構造と共通ユーティリティを再利用する。フッターNAPは各ファイルへ同一文字列を個別挿入し、canonical、本番用ワークフロー、共通CSS、別サイト複製には触れない。

**Tech Stack:** Static HTML, existing CSS utilities, PowerShell, Python standard library, Git/GitHub Actions, curl

---

## File Map

- Create: `tasks/_active/task-063-bellmfit-seo-quick-wins.md` — 実行範囲と完了条件
- Modify: `index.html` — トップtitle/description、駐車場ブロック、フッターNAP
- Modify: `contact/index.html` — 既存アクセス節の駐車場ブロック、フッターNAP
- Modify: `services/leaf/index.html` — description、満員時導線、フッターNAP
- Modify: `services/fitness/index.html` — フッターNAPだけ
- Modify: `services/fitness/night/index.html` — フッターNAPだけ
- Modify: `services/fitness/seed/index.html` — フッターNAPだけ
- Modify: `price/index.html` — フッターNAPだけ
- Modify: `privacy-policy/index.html` — 現状構造内のフッターNAPだけ
- Modify: `terms-of-service/index.html` — 現状構造内のフッターNAPだけ
- Create: `reports/2026-08-02-bellmfit-seo-quick-wins.md` — 差分、実物文言、検証、スクリーンショット索引
- Create: `reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/*.png` — ステージング表示証跡
- Move: `tasks/_active/task-063-bellmfit-seo-quick-wins.md` → `tasks/_completed/task-063-bellmfit-seo-quick-wins.md` — 全検証後の状態更新

## Fixed Content

トップtitle:

```text
町田のジム べるフィット｜メディカルフィットネス・駐車場無料
```

トップdescription:

```text
町田市木曽東のメディカルフィットネス。健康運動指導士や鍼灸マッサージ師などの専門職が無理のない運動をご案内。平日夜間・週末のナイト、女性向けのシード、介護保険で通えるリーフの3つの通い方。駐車場10台・無料。見学・体験を受け付けています。
```

リーフdescription:

```text
べるフィットのリーフは、介護保険の総合事業で通える「保険が使えるジム」です。現在は多くの時間帯が満員で、空きは限られています（最新の空き状況をページに掲載）。自費で通えるシード（女性向け）・ナイト（夜間・週末）もご案内しています。
```

フッターNAP駐車場行:

```text
駐車場10台・無料（施設向かい2台／近隣提携8台）
```

### Task 1: Register the Active Task and Record Safety Baseline

**Files:**
- Create: `tasks/_active/task-063-bellmfit-seo-quick-wins.md`
- Verify: `.github/workflows/deploy-staging.yml`
- Verify: nine canonical tags

- [ ] **Step 1: Create the active task with the approved scope**

```markdown
# Task 063 – Bellmfit SEO Quick Wins

## Goal
既存9ページの検索結果表現、駐車場情報、リーフ満員時導線を改善し、ステージングで検証する。

## Scope
- index.html
- contact/index.html
- services/leaf/index.html
- services/fitness/index.html
- services/fitness/night/index.html
- services/fitness/seed/index.html
- price/index.html
- privacy-policy/index.html
- terms-of-service/index.html
- reports/2026-08-02-bellmfit-seo-quick-wins.md
- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/

## Constraints
- stagingのみへpushする
- deploy.ymlを起動しない
- canonicalを書き換えない
- footerの駐車場行は9ページで完全一致させる
- privacy-policyとterms-of-serviceのフッター構造を変えない
- git add . / git add -Aを使わない

## Acceptance Criteria
- ローカル9URLが200で、内部リンク・画像切れがない
- stagingのX-Robots-Tagがnoindex, nofollow
- staging 9URLの表示・canonical・リンク・画像が正常
- トップ画像合計容量が基準約1.15MBから悪化していない
- トップ、contact、leafのスクリーンショットと報告がある

## Dependencies
- docs/superpowers/specs/2026-08-02-bellmfit-seo-quick-wins-design.md

## Parallel Safety
- 対象9HTMLとstagingブランチを専有する
```

- [ ] **Step 2: Confirm the branch baseline**

Run:

```powershell
git status --short --branch
git rev-parse --abbrev-ref HEAD
git merge-base --is-ancestor origin/main HEAD
if ($LASTEXITCODE -ne 0) { throw 'staging worktree does not contain the latest origin/main' }
git rev-list --left-right --count origin/main...HEAD
```

Expected: branch is `staging`; `origin/main` is an ancestor; the left count is `0` and the right count consists only of the approved local design/plan commits.

- [ ] **Step 3: Record the exact canonical baseline**

Run:

```powershell
$pages = @('index.html','services/fitness/index.html','services/fitness/night/index.html','services/fitness/seed/index.html','services/leaf/index.html','price/index.html','terms-of-service/index.html','contact/index.html','privacy-policy/index.html')
foreach ($page in $pages) {
  $canonical = Select-String -LiteralPath $page -Pattern '<link rel="canonical"' | ForEach-Object { $_.Line.Trim() }
  "$page`t$canonical"
}
```

Expected: every value points to `https://bellmfit.com/...`; none points to `/test/`.

- [ ] **Step 4: Run the pre-change assertion and confirm it fails**

Run:

```powershell
$expected = '駐車場10台・無料（施設向かい2台／近隣提携8台）'
$pages = @('index.html','services/fitness/index.html','services/fitness/night/index.html','services/fitness/seed/index.html','services/leaf/index.html','price/index.html','terms-of-service/index.html','contact/index.html','privacy-policy/index.html')
$bad = $pages | Where-Object { ([regex]::Matches((Get-Content -LiteralPath $_ -Raw), [regex]::Escape($expected))).Count -ne 1 }
if ($bad.Count -eq 0) { throw 'Expected the pre-change NAP assertion to fail.' }
$bad
```

Expected: all nine pages are listed because the new NAP line is absent.

### Task 2: Update the Homepage Metadata, Access Block, and Footer

**Files:**
- Modify: `index.html:6-7`
- Modify: `index.html:614-626`
- Modify: `index.html:791-795`

- [ ] **Step 1: Replace the homepage title and description**

```html
<title>町田のジム べるフィット｜メディカルフィットネス・駐車場無料</title>
<meta name="description" content="町田市木曽東のメディカルフィットネス。健康運動指導士や鍼灸マッサージ師などの専門職が無理のない運動をご案内。平日夜間・週末のナイト、女性向けのシード、介護保険で通えるリーフの3つの通い方。駐車場10台・無料。見学・体験を受け付けています。" />
```

- [ ] **Step 2: Add the parking block between the access paragraph and map**

```html
<div class="card mt-xl">
  <h3>お車でお越しの方へ</h3>
  <p class="text-muted mb-0">施設の向かいに2台、近隣の提携駐車場に8台、あわせて10台分をご用意しています。いずれも無料でご利用いただけます。</p>
</div>
```

- [ ] **Step 3: Add the exact parking line inside the existing footer NAP paragraph**

```html
東京都町田市木曽東4-9-14 Mビル2階<br/>
駐車場10台・無料（施設向かい2台／近隣提携8台）<br/>
TEL <a href="tel:0426822839">042-682-2839</a>／営業時間 平日 9:00〜18:00
```

- [ ] **Step 4: Confirm the homepage canonical was not changed**

Run: `Select-String -LiteralPath index.html -Pattern '<link rel="canonical" href="https://bellmfit.com/" />'`

Expected: exactly one match.

### Task 3: Extend the Existing Contact Access Section

**Files:**
- Modify: `contact/index.html:338-350`
- Modify: `contact/index.html:367-371`

- [ ] **Step 1: Add the parking block between the existing contact access paragraph and map**

The address, hours, and map already exist. Do not duplicate or rebuild the section. Insert only:

```html
<div class="card mt-xl">
  <h3>お車でお越しの方へ</h3>
  <p class="text-muted mb-0">施設の向かいに2台、近隣の提携駐車場に8台、あわせて10台分をご用意しています。いずれも無料でご利用いただけます。</p>
</div>
```

- [ ] **Step 2: Add the exact parking line inside the existing contact footer NAP paragraph**

```html
東京都町田市木曽東4-9-14 Mビル2階<br/>
駐車場10台・無料（施設向かい2台／近隣提携8台）<br/>
TEL <a href="tel:0426822839">042-682-2839</a>／営業時間 平日 9:00〜18:00
```

- [ ] **Step 3: Confirm the contact canonical remains production-facing**

Run: `Select-String -LiteralPath contact/index.html -Pattern 'href="https://bellmfit.com/contact/"'`

Expected: exactly one match.

### Task 4: Add the Leaf Full-Capacity Routing

**Files:**
- Modify: `services/leaf/index.html:7`
- Modify: `services/leaf/index.html:395-403`
- Modify: `services/leaf/index.html:503-507`

- [ ] **Step 1: Replace only the Leaf meta description**

```html
<meta name="description" content="べるフィットのリーフは、介護保険の総合事業で通える「保険が使えるジム」です。現在は多くの時間帯が満員で、空きは限られています（最新の空き状況をページに掲載）。自費で通えるシード（女性向け）・ナイト（夜間・週末）もご案内しています。" />
```

- [ ] **Step 2: Insert the alternative-course block after `.vacancy-notice` and before the existing contact CTA**

```html
<div class="card mt-xl">
  <h3>ご希望の時間帯が満員の場合</h3>
  <p class="text-muted">介護保険を使わず、自費で通えるコースもあります。</p>
  <ul>
    <li><a href="../fitness/seed/index.html">シード（女性向け・日中）</a></li>
    <li><a href="../fitness/night/index.html">ナイト（平日夜間・週末）</a></li>
  </ul>
  <p class="text-muted mb-0">どちらも見学・体験を受け付けています。</p>
</div>
```

- [ ] **Step 3: Add the exact parking line inside the existing Leaf footer NAP paragraph**

```html
東京都町田市木曽東4-9-14 Mビル2階<br/>
駐車場10台・無料（施設向かい2台／近隣提携8台）<br/>
TEL <a href="tel:0426822839">042-682-2839</a>／営業時間 平日 9:00〜18:00
```

- [ ] **Step 4: Confirm the vacancy table and canonical are unchanged**

Run:

```powershell
git diff -- services/leaf/index.html
Select-String -LiteralPath services/leaf/index.html -Pattern 'href="https://bellmfit.com/services/leaf/"'
```

Expected: diff contains only the description, new routing block, and footer line; canonical has one match; table rows and vacancy script have no diff.

### Task 5: Add the Exact Footer NAP Line to the Remaining Six Pages

**Files:**
- Modify: `services/fitness/index.html:416-420`
- Modify: `services/fitness/night/index.html:452-456`
- Modify: `services/fitness/seed/index.html:451-455`
- Modify: `price/index.html:452-456`
- Modify: `privacy-policy/index.html:219-223`
- Modify: `terms-of-service/index.html:336-340`

- [ ] **Step 1: Insert the same exact line into each file**

In each existing `<p class="footer-nap">`, insert this one line between address and telephone:

```html
駐車場10台・無料（施設向かい2台／近隣提携8台）<br/>
```

- [ ] **Step 2: Preserve the privacy-policy and terms-of-service footer structure**

Run:

```powershell
git diff --unified=1 -- privacy-policy/index.html terms-of-service/index.html
```

Expected: each file has one added parking line and no other footer or page changes.

- [ ] **Step 3: Run the exact-string assertion**

Run:

```powershell
$expected = '駐車場10台・無料（施設向かい2台／近隣提携8台）'
$pages = @('index.html','services/fitness/index.html','services/fitness/night/index.html','services/fitness/seed/index.html','services/leaf/index.html','price/index.html','terms-of-service/index.html','contact/index.html','privacy-policy/index.html')
$bad = $pages | Where-Object { ([regex]::Matches((Get-Content -LiteralPath $_ -Raw), [regex]::Escape($expected))).Count -ne 1 }
if ($bad.Count) { throw "NAP mismatch: $($bad -join ', ')" }
'PASS: exact parking NAP appears once in all 9 pages'
```

Expected: `PASS: exact parking NAP appears once in all 9 pages`.

### Task 6: Run Local Structural and HTTP Verification

**Files:**
- Verify: all nine target HTML files
- Verify: local image/CSS/JS references

- [ ] **Step 1: Verify metadata and canonical values exactly**

Run:

```powershell
$top = Get-Content -LiteralPath index.html -Raw
$leaf = Get-Content -LiteralPath services/leaf/index.html -Raw
if ($top -notmatch [regex]::Escape('<title>町田のジム べるフィット｜メディカルフィットネス・駐車場無料</title>')) { throw 'top title mismatch' }
if ($top -notmatch [regex]::Escape('町田市木曽東のメディカルフィットネス。健康運動指導士や鍼灸マッサージ師などの専門職が無理のない運動をご案内。平日夜間・週末のナイト、女性向けのシード、介護保険で通えるリーフの3つの通い方。駐車場10台・無料。見学・体験を受け付けています。')) { throw 'top description mismatch' }
if ($leaf -notmatch [regex]::Escape('べるフィットのリーフは、介護保険の総合事業で通える「保険が使えるジム」です。現在は多くの時間帯が満員で、空きは限られています（最新の空き状況をページに掲載）。自費で通えるシード（女性向け）・ナイト（夜間・週末）もご案内しています。')) { throw 'leaf description mismatch' }
$canonicals = @{
  'index.html'='https://bellmfit.com/'; 'services/fitness/index.html'='https://bellmfit.com/services/fitness/';
  'services/fitness/night/index.html'='https://bellmfit.com/services/fitness/night/'; 'services/fitness/seed/index.html'='https://bellmfit.com/services/fitness/seed/';
  'services/leaf/index.html'='https://bellmfit.com/services/leaf/'; 'price/index.html'='https://bellmfit.com/price/';
  'terms-of-service/index.html'='https://bellmfit.com/terms-of-service/'; 'contact/index.html'='https://bellmfit.com/contact/';
  'privacy-policy/index.html'='https://bellmfit.com/privacy-policy/'
}
foreach ($pair in $canonicals.GetEnumerator()) {
  $html = Get-Content -LiteralPath $pair.Key -Raw
  $tag = '<link rel="canonical" href="' + $pair.Value + '" />'
  if (([regex]::Matches($html, [regex]::Escape($tag))).Count -ne 1) { throw "canonical mismatch: $($pair.Key)" }
}
'PASS: metadata and production canonicals'
```

Expected: `PASS: metadata and production canonicals`.

- [ ] **Step 2: Verify local link and asset targets using the Python standard library**

Run:

```powershell
@'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

root = Path.cwd().resolve()
pages = [Path(p) for p in [
    'index.html','services/fitness/index.html','services/fitness/night/index.html',
    'services/fitness/seed/index.html','services/leaf/index.html','price/index.html',
    'terms-of-service/index.html','contact/index.html','privacy-policy/index.html'
]]

class Refs(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src'):
            if key in attrs: self.refs.append(attrs[key])

missing = []
for page in pages:
    parser = Refs(); parser.feed(page.read_text(encoding='utf-8'))
    for ref in parser.refs:
        if not ref or ref.startswith(('#','tel:','mailto:','javascript:','data:')): continue
        parsed = urlparse(ref)
        if parsed.scheme or parsed.netloc: continue
        local = unquote(parsed.path)
        target = (root / local.lstrip('/')) if local.startswith('/') else (page.parent / local)
        if local.endswith('/') or not target.suffix: target = target / 'index.html'
        if not target.resolve().exists(): missing.append(f'{page}: {ref}')
if missing:
    raise SystemExit('Missing local references:\n' + '\n'.join(missing))
print('PASS: local HTML links and assets resolve')
'@ | python -
```

Expected: `PASS: local HTML links and assets resolve`.

- [ ] **Step 3: Measure the homepage image payload**

Run:

```powershell
@'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

class Images(HTMLParser):
    def __init__(self): super().__init__(); self.srcs=[]
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            value = dict(attrs).get('src')
            if value: self.srcs.append(value)

root=Path.cwd(); page=root/'index.html'; parser=Images(); parser.feed(page.read_text(encoding='utf-8'))
files=[]
for src in parser.srcs:
    parsed=urlparse(src)
    if parsed.scheme or parsed.netloc: continue
    path=(page.parent/unquote(parsed.path)).resolve()
    if path.exists(): files.append(path)
total=sum(path.stat().st_size for path in set(files))
print(f'Homepage image bytes: {total} ({total/1024/1024:.2f} MiB), files: {len(set(files))}')
if total > 1_250_000: raise SystemExit('Homepage image payload regressed above 1,250,000 bytes')
'@ | python -
```

Expected: approximately 1.15MB and no regression failure.

- [ ] **Step 4: Start a hidden local server and verify nine HTTP 200 responses**

Run:

```powershell
$server = Start-Process -FilePath python -ArgumentList '-m','http.server','8765','--bind','127.0.0.1' -WorkingDirectory (Get-Location) -WindowStyle Hidden -PassThru
try {
  $paths = @('/','/services/fitness/','/services/fitness/night/','/services/fitness/seed/','/services/leaf/','/price/','/terms-of-service/','/contact/','/privacy-policy/')
  foreach ($path in $paths) {
    $status = curl.exe -s -o NUL -w '%{http_code}' "http://127.0.0.1:8765$path"
    if ($status -ne '200') { throw "$path returned $status" }
    "$status $path"
  }
} finally {
  Stop-Process -Id $server.Id -Force
}
```

Expected: nine `200` lines.

- [ ] **Step 5: Inspect the final diff and whitespace**

Run:

```powershell
git diff --check
git diff -- index.html contact/index.html services/leaf/index.html services/fitness/index.html services/fitness/night/index.html services/fitness/seed/index.html price/index.html privacy-policy/index.html terms-of-service/index.html
```

Expected: no whitespace errors; only approved metadata, parking blocks, Leaf routing, and nine footer lines.

### Task 7: Commit and Push the Site Changes to Staging

**Files:**
- Add individually: active task and nine target HTML files

- [ ] **Step 1: Stage only explicit paths**

Run:

```powershell
git add -- tasks/_active/task-063-bellmfit-seo-quick-wins.md
git add -- index.html
git add -- contact/index.html
git add -- services/leaf/index.html
git add -- services/fitness/index.html
git add -- services/fitness/night/index.html
git add -- services/fitness/seed/index.html
git add -- price/index.html
git add -- privacy-policy/index.html
git add -- terms-of-service/index.html
git diff --cached --name-status
```

Expected: exactly the active task plus nine HTML files. No untracked duplicate paths.

- [ ] **Step 2: Commit the implementation**

Run:

```powershell
git diff --cached --check
git commit -m "seo: add bellmfit quick wins and parking guidance"
```

Expected: commit succeeds with only approved paths.

- [ ] **Step 3: Push only the staging branch**

Run:

```powershell
git push origin staging
```

Expected: `staging -> staging`. Do not push `main` and do not run `deploy.yml`.

- [ ] **Step 4: Wait for `deploy-staging.yml`**

Run:

```powershell
gh run list --workflow deploy-staging.yml --branch staging --limit 1
gh run watch (gh run list --workflow deploy-staging.yml --branch staging --limit 1 --json databaseId --jq '.[0].databaseId') --exit-status
```

Expected: the staging deployment completes successfully.

### Task 8: Enforce the Staging Indexing Safety Gate and Verify the Deployment

**Files:**
- Verify: `https://bellmfit.com/test/` and eight subpaths
- Create: `reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/*.png`

- [ ] **Step 1: Check the real response header before any further staging inspection**

Run:

```powershell
$headers = curl.exe -sI https://bellmfit.com/test/
$headers
$robots = $headers | Select-String -Pattern '^X-Robots-Tag:\s*noindex,\s*nofollow\s*$' -CaseSensitive:$false
if (-not $robots) { throw 'SAFETY STOP: X-Robots-Tag: noindex, nofollow is missing.' }
```

Expected: an actual response header line `X-Robots-Tag: noindex, nofollow`.

**Stop condition:** If the header is absent or differs, report immediately and perform no additional staging page checks or screenshots.

- [ ] **Step 2: Verify all nine staging URLs return 200**

Run:

```powershell
$paths = @('/test/','/test/services/fitness/','/test/services/fitness/night/','/test/services/fitness/seed/','/test/services/leaf/','/test/price/','/test/terms-of-service/','/test/contact/','/test/privacy-policy/')
foreach ($path in $paths) {
  $status = curl.exe -s -o NUL -w '%{http_code}' "https://bellmfit.com$path"
  if ($status -ne '200') { throw "$path returned $status" }
  "$status $path"
}
```

Expected: nine `200` lines.

- [ ] **Step 3: Verify served metadata, exact NAP text, and production canonicals**

Run:

```powershell
$expectedNap = '駐車場10台・無料（施設向かい2台／近隣提携8台）'
$pages = [ordered]@{
  'https://bellmfit.com/test/'='https://bellmfit.com/'
  'https://bellmfit.com/test/services/fitness/'='https://bellmfit.com/services/fitness/'
  'https://bellmfit.com/test/services/fitness/night/'='https://bellmfit.com/services/fitness/night/'
  'https://bellmfit.com/test/services/fitness/seed/'='https://bellmfit.com/services/fitness/seed/'
  'https://bellmfit.com/test/services/leaf/'='https://bellmfit.com/services/leaf/'
  'https://bellmfit.com/test/price/'='https://bellmfit.com/price/'
  'https://bellmfit.com/test/terms-of-service/'='https://bellmfit.com/terms-of-service/'
  'https://bellmfit.com/test/contact/'='https://bellmfit.com/contact/'
  'https://bellmfit.com/test/privacy-policy/'='https://bellmfit.com/privacy-policy/'
}
foreach ($pair in $pages.GetEnumerator()) {
  $html = curl.exe -sL $pair.Key
  if (([regex]::Matches($html, [regex]::Escape($expectedNap))).Count -ne 1) { throw "NAP mismatch: $($pair.Key)" }
  $canonical = '<link rel="canonical" href="' + $pair.Value + '" />'
  if (([regex]::Matches($html, [regex]::Escape($canonical))).Count -ne 1) { throw "canonical mismatch: $($pair.Key)" }
}
$top = curl.exe -sL 'https://bellmfit.com/test/'
$leaf = curl.exe -sL 'https://bellmfit.com/test/services/leaf/'
if ($top -notmatch [regex]::Escape('<title>町田のジム べるフィット｜メディカルフィットネス・駐車場無料</title>')) { throw 'served top title mismatch' }
if ($top -notmatch [regex]::Escape('町田市木曽東のメディカルフィットネス。健康運動指導士や鍼灸マッサージ師などの専門職が無理のない運動をご案内。平日夜間・週末のナイト、女性向けのシード、介護保険で通えるリーフの3つの通い方。駐車場10台・無料。見学・体験を受け付けています。')) { throw 'served top description mismatch' }
if ($leaf -notmatch [regex]::Escape('べるフィットのリーフは、介護保険の総合事業で通える「保険が使えるジム」です。現在は多くの時間帯が満員で、空きは限られています（最新の空き状況をページに掲載）。自費で通えるシード（女性向け）・ナイト（夜間・週末）もご案内しています。')) { throw 'served leaf description mismatch' }
'PASS: served metadata, exact NAP, and production canonicals'
```

Expected: `PASS: served metadata, exact NAP, and production canonicals`.

- [ ] **Step 4: Capture desktop and mobile viewport screenshots**

Run:

```powershell
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$out = Join-Path (Get-Location) 'reports\screenshots\2026-08-02-bellmfit-seo-quick-wins'
New-Item -ItemType Directory -Path $out -Force | Out-Null
$shots = @(
  @{Name='top'; Url='https://bellmfit.com/test/'},
  @{Name='contact'; Url='https://bellmfit.com/test/contact/'},
  @{Name='leaf'; Url='https://bellmfit.com/test/services/leaf/'}
)
foreach ($shot in $shots) {
  & $chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1400 "--screenshot=$($out)\$($shot.Name)-desktop.png" $shot.Url
  & $chrome --headless=new --disable-gpu --hide-scrollbars --window-size=390,1200 "--screenshot=$($out)\$($shot.Name)-mobile.png" $shot.Url
}
Get-ChildItem -LiteralPath $out -Filter '*.png' | Select-Object Name,Length
```

Expected: six non-empty PNG files. Inspect each image; homepage and contact show the parking block, Leaf shows the full-capacity routing block, and no viewport shows overlap or clipping.

### Task 9: Write the Report, Complete the Task, and Push Documentation

**Files:**
- Create: `reports/2026-08-02-bellmfit-seo-quick-wins.md`
- Move: `tasks/_active/task-063-bellmfit-seo-quick-wins.md` → `tasks/_completed/task-063-bellmfit-seo-quick-wins.md`
- Create outside repository: `.ai-common/handoffs/codex-to-claude/active/2026-08-02-bellmfit-seo-quick-wins-result.md`

- [ ] **Step 1: Write the repository report**

The report must include these exact sections:

```markdown
# bellmfit.com 第1.5段階 SEO quick wins 実装報告

## 結論
## 変更差分の要約
## 変更後のtitle・description
## 駐車場ブロックの位置
## フッターNAP統一結果
## ローカル検証
## ステージング検証
## X-Robots-Tag実測
## canonical維持確認
## トップ画像合計容量
## 表示スクリーンショット
## Git・公開状態
## Claude Codeへのfact-check依頼
```

Record the exact strings, measured bytes, nine local and staging statuses, response header, commit IDs, workflow result, and screenshot links. State explicitly: `main` was not changed, `deploy.yml` was not run, and production was not published.

- [ ] **Step 2: Move the active task to completed**

Run:

```powershell
git mv -- tasks/_active/task-063-bellmfit-seo-quick-wins.md tasks/_completed/task-063-bellmfit-seo-quick-wins.md
```

Expected: one rename in Git status.

- [ ] **Step 3: Create the Codex-to-Claude handoff**

Write a concise result handoff containing: implementation commit, staging URL, header result, canonical result, NAP result, screenshot/report paths, and the requested fact-check items (parking count/fee, qualifications, service names, advertising-law wording). Do not copy P3 information.

- [ ] **Step 4: Stage documentation with individual paths and commit**

Run:

```powershell
git add -- reports/2026-08-02-bellmfit-seo-quick-wins.md
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/top-desktop.png
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/top-mobile.png
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/contact-desktop.png
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/contact-mobile.png
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/leaf-desktop.png
git add -- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/leaf-mobile.png
git add -- tasks/_completed/task-063-bellmfit-seo-quick-wins.md
git add -u -- tasks/_active/task-063-bellmfit-seo-quick-wins.md
git diff --cached --name-status
git commit -m "docs: record bellmfit quick wins verification"
git push origin staging
```

Expected: report, six screenshots, and task state only; `staging -> staging`; no `main` push. A docs-only staging workflow may run, but `.github/workflows/deploy-staging.yml` excludes `docs/`, `reports/`, `tasks/`, and `*.md` from FTP.

- [ ] **Step 5: Final safety and cleanliness check**

Run:

```powershell
git status --short --branch
git log -4 --oneline
git rev-parse origin/main
git rev-parse main
gh run list --workflow deploy.yml --limit 3
```

Expected: clean `staging`; `main` still at its original commit; no production deployment caused by this task; all required local/staging evidence recorded.
