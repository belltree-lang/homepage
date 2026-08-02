# bellmfit.com seed／night ローカルSEO強化 設計

作成日: 2026-08-03

対象ブランチ: `staging`

状態: 代表承認済みの設計内容を書面化。実装着手前の設計書確認待ち。

## 目的

Search Consoleで131語中露出が無かった「女性専用 ジム 町田」「ジム 夜 町田」の検索意図に対し、新規記事ではなく既存のシード／ナイトページ本体を強化する。地域、利用時間、料金、駐車場を検索結果とページ上部で明確にし、事実に沿った構造化データを追加する。

Codex側の作業は、ローカル実装、`staging` へのpush、`https://bellmfit.com/test/` の検証と報告までとする。`main` は変更せず、本番用 `.github/workflows/deploy.yml` は起動しない。

## 着手時の状態

- 専用worktree `C:\Users\sss_1\dev\homepage-staging` を使用する。
- 2026-08-03の設計書作成前にfetchして確認し、`origin/staging` と `origin/main` はともに `7bd766b2b53458e716e8788d5b8b717d20081a7c` で一致していた。
- 元の作業場所にある未追跡の `solutions/`、`about/`、`team/` 等は別サイトの複製なので触れない。
- `git add .` と `git add -A` は使わず、追加対象を毎回個別パスで指定する。

## 参照順位

1. 最新の代表訂正と承認内容
2. `.company/marketing/2026-08-02-bellmfit-seed-night-強化-文言案.md`
3. `.ai-common/handoffs/claude-to-codex/active/2026-08-02-bellmfit-seed-night-local-seo.md`
4. `.company/shared/contacts-directory.md`
5. リポジトリの `price/index.html`

旧案の「受付時間 平日 9:00〜20:00（スタッフ在館）」は撤回済みであり、実装しない。電話受付の数字は変更せず、誤解を生む「営業時間」のラベルだけを直す。

## 採用する画面構成

比較した3案のうち、既存の要約カードへ必要情報を統合するB案を採用する。

- A案: 既存要約とは別に地域・料金カードを早い位置へ追加する。
- **B案（採用）: 既存の3カードを、地域／利用時間／料金／駐車場の4カードへ組み替える。**
- C案: 地域・料金情報をページ後半へ置く。

B案は、検索から直接来た利用者が最初の画面に続く位置で判断材料を確認でき、既存デザインのカードを再利用できる。`styles.css` は変更せず、既存の `grid` と `card` クラスでデスクトップ2列・モバイル縦並びにする。

### ヒーローと4カード

両ページとも、既存h1と既存導入文は維持する。既存導入文の直後に、確定済みの地域・利用時間の一節を追加する。その直後にある3カードを4カードへ変更する。

4カードの見出しと内容は次のとおり。

| カード | seed | night |
|---|---|---|
| 地域 | `東京都町田市木曽東4-9-14 Mビル2階` | `東京都町田市木曽東4-9-14 Mビル2階` |
| 利用時間 | `平日11:30〜13:30／16:30〜20:00` | `平日20:00〜翌9:00／週末24時間` |
| 料金 | `月6,800円（年契約・税込）／月7,480円（月契約・税込）。入会金16,500円。見学・体験は無料です。` | `月4,980円（税込）。入会金16,500円。見学・体験は無料です。` |
| 駐車場 | `10台・無料（施設向かい2台／近隣提携8台）` | `10台・無料（施設向かい2台／近隣提携8台）` |

カードの料金の後に、既存の `/price/` 詳細リンクを残す。実装直前にも `price/index.html` の6,800円、7,480円、4,980円、16,500円、見学・体験無料を再照合し、1つでも不一致なら料金を実装せず差し戻す。

### 「申込の流れ」の移設

既存の次のカードは削除しない。

```text
申込の流れ｜お問い合わせ → 見学・体験 → お手続き
```

seed／nightとも、現在の上部3カードから外し、`section#trial-form` 内の見学・体験フォームカードの直前へ移す。フォームへ進む直前に「いきなり入会ではない」ことを伝える安心材料として機能させる。文言は変更しない。

### 駐車場ブロック

seed／nightとも、本文の主要説明が終わった後、既存の「べるフィットの通い方」ナビゲーションの直前に、既存のコンテナ／カード表現を使って次の独立ブロックを置く。

```text
お車でお越しの方へ
施設の向かいに2台、近隣の提携駐車場に8台、あわせて10台分をご用意しています。いずれも無料でご利用いただけます。
```

提携先の建物名は記載しない。上部カードは即時判断用の要約、独立ブロックは内訳を文章で説明する役割とする。

## 確定文言

### title

seed:

```text
町田のジム べるフィット シード｜女性専用の時間帯・仕事帰りにも・駐車場無料
```

night:

```text
町田のジム べるフィット ナイト｜週末24時間・平日20時〜・駐車場無料
```

### meta description

seed:

