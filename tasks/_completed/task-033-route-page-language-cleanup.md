# Task 033 – Route Page Language Cleanup

## Goal
下層ページの英語ラベルやプレースホルダ感のある表示を整理し、日本語サイトとしての一貫性を高める

## Scope
変更可能ファイル
- services/index.html
- services/fitness/index.html
- services/acupuncture/index.html
- services/home-care/index.html
- services/legal/index.html
- services/community/index.html
- about/index.html
- contact/index.html

## Changes
具体的変更
- 英語ラベルを日本語化する
- 露骨なプレースホルダ表示を避ける文言に整える
- ルートページ間の見出しと導線表現を統一する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 実在しない企業情報を新規に捏造しない

## Acceptance Criteria
完了条件
- 下層ページの言語トーンが統一されている
- プレースホルダ感の強い表示が減っている
- UI崩れなし

## Dependencies
依存タスク
- task-007-services-index-page-shell

## Parallel Safety
衝突しない範囲
- 下層ページHTMLに限定すればホームページ変更と並行可能

