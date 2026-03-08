# Task 017 – SEO Improvements

## Goal
静的サイトとして最低限必要なSEO基盤を整備する

## Scope
変更可能ファイル
- index.html
- assets/images/*

## Changes
具体的変更
- title、description、og、canonical などのメタ情報を整える
- 見出し構造とページ要約の一貫性を確認する
- SNS共有時に必要な画像や補助設定を追加する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 実URLが未確定の場合は仮URLを勝手に固定しない

## Acceptance Criteria
完了条件
- head 内の主要SEOメタが整理されている
- OGP表示に必要な基本情報が揃っている
- 見出しとメタ文言が大きく矛盾しない

## Dependencies
依存タスク
- Task 016 – Accessibility Improvements

## Parallel Safety
衝突しない範囲
- head と共有画像中心の変更なら並行可能

