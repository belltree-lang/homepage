# Bellmfit シード／ナイト ローカルSEO 検証報告

検証日: 2026-08-04
設計書: `docs/superpowers/specs/2026-08-03-bellmfit-seed-night-local-seo-design.md`
実装コミット: `31a0e1b`〜`c5f509f`（2026-08-03）＋検収時修正 `778e380`（2026-08-04）

## 結論

設計書の検証項目をすべて実施し、**合格**。`staging` へ配信済みで、`main` は未変更、本番用deployは起動していない。

**Rich Results Testの停止条件は発動しなかった。** トップの平日営業時間は結果画面で `opens T09:00 / closes T09:00` のまま表示され、「24時間営業」への正規化は起きていない。

検収時に逸脱を1件検出し、修正した（下記）。

## 検収時に見つけた逸脱と修正

実装コミット `31a0e1b` が、トップの平日 `openingHoursSpecification` に設計書の規定値（`opens 09:00 / closes 09:00` ＝翌朝9時までの連続利用）ではなく、全曜日 `00:00–23:59` を入れていた。`00:00–23:59` はGoogleが「24時間営業」に正規化する典型形で、「24時間ジムと名乗らない」決定（優良誤認回避）と衝突するため、正本である設計書の値へ戻した（コミット `778e380`、push・ステージング反映済み）。週末の `00:00–23:59` は設計どおり維持。

## 検証結果

### 機械確認（フッター・ラベル置換）

- 対象9ページの旧「営業時間 平日 9:00〜18:00」: **0件**（recruit/seed の「営業時間」1件は施設利用時間の正しい表記で、fact-check済みの対象外）
- 新「電話受付」: 9フッター各1回＋contactアクセス欄1回 = **計10件**
- 維持3件（トップ電話横・contact相談案内・privacy-policy窓口）: **すべて現存**
- canonical: 3ページとも本番URL（`/test/` なし）を維持

### JSON-LD構文検証（ローカル）

- トップ: `@graph` 1ブロック、構文OK。`LocalBusiness`+`ExerciseGym` 維持、`amenityFeature`（無料駐車場10台）あり
- seed: BreadcrumbList＋Service の2ブロック、構文OK。`audience: PeopleAudience（suggestedGender: Female）` あり、`hoursAvailable` = 平日 11:30–13:30／16:30–20:00
- night: BreadcrumbList＋Service の2ブロック、構文OK。`hoursAvailable` = 平日 20:00–翌9:00／週末 00:00–23:59
- 文言メモ: トップの `amenityFeature.name` は「無料駐車場（10台／施設向かい2台・近隣提携8台）」で、設計書例文「駐車場10台・無料（…）」と語順が異なるが事実は同一（許容）

### X-Robots-Tag 実測

トップ・seed・night の3URLとも `x-robots-tag: noindex, nofollow`（HTTP 200）。ステージングは検索に載らない状態を維持。

### Google Rich Results Test（2026-08-04 15:23〜15:28・URLテスト）

| ページ | 結果 | 共有リンク |
|---|---|---|
| トップ | 地域のお店やサービス: 有効1件（重大でない指摘=任意項目priceRange欠落のみ）／組織: 有効1件 | <https://search.google.com/test/rich-results/result?id=BfXttDRYG6fCJkheYy-Eug> |
| seed | パンくずリスト: 有効1件・問題なし | <https://search.google.com/test/rich-results/result?id=KQwsw7YGxm3ezCAGl3deVA> |
| night | パンくずリスト: 有効1件・問題なし | <https://search.google.com/test/rich-results/result?id=hQlMD1katKufHPesAzJpQw> |

- **停止条件**: 非発動。トップの平日時間は `opens T09:00 / closes T09:00`、週末は `T00:00 / T23:59` とそのまま表示され、「24時間営業」等への正規化表示はなかった
- 3件とも「URL は Google に登録できません／クロールに失敗」と出るが、これは `/test/` の noindex によるもので想定どおり（構造化データの解析自体は完了している）
- seed／night の Service 型はリッチリザルトUIの表示対象外のため結果画面に出ない（仕様どおり）

### 表示確認

- デスクトップ（1280px）: seed・night とも4カード（対象／利用できる時間／料金／駐車場）が2×2で表示、アイコン・「申込の流れ」・ヒーロー装飾とも正常。スクリーンショット: `screenshots-2026-08-04-seed-night/`
- モバイル: 実ブラウザ375px幅で seed・night とも `scrollWidth = clientWidth = 375`（横はみ出しゼロ）を実測確認。装飾画像2点がビューポート外へ伸びるのは overflow クリップ内の設計どおりの挙動
- 注記: 同梱のモバイルスクリーンショットはヘッドレスChrome撮影の既知アーティファクトで右端が欠けて見えるが、実ブラウザでは再現しない（上記実測のとおり）。スマホ実機での最終目視は代表確認時に

## 残作業（代表判断待ち）

1. 代表がステージング（<https://bellmfit.com/test/> の トップ・seed・night）とスマホ表示を目視確認
2. 問題なければ本番反映（`main` へのマージとデプロイ）。設計書の「`main` 未変更・本番deploy禁止」は代表承認まで継続
