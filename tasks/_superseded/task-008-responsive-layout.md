# Task 008 – Responsive Layout

## Goal
主要セクションのレイアウトをレスポンシブ前提で安定化する

## Scope
変更可能ファイル
- styles.css
- index.html

## Changes
具体的変更
- セクション間のレイアウト崩れをモバイル、タブレット、デスクトップで確認して調整する
- グリッド列数、余白、折り返し条件を統一する
- 主要コンポーネントのレスポンシブ閾値を設計意図に沿って整理する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- ブレークポイントを無秩序に増やさない

## Acceptance Criteria
完了条件
- 主要セクションに横スクロールが発生しない
- 画面幅ごとの情報密度が適切である
- レスポンシブ調整が既存トークンと整合する

## Dependencies
依存タスク
- Task 002 – Design Token Freeze

## Parallel Safety
衝突しない範囲
- レイアウト調整は共通CSSに影響するため、他の全体CSS変更とは衝突しやすい

