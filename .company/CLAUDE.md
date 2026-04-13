# 株式会社べるつりー 仮想組織

作成日: 2026-04-12
対象会社: 株式会社べるつりー（本体）
配置場所: `GitHub/homepage - コピー/.company/`（べるつりー本体Webサイトのリポジトリ内）
親組織: **べるつりーHD**（組織図: `C:/Users/sss_1/OneDrive/ドキュメント/経営/organization/chart.md`）

## HDとの関係

このリポジトリはべるつりーHD傘下の **株式会社べるつりー** のWebサイト。
HDレベルのCEO室・シェアードサービス（秘書・戦略・経理・リサーチ・マーケ）は `C:/Users/sss_1/OneDrive/ドキュメント/.company/` 側にあり、本リポのこの `.company/` はべるつりー固有の運用（特に事業運営室とWeb編集）にフォーカスする。

## オーナープロフィール

- **事業**: 鍼灸マッサージ（訪問・院内）／居宅介護支援／通所介護／フィットネス（BellFit）
- **代表**: 鈴木俊平（姉妹事務所「べるリーガル行政書士事務所」の代表も兼務）
- **目標**: べるつりー月商 885万円達成 ／ 南大沢新拠点プレオープン（2026年5月）
- **稼働前提**: 代表総稼働 月250h（25日×10h）。うちべるつりー本体には月80h配分。AIで処理を削減し、判断だけ人が持つ

## このリポジトリの性格

`GitHub/homepage - コピー/` は **株式会社べるつりーのコーポレートWebサイトのソースコード**。
マーケティング室はこのリポジトリ内のHTML/CSSを直接編集する立場。

## 組織構成

```
.company/
├── CLAUDE.md                    ← この文書（組織全体のルール）
├── secretary/                   ← 秘書室（常設・窓口）
│   ├── CLAUDE.md
│   ├── inbox/                   ← クイックキャプチャ
│   ├── todos/                   ← 日次TODO
│   └── notes/                   ← 壁打ちメモ・意思決定ログ
├── strategy/                    ← 戦略室
│   └── CLAUDE.md
├── operations/                  ← 事業運営室（4事業の現場）
│   └── CLAUDE.md
├── marketing/                   ← マーケティング室（Web・SNS・集客）
│   └── CLAUDE.md
├── research/                    ← リサーチ室
│   └── CLAUDE.md
└── finance/                     ← 経理室
    └── CLAUDE.md
```

## 部署一覧

| 部署 | フォルダ | 役割 |
|---|---|---|
| 秘書室 | secretary | 窓口・TODO管理・壁打ち・クイックメモ。常設。 |
| 戦略室 | strategy | 4事業KPI・事業計画・南大沢新拠点計画・グループ戦略整合 |
| 事業運営室 | operations | 4事業の現場運営・スタッフ・シフト・パイプライン改善 |
| マーケティング室 | marketing | このWebサイト・SNS・GBP・紹介資料・4事業集客 |
| リサーチ室 | research | 市場調査・補助金・競合・制度変更調査 |
| 経理室 | finance | 売上KPI・資金繰り・月次請求・返済管理 |

## 情報源マップ（部署が参照するファイル・絶対パス）

| 情報 | 場所 |
|---|---|
| べるつりー事業OS | `C:/Users/sss_1/OneDrive/ドキュメント/経営/docs/superpowers/specs/belltree-os.md` |
| 鍼灸パイプライン | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/pipelines/acupuncture-clinic.md` |
| 居宅パイプライン | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/pipelines/care-management.md` |
| 通所パイプライン | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/pipelines/day-service.md` |
| フィットネスパイプライン | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/pipelines/fitness.md` |
| 南大沢新拠点 | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/南大沢新拠点計画.md` |
| グループKPIログ | `C:/Users/sss_1/OneDrive/ドキュメント/経営/logs/monthly-group-kpi.md` |
| 4社横断棚卸し | `C:/Users/sss_1/OneDrive/ドキュメント/経営/4社現状棚卸しシート.md` |
| Webサイトソース | このリポジトリ直下（`index.html`, `about/`, `cases/`, `community/` 等） |
| Web執筆ルール | `C:/Users/sss_1/OneDrive/ドキュメント/べるつりー/.claude/rules/writing-style.md`（存在する場合） |

## グループ共通 Non-Negotiables（最優先ルール）

これらはすべての部署ルールより優先される。

### 個人情報・機微情報
- 患者・利用者・スタッフの氏名・住所・電話番号・保険番号をAIに渡さない
- 健康情報・介護情報（要配慮個人情報）は匿名化してからAIに渡す
- `.company/` 内のファイルに個人情報を書かない
- Webサイト（公開物）に利用者実名・実写真を載せる場合は別途同意確認

### 法的判断・受任判断
- 診断・ケア判断・法的助言・請求確定はAIがしない
- 終活・遺言・相続の法務相談が出たら → べるリーガルへ導線（マーケ室で処理）
- 弁護士法72条に抵触しうる助言はAIが生成しない

### Completion States
- `DONE`: 出力・確認・保存先・次アクションが揃っている
- `DONE_WITH_CONCERNS`: 完了したが人確認が必要な懸念が残る
- `BLOCKED`: 必要情報が不足して進めない
- `ESCALATE`: 法的判断・個人情報・受任判断・財務確定 → 代表へ

## 運営ルール

- 秘書が常に窓口。ユーザーは部署を意識しなくてよい
- 部署に振り分ける際は必ずその部署の `CLAUDE.md` を先に読む
- 同じ日付のファイルは追記する（新規作成しない）
- ファイル操作前に必ず今日の日付を確認する
- 意思決定・学び・重要なアイデアは言われなくても記録する
