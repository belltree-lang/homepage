# Task 012 – Footer System

## Goal
フッターを再利用可能なシステムとして整理し、全ページで一貫した末尾情報を提供できるようにする

## Scope
変更可能ファイル
- index.html
- styles.css

## Changes
具体的変更
- フッターの情報ブロック、導線、会社情報、補助リンクの構造を定義する
- フッター内の見出し、余白、区切り、階層を共通ルール化する
- 将来の下層ページでも流用できるフッターシステムへ整理する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- フッター構造が再利用可能な単位で整理されている
- design-systemと一致
- CSS重複なし

## Dependencies
依存タスク
- task-010-trust-block-system

## Parallel Safety
衝突しない範囲
- フッター関連のHTML/CSSに限定すれば他セクション作業と並行可能

