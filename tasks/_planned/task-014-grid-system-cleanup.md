# Task 014 – Grid System Cleanup

## Goal
グリッドレイアウトの重複とばらつきを整理し、共通パターンへ統合する

## Scope
変更可能ファイル
- styles.css
- index.html

## Changes
具体的変更
- 既存のグリッド定義を棚卸しし、共通グリッドクラスへ統合する
- 列数、ギャップ、折り返しルールを整理する
- セクション固有の例外を最小限に抑える

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- グリッド定義の重複が減っている
- design-systemと一致
- CSS重複なし

## Dependencies
依存タスク
- task-008-card-component-variants

## Parallel Safety
衝突しない範囲
- 共通レイアウト層を触るため、他の全体CSS変更とは競合しやすい
