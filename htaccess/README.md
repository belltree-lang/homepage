# `.htaccess` 切替ガイド

ルート `.htaccess` は本番に1本しか置けないため、ここに**フェーズ別バリアント**を保管している。
切り替えるときは、このディレクトリの該当ファイルの**中身をコピー**してルート `.htaccess` を上書きする（ファイル名 `.htaccess` のままにする）。

## ファイル一覧

| ファイル | 用途 | リダイレクト挙動 |
|---|---|---|
| `maintenance.htaccess` | **現フェーズ**：完全メンテナンスモード | 全アクセス → `maintenance.html`（302） |
| `maintenance-preview.htaccess` | **公開直前テスト**：preview抜け道つきメンテ | `?preview=true` 付きは素通し／なしは302／旧パスは301 |
| `production.htaccess` | **公開後**：301のみ | 旧パスは301／その他は通常表示 |

## 公開ライフサイクル

```
[現在] maintenance.htaccess
    ↓ 公開直前テストを始めるとき
[テスト] maintenance-preview.htaccess
    ↓ 公開当日
[公開] production.htaccess
```

## 切替手順

### 1. 現在 → 公開直前テスト

```bash
# ローカルで上書き
cp "htaccess/maintenance-preview.htaccess" ".htaccess"
# Lolipop へ FTP アップロード（ルートの .htaccess を差し替え）
```

確認：
- `https://bellmfit.com/?preview=true` → 通常ページ表示
- `https://bellmfit.com/` → メンテページ（302）
- `https://bellmfit.com/solutions/end-of-life-preparation/` → 301 で `/services/shukatsu/`

### 2. 公開直前テスト → 公開

```bash
cp "htaccess/production.htaccess" ".htaccess"
# Lolipop へ FTP アップロード
```

確認：
- `https://bellmfit.com/` → 通常ページ表示
- `https://bellmfit.com/?preview=true` → 通常ページ表示（preview抜け道は削除済み・特別な意味なし）
- `https://bellmfit.com/solutions/end-of-life-preparation/` → 301

### 3. 何かトラブル → メンテに戻す

```bash
cp "htaccess/maintenance.htaccess" ".htaccess"
# Lolipop へ FTP アップロード
```

## 注意

- ルート `.htaccess` の中身は常にこのディレクトリのいずれかと**同一**であること（drift防止）。手動で編集する場合はこのディレクトリ側にも反映する
- `lolipop_staging/.htaccess` は `scripts/build_staging.py` がルート `.htaccess` をミラーする想定（=現在のフェーズが反映される）
- 公開時の301は1件のみ（`/solutions/end-of-life-preparation/` → `/services/shukatsu/`）。他に必要な301が発見されたら `production.htaccess` と `maintenance-preview.htaccess` の両方に追記する

## 履歴

- 2026-04-28：旧 `-suzuki.htaccess`（ハイフン始まりの危険ファイル名）を解体し、内容を `maintenance-preview.htaccess` に統合。`htaccess/` ディレクトリ運用を開始
