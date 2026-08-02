# bellmfit.com 第1.5段階 SEO quick wins 設計

作成日: 2026-08-02

## 目的

bellmfit.com の既存9ページに限定し、検索結果の表現、駐車場情報、リーフ満員時の代替導線を改善する。本番サイトは公開せず、`staging` ブランチの `/test/` 環境で表示・リンク・画像を検証する。

## 前提

- 作業ブランチは `staging` とする。
- 実装前に `staging` を `origin/main` の最新へ早送りする。
- 2026-08-02の着手時点で、`staging` は独自コミットなしで `origin/main` より26コミット遅れていたため、専用worktreeで `f8f1e38` へ早送り済み。
- 元のリポジトリにある未追跡の `about/`、`solutions/`、`team/` 等には触れない。
- `git add .` と `git add -A` は使わず、追加対象を個別パスで指定する。

## 対象ページ

`sitemap.xml` に掲載されている次の9ページだけを対象とする。

1. `index.html`
2. `services/fitness/index.html`
3. `services/fitness/night/index.html`
4. `services/fitness/seed/index.html`
5. `services/leaf/index.html`
6. `price/index.html`
7. `terms-of-service/index.html`
8. `contact/index.html`
9. `privacy-policy/index.html`

## 実装内容

### トップページ

- `<title>` を代表確認済み文言へ置換する。
- meta description を代表確認済み文言へ置換する。
- 既存アクセス節の地図付近へ、住所・アクセス情報の流れを保ったまま駐車場案内を追加する。
- 既存フッターのNAPへ駐車場行を1行追加する。

### お問い合わせページ

- 既存デザインとユーティリティを使い、住所、アクセス、営業時間、Googleマップ、駐車場をまとめたアクセスブロックを追加する。
- 既存フッターのNAPへ駐車場行を1行追加する。
- 電話番号とフォーム動作は変更しない。

### リーフページ

- meta description を代表確認済み文言へ置換する。
- 空き状況表自体は変更せず、その直下へ「ご希望の時間帯が満員の場合」の案内を置く。
- シードとナイトへの相対リンクを設け、見学・体験へつなぐ。
- 既存フッターのNAPへ駐車場行を1行追加する。

### 残り6ページ

- 各ページ固有のフッター構造を維持したまま、NAPへ駐車場行を1行だけ追加する。
- `privacy-policy` と `terms-of-service` は他ページのフッター構造へ寄せない。

## NAP統一条件

9ページのフッターへ入れる駐車場行は、次の文字列とバイト単位で一致させる。

```text
駐車場10台・無料（施設向かい2台／近隣提携8台）
```

提携先の建物名は記載しない。電話番号は本社 `042-682-2839` のままとする。

## 変更しないもの

- `main` ブランチ
- `internal/belltree-home/`
- `styles.css` の共通部
- リーフの空き状況表とデータ取得処理
- 電話番号
- 未参照画像原本の整理
- 未追跡の別サイト複製
- 本番用 `.github/workflows/deploy.yml` の起動

## 検証

### ローカル

- 静的HTTPサーバーで9URLを開き、すべて正常表示されることを確認する。
- 9ページのローカルHTTP応答が200であることを確認する。
- 内部HTMLリンク、画像、CSS、JSの参照切れがないことを確認する。
- 9フッターの駐車場文字列が完全一致し、各ページに1回だけ存在することを機械確認する。
- 変更後のtitleとdescriptionが指定文言と完全一致することを確認する。
- トップが読み込む画像の合計容量を再計測し、基準約1.15MBから悪化していないことを確認する。
- トップ、contact、leafをデスクトップ幅とモバイル幅で目視し、重なり、はみ出し、リンク不良がないことを確認する。

### ステージング

- 実装コミットを `staging` へpushし、`deploy-staging.yml` の完了を確認する。
- `https://bellmfit.com/test/` 配下の9URL、内部リンク、画像を確認する。
- トップ、contact、leafの表示スクリーンショットを保存する。
- `main` へpushせず、`deploy.yml` を起動しない。
- 9ページの canonical は本番URLのまま維持し、`/test/` へ書き換えない。
- 配信後、ページ確認より先に `https://bellmfit.com/test/` の実レスポンスヘッダーを測定する。
- `X-Robots-Tag: noindex, nofollow` が無い場合は、重複公開防止の条件を満たさないため、その時点で作業を停止して報告する。

## 報告内容

- 変更差分の要約
- 変更後のトップtitleとdescriptionの実物
- 変更後のリーフdescriptionの実物
- 駐車場ブロックを追加した位置
- 9ページのフッターNAP統一結果
- ローカル・ステージング検証結果
- トップ画像合計容量
- トップ、contact、leafの表示スクリーンショット
- コミットIDと `staging` のpush結果
- `main` 未変更、`deploy.yml` 未起動の明記

## 完了後の流れ

Codex側はステージング検証と報告までで完了とする。公開前のfact-check、代表の目視確認、本番用 `deploy.yml` の手動起動はClaude Code・代表側で行う。
