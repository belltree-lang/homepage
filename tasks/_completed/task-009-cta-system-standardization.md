# Task 009 – CTA System Standardization

## Goal
CTAの種類と表現を標準化し、行動導線を一貫したルールで管理できるようにする

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- primary、secondary、text link などCTA種別を整理する
- セクションごとのCTA表現を統一する
- ボタンとリンクの使い分けルールを明確化する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- CTAの優先順位が視覚的に統一されている
- セクション間で表現ルールがぶれない
- design-systemと一致

## Dependencies
依存タスク
- task-002-design-token-freeze
- task-003-component-catalog

## Parallel Safety
衝突しない範囲
- CTAクラスと関連マークアップに限定すれば並行可能

