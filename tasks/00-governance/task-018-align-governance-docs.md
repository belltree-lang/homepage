# Task 018 – Align Governance Docs

## Goal
ガバナンス文書間の責務と記述のずれを解消する

## Scope
変更可能ファイル
- AGENTS.md
- AI_RULES.md
- ARCHITECTURE.md
- design-system.md
- PROJECT.md

## Changes
具体的変更
- 各文書の責務を再確認し、重複記述を削減する
- タイポグラフィ、レイアウト、トークン定義の矛盾を揃える
- 今後の更新先が明確になるよう参照関係を整理する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 実装と乖離した理想論だけを記載しない

## Acceptance Criteria
完了条件
- 文書間で同じ項目に矛盾がない
- 各ドキュメントの責務境界が明確である
- 実装と整合した記述になっている

## Dependencies
依存タスク
- Task 001 – Governance Authority Model
- Task 002 – Design Token Freeze

## Parallel Safety
衝突しない範囲
- ドキュメント専用作業のため、実装変更と並行可能

