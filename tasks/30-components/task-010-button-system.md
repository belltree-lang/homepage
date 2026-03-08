# Task 010 – Button System

## Goal
CTAボタンの見た目と状態管理を統一する

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- primary と secondary のボタン役割を定義する
- hover、focus、disabled 相当の見た目を整理する
- 既存リンクCTAをボタンパターンへ統一する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- ボタン用途でない要素に不要なボタン装飾を適用しない

## Acceptance Criteria
完了条件
- CTAの優先順位が視覚的に分かる
- キーボード操作時のフォーカスが明確である
- ボタンスタイルが共通化されている

## Dependencies
依存タスク
- Task 002 – Design Token Freeze

## Parallel Safety
衝突しない範囲
- ボタン関連クラスに限定すれば他セクション作業と並行可能

