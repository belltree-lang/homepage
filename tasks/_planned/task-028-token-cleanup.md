# Task 028 – Token Cleanup

## Goal
CSS内のリテラル値を整理し、design token を唯一の基準に近づける

## Scope
変更可能ファイル
- styles.css
- design-system.md

## Changes
具体的変更
- 色、余白、半径、影などの直書き値を棚卸しする
- 既存トークンへ置換できるものを差し替える
- 足りないトークンがある場合のみ最小追加する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 無意味にトークン数を増やさない

## Acceptance Criteria
完了条件
- 不要なリテラル値が減っている
- トークンの責務が明確である
- design-system.md と styles.css の定義が揃っている

## Dependencies
依存タスク
- Task 002 – Design Token Freeze
- Task 027 – Card System

## Parallel Safety
衝突しない範囲
- 共通トークン層を触るため、全体CSS変更と競合しやすい

