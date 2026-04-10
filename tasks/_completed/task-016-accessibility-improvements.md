# Task 016 – Accessibility Improvements

## Goal
静的サイトとしての基本アクセシビリティ品質を引き上げる

## Scope
変更可能ファイル
- index.html
- styles.css
- main.js

## Changes
具体的変更
- 見出し構造、ランドマーク、代替テキスト、aria属性の妥当性を確認して修正する
- キーボードフォーカスと色コントラストを改善する
- 動きのある表現に reduced motion 対応を追加する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- aria属性を過剰追加しない

## Acceptance Criteria
完了条件
- キーボード操作で主要導線に到達できる
- コントラストや見出し構造に重大な問題がない
- 動きを減らしたい利用者に配慮できている

## Dependencies
依存タスク
- Task 008 – Responsive Layout
- Task 009 – Readability Tuning

## Parallel Safety
衝突しない範囲
- HTML全体確認が必要なため、全体構造変更とは競合しやすい

