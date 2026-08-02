# Bellmfit SEO Quick Wins 実装・検証報告

## 結論

第1.5段階 quick wins を対象9ページへ実装し、`staging` へ配信した。`main` は変更せず、本番用 `deploy.yml` は起動していない。

ステージングの実レスポンスで `x-robots-tag: noindex, nofollow` を確認した後、9ページのHTTP 200、NAP完全一致、canonical維持、内部ページ・画像等の参照、デスクトップ／モバイル表示を確認し、すべて合格した。

- ステージング: <https://bellmfit.com/test/>
- 実装確認コミット: `98ab2d6`
- staging workflow: <https://github.com/belltree-lang/homepage/actions/runs/30739607069>

## 変更差分の要約

- トップのtitleとdescriptionを更新
- トップとお問い合わせページのアクセス節へ駐車場案内カードを追加
- 対象9ページのフッターへ完全一致の駐車場NAPを1回ずつ追加
- リーフのdescriptionを更新し、満員時にシード／ナイトを案内する導線を追加
- Leafの2リンクには既存の常時下線・ブランド色のリンク表現を適用
- HTML差分: 9ファイル、32行追加・3行削除
- CSS、電話番号、空き状況表・スクリプト、canonical、workflow、`internal/belltree-home/` は変更なし

## 変更後のtitle・description

### トップ

- title: `町田のジム べるフィット｜メディカルフィットネス・駐車場無料`
- description: `町田市木曽東のメディカルフィットネス。健康運動指導士や鍼灸マッサージ師などの専門職が無理のない運動をご案内。平日夜間・週末のナイト、女性向けのシード、介護保険で通えるリーフの3つの通い方。駐車場10台・無料。見学・体験を受け付けています。`

### リーフ

- title: `保険が使えるジム（リーフ）｜べるフィット | 株式会社べるつりー`（変更なし）
- description: `べるフィットのリーフは、介護保険の総合事業で通える「保険が使えるジム」です。現在は多くの時間帯が満員で、空きは限られています（最新の空き状況をページに掲載）。自費で通えるシード（女性向け）・ナイト（夜間・週末）もご案内しています。`

## 駐車場ブロックを入れた位置

- トップ `index.html`: 「アクセス」節の住所・営業時間の直後、地図の直前
- お問い合わせ `contact/index.html`: 「アクセス・所在地」節の住所・営業時間の直後、地図の直前
- 両カードの本文: `施設の向かいに2台、近隣の提携駐車場に8台、あわせて10台分をご用意しています。いずれも無料でご利用いただけます。`
- フッター: 対象9ページそれぞれの既存住所・電話・営業時間ブロック内

## フッターNAP統一結果

次の文字列が対象9ページにバイト単位で同一、かつ各1回だけ存在することを機械確認した。

`駐車場10台・無料（施設向かい2台／近隣提携8台）`

対象はトップ、運動施設、ナイト、シード、リーフ、料金、利用規約、お問い合わせ、個人情報保護方針。`privacy-policy` と `terms-of-service` は既存フッター構造を変えず、上記1行のみ追加した。

## ローカル検証

- 対象9URL: すべてHTTP 200
- 内部リンク・画像・CSS・JavaScript参照: 切れなし
- NAP: 9ページすべて完全一致、各1回
- metadata: 指定文言と完全一致
- canonical: 本番URLのまま
- `git diff --check`: 合格
- コードレビュー: Critical 0 / Important 0
- トップ画像合計: 1,181,983 bytes（1.13 MiB、22ファイル）。基準約1.15MBから悪化なし

## ステージング検証

- `/test/` 以下の対象9URL: すべてHTTP 200
- NAP: 配信HTMLでも9ページすべて完全一致、各1回
- metadata: トップtitle／description、Leaf descriptionが指定文言と完全一致
- Leaf導線: シード／ナイトのリンク先と常時下線表示を確認
- 内部ページ・画像等: 44件の`/test/` URLがすべてHTTP 400未満
- 表示: トップ、お問い合わせ、Leafをデスクトップ1440px／モバイル390pxで確認。重なり、横はみ出し、導線欠落なし

## X-Robots-Tag実測

2026-08-02、デプロイ完了直後に `https://bellmfit.com/test/` のレスポンスヘッダーを実測した。

```text
HTTP/1.1 200 OK
x-robots-tag: noindex, nofollow
```

指定の安全ゲートを通過してから、それ以降のステージング検証を実施した。

## canonical維持確認

9ページとも `/test/` へ書き換えず、本番URLを維持している。

- `https://bellmfit.com/`
- `https://bellmfit.com/services/fitness/`
- `https://bellmfit.com/services/fitness/night/`
- `https://bellmfit.com/services/fitness/seed/`
- `https://bellmfit.com/services/leaf/`
- `https://bellmfit.com/price/`
- `https://bellmfit.com/terms-of-service/`
- `https://bellmfit.com/contact/`
- `https://bellmfit.com/privacy-policy/`

## 表示スクリーンショット

### トップ

![トップ・デスクトップ](screenshots/2026-08-02-bellmfit-seo-quick-wins/top-desktop.png)

![トップ・モバイル](screenshots/2026-08-02-bellmfit-seo-quick-wins/top-mobile.png)

### お問い合わせ

![お問い合わせ・デスクトップ](screenshots/2026-08-02-bellmfit-seo-quick-wins/contact-desktop.png)

![お問い合わせ・モバイル](screenshots/2026-08-02-bellmfit-seo-quick-wins/contact-mobile.png)

### リーフ

![リーフ・デスクトップ](screenshots/2026-08-02-bellmfit-seo-quick-wins/leaf-desktop.png)

![リーフ・モバイル](screenshots/2026-08-02-bellmfit-seo-quick-wins/leaf-mobile.png)

## Git・公開状態

- `staging`: 実装コミット `98ab2d6` をpush済み
- `main`: `f8f1e38` のまま。pushなし
- 本番用 `.github/workflows/deploy.yml`: workflow_dispatchのみ。起動なし
- 公開範囲: `https://bellmfit.com/test/` のみ

## Claude Codeへのfact-check依頼

本番公開判断の前に、駐車場の台数・無料条件、資格表現、サービス名称、満員表現、広告・医療介護関連表現の事実確認を依頼する。本報告時点では本番公開していない。