```text
町田市木曽東のジム べるフィット シード。11:30〜13:30と16:30〜20:00は女性専用の時間帯です。周りの目を気にせず、仕事帰りにも通えます。専門職が体力に合わせて無理のない運動をご案内。月6,800円〜、見学・体験は無料。駐車場10台・無料。
```

night:

```text
町田市木曽東のジム べるフィット ナイト。平日は20:00〜翌9:00、週末は24時間ご利用いただけます。深夜も早朝も、自分の時間に合わせて。20時以降と週末はスタッフのいない自由利用の時間帯です。月4,980円、見学・体験は無料。駐車場10台・無料。
```

`og:title` と `og:description` も各ページの新しいtitleとdescriptionへ完全一致させる。canonicalは本番URLのまま変更しない。

### 既存導入文の直後へ足す本文

seed:

```text
べるフィットは、町田市木曽東のメディカルフィットネスです。
11:30〜13:30と16:30〜20:00は女性専用の時間帯で、男性の会員様はご利用になりません。
```

night:

```text
べるフィットは、町田市木曽東のメディカルフィットネスです。
ナイトは平日20:00〜翌9:00、週末は24時間ご利用いただける通い方です。
20時以降と週末はスタッフのいない自由利用の時間帯で、QRコードで入館していただきます。
```

## 電話受付ラベルの修正10件・維持3件

判定の物差しは「営業時間」という語を使っているかどうかとする。「営業時間」は施設の利用時間に読めるため「電話受付」へ変える。「お電話でのご相談」や個人情報保護窓口の「受付時間」のように、電話・窓口の文脈が明確なものは触らない。

### 修正する10件

9ページのフッター9件は、HTMLタグを除いた表示文字列がすべて次と完全一致するようにする。

```text
TEL 042-682-2839 ／電話受付 平日 9:00〜18:00
```

対象は次の9ページで、各ページ1件とする。

1. `index.html`
2. `services/fitness/index.html`
3. `services/fitness/night/index.html`
4. `services/fitness/seed/index.html`
5. `services/leaf/index.html`
6. `price/index.html`
7. `terms-of-service/index.html`
8. `contact/index.html`
9. `privacy-policy/index.html`

`contact/index.html` の「Access ／ アクセス・所在地」欄1件は、表示文字列を次にする。

```text
電話：042-682-2839／電話受付：平日 9:00〜18:00
```

既存HTMLの視覚上の空白はブラウザ表示で吸収されるため、ソースでは現在のタグ構造を維持しながら、ラベルだけを `営業時間：` から `電話受付：` へ置換する。

### 現状維持する3件

次の3件はバイト単位で変更しない。

1. `index.html` ヒーロー下の `平日 9:00〜18:00`（電話アイコンと電話番号に隣接し、営業時間ラベルなし）
2. `contact/index.html` の `お電話でのご相談：042-682-2839` と `（平日 9:00〜18:00）`
3. `privacy-policy/index.html` の個人情報保護窓口 `受付時間：9:00〜18:00`

機械確認では、対象9フッターの `営業時間 平日 9:00〜18:00` が0件、新しい `電話受付 平日 9:00〜18:00` が9件、contactアクセス欄の `営業時間：平日 9:00〜18:00` が0件、`電話受付：平日 9:00〜18:00` が1件であることを確認する。さらに、上記3件の実装前後のバイト列が一致することを確認する。

電話番号 `042-682-2839` と数字 `9:00〜18:00` は変更しない。施設の利用時間は共通フッターへ入れず、seed／night／leafの本文と構造化データで管理する。

## 構造化データ

### トップページ

既存の `@graph` 内にある `"@type": ["LocalBusiness", "ExerciseGym"]` と `"@id": "https://bellmfit.com/#organization"` を維持し、ExerciseGymを重複追加しない。既存ブロックへ次を追加・更新する。

`amenityFeature`:

```json
{
  "@type": "LocationFeatureSpecification",
  "name": "駐車場10台・無料（施設向かい2台／近隣提携8台）",
  "value": true
}
```

`openingHoursSpecification`:

```json
[
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "09:00"
  },
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Saturday", "Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  }
]
```

平日の `closes: 09:00` は翌日9時を示す意図で、電話受付ではなく施設全体でいずれかのプランが利用できる時間を表す。住所、電話、`@type`、`@id`、既存の親組織等は変更しない。

### seed Service

既存BreadcrumbListを残し、別のJSON-LDブロックとして次の内容を追加する。

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://bellmfit.com/services/fitness/seed/#service",
  "name": "べるフィット シード",
  "url": "https://bellmfit.com/services/fitness/seed/",
  "provider": {"@id": "https://bellmfit.com/#organization"},
  "audience": {"@type": "PeopleAudience", "suggestedGender": "Female"},
  "hoursAvailable": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "11:30",
      "closes": "13:30"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "16:30",
      "closes": "20:00"
    }
  ]
}
```

### night Service

既存BreadcrumbListを残し、別のJSON-LDブロックとして次の内容を追加する。

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "https://bellmfit.com/services/fitness/night/#service",
  "name": "べるフィット ナイト",
  "url": "https://bellmfit.com/services/fitness/night/",
  "provider": {"@id": "https://bellmfit.com/#organization"},
  "hoursAvailable": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "20:00",
      "closes": "09:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday", "Sunday"],
      "opens": "00:00",
      "closes": "23:59"
    }
  ]
}
```

