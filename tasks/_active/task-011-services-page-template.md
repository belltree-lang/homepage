# Task 011 – Services Page Template

## Goal
サービス詳細ページへ展開できる共通テンプレートを定義する

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- サービスページ用のヒーロー、概要、詳細、CTA の基本構造を整理する
- 既存トップページの情報設計を流用できるテンプレート化ルールを定義する
- サービスごとの差し替え箇所と共通箇所を明確にする

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- サービス詳細ページの共通骨格が定義されている
- design-systemと一致
- 他サービスへ横展開できる

## Dependencies
依存タスク
- task-007-services-index-page-shell

## Parallel Safety
衝突しない範囲
- サービスページ構造の定義に限定すれば他コンポーネント作業と並行可能

