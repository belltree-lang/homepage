#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belltree1102.com — ヘッダーナビ／フッターリンクの一括同期（手動実行）

このサイトは全ページがヘッダー・フッターを手書きで重複保持している。
ナビ項目を1つ増やすたびに20ページ以上を手で直すのを避けるため、
「ナビの正本は下の NAV_ITEMS」という形に寄せるためのスクリプト。

ページごとの階層の深さ（../ の数）は自動で計算する。
トップページだけは同一ページ内アンカー（#concerns 等）を使う。

使い方:
    python _scripts/sync_nav.py --dry-run   変更点を表示するだけ
    python _scripts/sync_nav.py             実際に書き換える

CI では動かない（GitHub Actions の公開対象から _scripts/ は除外済み）。
生成・更新した HTML をコミットすることで公開される。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- ナビの正本 -------------------------------------------------------------
# (ラベル, リンク先) — リンク先は「トップからの相対パス」で書く。
# '#' で始まるものはトップページ内のアンカー。
NAV_ITEMS = [
    ("ホーム", "#top"),
    ("お悩み別解決策", "#concerns"),
    ("サービス一覧", "#model"),
    ("改善事例", "#cases"),
    ("お知らせ", "news/index.html"),
    ("スタッフ紹介", "team/index.html"),
    ("会社概要", "about/index.html"),
]

# フッターの会社情報欄に足すリンク（欄の最後に入れる）
# 見出しは古いページが「企業情報」、トップと会社概要が「About」と揺れているので両方見る。
FOOTER_ADD = ("お知らせ", "news/index.html")
FOOTER_HEADINGS = ("企業情報", "About")

NAV_RE = re.compile(r'([ \t]*)<nav class="main-nav">.*?</nav>', re.S)
FOOTER_BLOCK_RE = re.compile(
    r"<h5>(?:" + "|".join(FOOTER_HEADINGS) + r")</h5>\s*<ul>(.*?)</ul>", re.S
)
LAST_LI_RE = re.compile(r"([ \t]*)<li>.*?</li>(?!.*<li>)", re.S)


def depth_prefix(path: Path) -> str:
    """belltree-home からの深さに応じた '../' の並びを返す。"""
    rel = path.relative_to(ROOT)
    # index.html → 0 / faq/index.html → 1 / services/home-visit/index.html → 2
    return "../" * (len(rel.parts) - 1)


def build_nav(prefix: str, is_top: bool) -> str:
    """そのページ用のナビHTMLを組み立てる（インデントは呼び出し側で付ける）。"""
    lines = []
    for label, href in NAV_ITEMS:
        if href.startswith("#"):
            # トップページ内のアンカー。下層ページからはトップへ戻ってから飛ぶ。
            target = href if is_top else f"{prefix}index.html{'' if href == '#top' else href}"
        else:
            target = f"{prefix}{href}"
        lines.append(f'<a href="{target}">{label}</a>')
    return lines


def sync_nav(text: str, prefix: str, is_top: bool) -> tuple[str, bool]:
    m = NAV_RE.search(text)
    if not m:
        return text, False
    indent = m.group(1)
    inner_indent = indent + "  "
    links = build_nav(prefix, is_top)
    block = (
        f"{indent}<nav class=\"main-nav\">\n"
        + "\n".join(f"{inner_indent}{a}" for a in links)
        + f"\n{indent}</nav>"
    )
    if m.group(0) == block:
        return text, False
    return text[: m.start()] + block + text[m.end():], True


def sync_footer(text: str, prefix: str) -> tuple[str, bool]:
    m = FOOTER_BLOCK_RE.search(text)
    if not m:
        return text, False
    block = m.group(1)
    label, href = FOOTER_ADD
    target = f"{prefix}{href}"
    if f'href="{target}"' in block:
        return text, False
    li = LAST_LI_RE.search(block)
    if not li:
        return text, False
    indent = li.group(1)
    new_block = block[: li.end()] + f'\n{indent}<li><a href="{target}">{label}</a></li>' + block[li.end():]
    return text[: m.start(1)] + new_block + text[m.end(1):], True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="書き換えず、対象と変更有無だけ表示")
    args = ap.parse_args()

    targets = sorted(
        p for p in ROOT.rglob("*.html")
        if not p.name.startswith("google")
    )

    changed_nav: list[str] = []
    changed_footer: list[str] = []
    skipped: list[str] = []

    for path in targets:
        text = path.read_text(encoding="utf-8")
        if 'class="main-nav"' not in text:
            skipped.append(str(path.relative_to(ROOT)))
            continue
        prefix = depth_prefix(path)
        is_top = path.parent == ROOT and path.name == "index.html"

        new_text, nav_hit = sync_nav(text, prefix, is_top)
        new_text, foot_hit = sync_footer(new_text, prefix)

        rel = str(path.relative_to(ROOT))
        if nav_hit:
            changed_nav.append(rel)
        if foot_hit:
            changed_footer.append(rel)
        if (nav_hit or foot_hit) and not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

    print(f"対象ページ: {len(targets) - len(skipped)} 件")
    print(f"ナビ更新  : {len(changed_nav)} 件")
    print(f"フッター  : {len(changed_footer)} 件")
    if skipped:
        print(f"ナビなしのため対象外: {', '.join(skipped)}")
    if args.dry_run:
        print("\n--dry-run のため書き込みはしていない")
    return 0


if __name__ == "__main__":
    sys.exit(main())
