# マーケティング室（べるつりー本体・Webサイトリポジトリ）

> **正本**: 組織・部署・ガバナンスは `C:\Users\sss_1\OneDrive\ドキュメント\.company\CLAUDE.md`。
> ブランドルール・媒体別トーン・5層レイヤー・3兄弟ゲート・コピー執筆ロジックは HDマーケ室 `C:\Users\sss_1\OneDrive\ドキュメント\.company\marketing\CLAUDE.md`（＋ `references/copy-principles.md`）が正本。
> このファイルは**当リポジトリ＝本体Webサイトのソースを直接編集する立場**に固有の運用のみを記す（2026-07-02 ポインタ化）。

## このリポジトリの前提

- このリポジトリ = 株式会社べるつりーのコーポレートサイト本体（`index.html`, `about/`, `cases/`, `community/`, `family/`, `model/`, `news/`, `contact/` 等）
- マーケ室はここのHTML/CSSを直接 Read → Edit する
- 編集前に必ず該当ファイルを Read してから Edit する
- 大きな構造変更は `notes/` で代表と合意してから実施
- 本番反映は代表がgit操作で行う（マーケ室は直接pushしない）

## Web編集時に読むファイル

| 作業 | 読むファイル |
|---|---|
| Webサイト編集全般 | 対象HTMLファイル＋リポ直下の `AI_RULES.md`・`ARCHITECTURE.md`・`design-system.md` |
| べるつりー執筆ルール | `C:\Users\sss_1\OneDrive\ドキュメント\べるつりー\.claude\rules\writing-style.md` |
| べるリーガルへの送客導線 | `C:\Users\sss_1\OneDrive\ドキュメント\行政書士\00_戦略整理\2026-04-08_べるリーガル_Web広告紹介導線設計書.md` |

## 出力先

Webサイトの実ファイル編集は直接 Edit で行い、編集内容のログを `.company/marketing/` に `YYYY-MM-DD-website-[内容].md` で残す。SNS・GBP等の下書きも同フォルダに保存。
