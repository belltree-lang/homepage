# Task 029 – Task Template Standardization

## Goal
タスク定義フォーマットを標準化し、AIエージェントが一貫して扱える状態にする

## Scope
変更可能ファイル
- tasks/TASK_TEMPLATE.md
- tasks/*
- AGENTS.md

## Changes
具体的変更
- 必須項目を持つ標準テンプレートを確定する
- 既存タスクを新テンプレートに合わせて正規化する
- タスク作成時の命名規則と配置ルールを明文化する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- テンプレートだけ更新して運用ルールを未記述のままにしない

## Acceptance Criteria
完了条件
- 新規タスクが同じ構造で作成できる
- 番号、タイトル、配置規則が統一されている
- AGENTS.md に参照可能な運用ルールがある

## Dependencies
依存タスク
- Task 026 – Governance Unification

## Parallel Safety
衝突しない範囲
- タスク定義ファイル中心の作業のため、実装変更と並行可能

