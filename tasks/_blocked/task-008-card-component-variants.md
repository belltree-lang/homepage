# Task 008 – Card Component Variants

## Goal
カードコンポーネントの派生パターンを定義し、用途ごとの差異を整理する

## Scope
変更可能ファイル
- styles.css
- index.html

## Changes
具体的変更
- 実績、事業、信頼情報などで使うカード派生を分類する
- 共通カード基盤と派生バリアントの責務を整理する
- 見出し、本文、補助要素の配置ルールを定義する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持

## Acceptance Criteria
完了条件
- カード派生の違いが明文化されている
- 共通部分と差分部分が分離されている
- CSS重複なし

## Dependencies
依存タスク
- task-003-component-catalog
- task-002-design-token-freeze

## Parallel Safety
衝突しない範囲
- カード系スタイルに限定すればページシェル作業と並行可能

