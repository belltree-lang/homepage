# Task 013 – Icon System

## Goal
アイコンの利用方針と実装パターンを統一し、補助情報表現の一貫性を高める

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- アイコンを使うべき箇所と使わない箇所を整理する
- サイズ、色、余白、配置の共通ルールを定義する
- テキストとの組み合わせ方を標準化する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- アイコン利用ルールが一貫している
- design-systemと一致
- CSS重複なし

## Dependencies
依存タスク
- task-008-card-component-variants

## Parallel Safety
衝突しない範囲
- アイコン関連クラスと対象セクションに限定すれば並行可能

