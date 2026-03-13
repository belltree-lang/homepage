# Task 027 – Card System

## Goal
カードUIを再利用可能な共通パターンとして整理する

## Scope
変更可能ファイル
- styles.css
- index.html
- design-system.md

## Changes
具体的変更
- 実績、事業、補助情報などのカード表現を共通化する
- 背景、境界線、角丸、影、内側余白を標準化する
- カード派生パターンの違いを最小限に抑える

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 見た目の違いごとに無制限に派生クラスを増やさない

## Acceptance Criteria
完了条件
- 共通カード基盤が存在する
- 既存カード群の重複スタイルが削減されている
- デザインシステムと実装が一致している

## Dependencies
依存タスク
- Task 002 – Design Token Freeze
- Task 021 – Section Contrast

## Parallel Safety
衝突しない範囲
- カード共通化は全体CSSに影響するため、他のコンポーネント整理と競合しやすい

