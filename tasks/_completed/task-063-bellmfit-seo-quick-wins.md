# Task 063 – Bellmfit SEO Quick Wins

## Status

Completed on 2026-08-02. Staging verification passed; production was not deployed.

## Goal

既存9ページの検索結果表現、駐車場情報、リーフ満員時導線を改善し、ステージングで検証する。

## Scope

- index.html
- contact/index.html
- services/leaf/index.html
- services/fitness/index.html
- services/fitness/night/index.html
- services/fitness/seed/index.html
- price/index.html
- privacy-policy/index.html
- terms-of-service/index.html
- reports/2026-08-02-bellmfit-seo-quick-wins.md
- reports/screenshots/2026-08-02-bellmfit-seo-quick-wins/

## Constraints

- stagingのみへpushする
- deploy.ymlを起動しない
- canonicalを書き換えない
- footerの駐車場行は9ページで完全一致させる
- privacy-policyとterms-of-serviceのフッター構造を変えない
- git add . / git add -Aを使わない

## Acceptance Criteria

- [x] ローカル9URLが200で、内部リンク・画像切れがない
- [x] stagingのX-Robots-Tagがnoindex, nofollow
- [x] staging 9URLの表示・canonical・リンク・画像が正常
- [x] トップ画像合計容量が基準約1.15MBから悪化していない
- [x] トップ、contact、leafのスクリーンショットと報告がある

## Result

- 実装確認コミット: `98ab2d6`
- ステージング: <https://bellmfit.com/test/>
- 報告: `reports/2026-08-02-bellmfit-seo-quick-wins.md`

## Dependencies

- docs/superpowers/specs/2026-08-02-bellmfit-seo-quick-wins-design.md

## Parallel Safety

- 対象9HTMLとstagingブランチを専有した
