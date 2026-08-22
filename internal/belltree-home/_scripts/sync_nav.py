#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belltree1102.com — ヘッダーナビ／フッターリンクの一括同期（手動実行）

このサイトは全ページがヘッダー・フッターを手書きで重複保持している。
ナビ項目を1つ増やすたびに20ページ以上を手で直すのを避けるため、
「ナビの正本は下の NAV_ITEMS」という形に寄せるためのスクリプト。

ページごとの階層の深さ（../ の数）は自動で計算する。
トップページだけは同一ページ内アンカー（#concerns 等）を使う。
いま開いているページに当たるナビ項目には class="current" が付く
（見た目は colors_and_type.css の .main-nav a.current が持つ）。

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
# build_news.py もこの定義を import して使う（二重管理をしないため）。
NAV_ITEMS = [
    ("ホーム", "#top"),
    ("お悩み別解決策", "#concerns"),
    ("サービス一覧", "#model"),
    ("改善事例", "#cases"),
    ("お知らせ", "news/index.html"),
    ("スタッフ紹介", "team/index.html"),
    ("会社概要", "about/index.html"),
]

# そのページ自身を指すナビ項目のリンク先を、ページ内アンカーに差し替える。
# （会社概要ページは以前から #company へ飛ぶ作りだった。読み込み直しを避ける）
SELF_ANCHORS = {
    "about/index.html": "#company",
}

# フッターの会社情報欄に足すリンク（欄の最後に入れる）
# 見出しは古いページが「企業情報」、トップと会社概要が「About」と揺れているので両方見る。
FOOTER_ADD = ("お知らせ", "news/index.html")
FOOTER_HEADINGS = ("企業情報", "About")

NAV_MARK = 'class="main-nav"'
NAV_RE = re.compile(r'([ \t]*)<nav[^>]*class="main-nav"[^>]*>.*?</nav>', re.S)
FOOTER_BLOCK_RE = re.compile(
    r"<h5>(?:" + "|".join(FOOTER_HEADINGS) + r")</h5>\s*<ul>(.*?)</ul>", re.S
)
LAST_LI_RE = re.compile(r"([ \t]*)<li>.*?</li>(?!.*<li>)", re.S)


def page_key(path: Path) -> str:
    """belltree-home からの相対パスを 'about/index.html' 形式で返す。"""
    return path.relative_to(ROOT).as_posix()


def depth_prefix(rel: str) -> str:
    """ページの深さに応じた '../' の並びを返す。"""
    return "../" * rel.count("/")


def build_nav(rel: str) -> list[str]:
    """そのページ用のナビのリンク行を組み立てる（インデントは呼び出し側で付ける）。"""
    prefix = depth_prefix(rel)
    is_top = rel == "index.html"
    lines = []
    for label, href in NAV_ITEMS:
        if href.startswith("#"):
            # トップページ内のアンカー。下層ページからはトップへ戻ってから飛ぶ。
            target = href if is_top else f"{prefix}index.html{'' if href == '#top' else href}"
            current = False
        else:
            # そのファイル自身か、その下の階層にいるなら「現在地」
            section = href.rsplit("/", 1)[0] + "/"
            current = rel == href or rel.startswith(section)
            target = SELF_ANCHORS[href] if (current and href in SELF_ANCHORS) else f"{prefix}{href}"
        attrs = ' class="current" aria-current="page"' if current else ""
        lines.append(f'<a href="{target}"{attrs}>{label}</a>')
    return lines


def sync_nav(text: str, rel: str) -> tuple[str, bool]:
    m = NAV_RE.search(text)
    if not m:
        return text, False
    indent = m.group(1)
    inner_indent = indent + "  "
    links = build_nav(rel)
    block = (
        f"{indent}<nav class=\"main-nav\">\n"
        + "\n".join(f"{inner_indent}{a}" for a in links)
        + f"\n{indent}</nav>"
    )
    if m.group(0) == block:
        return text, False
    return text[: m.start()] + block + text[m.end():], True


def sync_footer(text: str, prefix: str) -> tuple[str, bool, str]:
    """フッターの企業情報欄に「お知らせ」を足す。戻り値の3つ目は見送り理由。"""
    m = FOOTER_BLOCK_RE.search(text)
    if not m:
        return text, False, "フッターにリンク欄（企業情報／About）がない"
    block = m.group(1)
    label, href = FOOTER_ADD
    target = f"{prefix}{href}"
    if f'href="{target}"' in block:
        return text, False, ""
    li = LAST_LI_RE.search(block)
    if not li:
        return text, False, "フッターのリンク欄に <li> が1つもない"
    indent = li.group(1)
    new_block = block[: li.end()] + f'\n{indent}<li><a href="{target}">{label}</a></li>' + block[li.end():]
    return text[: m.start(1)] + new_block + text[m.end(1):], True, ""


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
    no_nav: list[str] = []
    problems: list[str] = []

    for path in targets:
        text = path.read_text(encoding="utf-8")
        rel = page_key(path)
        if NAV_MARK not in text:
            no_nav.append(rel)
            continue
        new_text, nav_hit = sync_nav(text, rel)
        if not nav_hit and not NAV_RE.search(text):
            # class="main-nav" はあるのに <nav> の形が合わず素通りした＝取りこぼし
            problems.append(f"{rel}: ナビを書き換えられなかった（<nav class=\"main-nav\"> の形が想定と違う）")
            continue

        new_text, foot_hit, foot_why = sync_footer(new_text, depth_prefix(rel))
        if foot_why:
            problems.append(f"{rel}: フッター未更新 — {foot_why}")

        if nav_hit:
            changed_nav.append(rel)
        if foot_hit:
            changed_footer.append(rel)
        if (nav_hit or foot_hit) and not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

    print(f"対象ページ: {len(targets) - len(no_nav)} 件")
    print(f"ナビ更新  : {len(changed_nav)} 件")
    print(f"フッター  : {len(changed_footer)} 件")
    if no_nav:
        print(f"ナビなしのため対象外: {', '.join(no_nav)}")
    if problems:
        print("\n【要確認】手で見たほうがよいページ")
        for p in problems:
            print(f"  - {p}")
    if args.dry_run:
        print("\n--dry-run のため書き込みはしていない")
    return 0


if __name__ == "__main__":
    sys.exit(main())
