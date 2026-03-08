# Task 012 – Section Background Contrast

## Goal
各セクションの背景コントラストを整理し、情報の区切りを明確にする

## Scope
変更可能ファイル
- styles.css
- index.html

## Changes
具体的変更
- セクションごとの背景色や境界表現を見直す
- 連続するセクション間で視覚的な切れ目をつくる
- トークンベースで背景バリエーションを定義する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 色数を増やしすぎない

## Acceptance Criteria
完了条件
- 隣接セクションの境界が明確である
- テキストコントラストが十分である
- 背景表現がトークン経由で管理されている

## Dependencies
依存タスク
- Task 002 – Design Token Freeze

## Parallel Safety
衝突しない範囲
- セクション背景は全体影響が大きく、他の全体スタイル変更と競合しやすい

