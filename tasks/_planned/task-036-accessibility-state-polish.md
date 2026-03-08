# Task 036 – Accessibility State Polish

## Goal
ページ状態表示や補助属性を整え、静的サイトとしてのアクセシビリティ品質を高める

## Scope
変更可能ファイル
- index.html
- services/index.html
- services/fitness/index.html
- services/acupuncture/index.html
- services/home-care/index.html
- services/legal/index.html
- services/community/index.html
- about/index.html
- contact/index.html
- styles.css

## Changes
具体的変更
- 現在地ナビゲーションの状態を明示する
- 補助的なaria属性やリンク文言を整理する
- フォーカス状態と可読性の微調整を行う

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- aria属性を過剰追加しない

## Acceptance Criteria
完了条件
- 現在地が分かるナビゲーションになっている
- 主要導線の意味が明確である
- UI崩れなし

## Dependencies
依存タスク
- task-033-route-page-language-cleanup
- task-034-shared-component-visual-polish

## Parallel Safety
衝突しない範囲
- 複数ページと共有CSSにまたがるため、逐次実行が望ましい
