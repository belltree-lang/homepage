# Task 010 – Trust Block System

## Goal
信頼補強のための情報ブロックを共通パターン化し、サイト全体で再利用できるようにする

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- 実績、提携先、会社情報などの信頼要素を整理する
- trust block の構造、見出し、補助文、数値表現ルールを定義する
- ページ下部やサービス詳細ページでも再利用できる構成にする

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- 信頼情報の見せ方が統一されている
- 数値、提携、補足説明の扱いが整理されている
- コンポーネントとして再利用可能である

## Dependencies
依存タスク
- task-003-component-catalog
- task-008-card-component-variants

## Parallel Safety
衝突しない範囲
- 信頼ブロック専用パターンに限定すれば他ページ作業と並行可能

