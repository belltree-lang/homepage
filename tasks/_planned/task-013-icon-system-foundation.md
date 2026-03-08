# Task 013 – Icon System Foundation

## Goal
アイコン利用の方針と最小セットを定義し、情報補助表現を統一する

## Scope
変更可能ファイル
- assets/icons/*
- styles.css
- index.html
- design-system.md

## Changes
具体的変更
- サービスや実績で使うアイコンの形状方針を決める
- サイズ、余白、色の利用ルールを定義する
- 最低限必要なアイコンセットを追加する

## Constraints
禁止事項
- framework追加禁止
- design token必須
- semantic HTML維持
- 装飾目的だけの過剰なアイコン追加をしない

## Acceptance Criteria
完了条件
- アイコンのサイズと色ルールが統一されている
- アイコン追加時の判断基準が文書化されている
- 既存UIに導入してもノイズにならない

## Dependencies
依存タスク
- Task 002 – Design Token Freeze

## Parallel Safety
衝突しない範囲
- アイコン資産と専用クラスに限定すれば並行可能