### Rich Results Testの停止条件

ローカルでJSONを構文検証した後、Google Rich Results Testのコード貼り付け、またはステージングURLでトップ、seed、nightを確認する。

トップの `openingHoursSpecification` が結果画面で「24時間営業」「24 hours」「Open 24 hours」その他これと同義の単一営業時間として表示・正規化された場合は、その時点で構造化データの表現判断を停止し、表示結果のスクリーンショットと実測内容を報告して代表判断を仰ぐ。別の値への置換、営業時間プロパティの削除、電話受付時間への差し戻しは独断で行わない。

構文エラー、参照切れ、provider不一致、Seedのaudience欠落、各Serviceの時間帯不一致も合格とはしない。

## 変更対象

- `index.html`: ExerciseGymの駐車場・利用可能時間、フッター電話受付ラベル
- `services/fitness/seed/index.html`: SEO、OGP、本文、4カード、料金・駐車場、申込の流れ移設、Service、フッター
- `services/fitness/night/index.html`: SEO、OGP、本文、4カード、料金・駐車場、申込の流れ移設、Service、フッター
- `services/fitness/index.html`: フッター電話受付ラベルのみ
- `services/leaf/index.html`: フッター電話受付ラベルのみ
- `price/index.html`: フッター電話受付ラベルのみ
- `terms-of-service/index.html`: 現状のフッター構造内でラベルのみ
- `contact/index.html`: フッターとアクセス欄のラベルのみ。197行付近の相談案内は維持
- `privacy-policy/index.html`: 現状のフッター構造内でラベルのみ。個人情報保護窓口は維持

## 変更しないもの

- `main` ブランチと本番サイト
- `.github/workflows/deploy.yml` の内容と手動起動
- canonicalの本番URL
- seed／nightのh1
- 電話番号 `042-682-2839`
- `privacy-policy` の個人情報保護窓口の受付時間
- `contact` の「お電話でのご相談」表記
- `index.html` ヒーロー下の電話隣接時間
- `styles.css`
- `internal/belltree-home/`
- 未追跡の別サイト複製
- 記事・新規ページ
- 防犯カメラ、緊急通報ボタン、効果改善等の未承認主張
- 「町田の24時間ジム」「女性専用ジム」という施設全体を誤認させる表現

## 検証

### ローカル

- 実装前に `/price/` と料金を再照合する。
- 対象9URLがすべてHTTP 200で表示されることを確認する。
- 内部HTMLリンク、CSS、JS、画像の参照切れが0件であることを確認する。
- seed／nightのtitle、description、OGPが本設計の文言と完全一致することを確認する。
- h1、canonical、電話番号が変更されていないことを確認する。
- 4カード、地域の一節、駐車場ブロック、フォーム直前へ移した申込の流れをデスクトップ幅とモバイル幅で確認する。
- 9フッター＋contactアクセス欄の修正10件と、維持3件を機械確認する。
- 全JSON-LDをJSONとして解析し、トップのExerciseGymが1件だけであること、seed／nightのServiceとprovider、Seedのaudience、各時間帯を確認する。
- Rich Results Testでトップ、seed、nightを確認し、表示結果を保存する。

### ステージング

- 実装コミットを `staging` へpushし、`deploy-staging.yml` の完了を確認する。
- ページを開く前に `https://bellmfit.com/test/` の実レスポンスヘッダーを測定する。
- `X-Robots-Tag: noindex, nofollow` が無い場合は、その場で停止して報告し、以後のページ確認を行わない。
- ヘッダー合格後、`/test/` 配下の9URL、内部リンク、画像、title、description、canonical、10件／3件の分類を実測する。
- seed／nightをデスクトップ幅とモバイル幅で撮影する。
- `main` へpushせず、`deploy.yml` を起動しない。

## 報告内容

- 変更差分の要約
- 変更後のseed／nightのtitleとdescriptionの実物
- 地域の一節、4カード、駐車場ブロック、申込の流れを入れた位置
- 電話受付ラベルの修正10件・維持3件の機械確認結果
- 構造化データの実装値とRich Results Testの表示結果
- ローカルとステージングの検証結果
- `/test/` の `X-Robots-Tag` 実測値
- seed／nightのデスクトップ・モバイル表示スクリーンショット
- コミットIDと `staging` のpush結果
- `main` 未変更、`deploy.yml` 未起動の明記

## 完了後の流れ

Codexはステージング検証と報告までで完了とする。その後、Claude Codeが料金、サービス名、駐車場、女性専用表現、時間帯、景表法をfact-checkし、代表がステージングを目視する。本番反映は別途承認後に行い、本案件では実施しない。効果は2026年11月にSearch Consoleで再計測する。
