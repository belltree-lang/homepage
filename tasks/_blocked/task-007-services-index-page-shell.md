# Task 007 – Services Index Page Shell

## Goal
サービス一覧ページのページシェルを定義し、ナビゲーション移行後の受け皿を用意する

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- `/services/` を想定したページシェルの構成を設計する
- サービス一覧、導入文、ページタイトル領域の基本ブロックを定義する
- 既存トップページから流用できるレイアウトパターンを整理する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- サービス一覧ページの基本構造が定義されている
- 既存デザインシステムと整合している
- 他ページへ転用可能なシェルになっている

## Dependencies
依存タスク
- task-004-page-shell-system
- task-005-navigation-architecture

## Parallel Safety
衝突しない範囲
- サービスページ用の構造定義に限定すれば他コンポーネント作業と並行可能

