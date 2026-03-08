# Task 026 – Governance Unification

## Goal
ガバナンス文書を一貫した運用ルールとして再統合する

## Scope
変更可能ファイル
- AGENTS.md
- AI_RULES.md
- ARCHITECTURE.md
- design-system.md
- DECISIONS.md
- PROJECT.md

## Changes
具体的変更
- 各文書の役割分担を統合観点で見直す
- 冗長な記述や重複ルールを削減する
- 更新フローと参照順を明文化する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 単一文書にすべてを押し込まず責務を保つ

## Acceptance Criteria
完了条件
- どのルールをどの文書で管理するかが明確である
- 重複ルールが減っている
- AI/人間双方が参照しやすい構成になっている

## Dependencies
依存タスク
- Task 018 – Align Governance Docs
- Task 025 – Structure Analysis

## Parallel Safety
衝突しない範囲
- ガバナンス文書専用作業のため、実装変更と並行可能

