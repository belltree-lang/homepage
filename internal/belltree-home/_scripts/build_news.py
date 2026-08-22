#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belltree1102.com — お知らせ・健康コラムの生成（手動実行）

_articles/*.md を読んで、
  news/index.html          一覧ページ
  news/<slug>/index.html   記事ページ
  news/feed.xml            RSS
を書き出す。あわせて sitemap.xml・llms.txt・トップページの最新3件枠も更新し、
最後に _check.py（リンク切れ等の公開前チェック）を通す。

このサイトはビルドツールを入れない方針なので、CI では動かさない。
手元でこのスクリプトを走らせ、出来た HTML をコミットして公開する。

使い方:
    python _scripts/build_news.py --dry-run          何が作られるか見るだけ（組み立ては実際に走らせる）
    python _scripts/build_news.py                    生成する
    python _scripts/build_news.py --include-future   配布日がまだ来ていない記事も出す

記事の書き方（_articles/2026-09-01-example.md）:
    ---
    title: 記事の見出し
    description: 一覧とSNSカードに出る一文
    eyebrow: 帯見出し（紙面にあれば。任意）
    date: 2026-09-01
    category: 健康コラム
    source: べるつりー通信 2026年9月号     ← 任意（紙面の再録なら書く）
    order: 1                              ← 任意（同じ日付の中での並び。大きいほど前）
    draft: false
    ---

    本文（Markdown）

紙面の再録では、確定文言を一字一句変えない。
三点リーダの点数（…と……）も紙面のまま。揃えたくなっても揃えない。
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_nav import build_nav  # ナビの正本は sync_nav.py。ここでは持たない

try:
    import markdown as md_lib
except ImportError:
    print("markdown が入っていません。 python -m pip install markdown", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = ROOT / "_articles"
NEWS_DIR = ROOT / "news"
SITE = "https://belltree1102.com"
JST = timezone(timedelta(hours=9))

# カテゴリ → 色（colors_and_type.css のサービス色トークンを使う）
CATEGORIES: dict[str, str] = {
    "お知らせ": "var(--bt-primary)",
    "健康コラム": "var(--bt-svc-shinkyu)",
    "介護と制度": "var(--bt-svc-kaigo)",
    "べるフィット": "var(--bt-svc-fit)",
    "終活・相続": "var(--bt-svc-shukatsu)",
}
DEFAULT_CATEGORY = "お知らせ"

# --------------------------------------------------------------------------
# 記事の読み込み
# --------------------------------------------------------------------------

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)
# 全角コロンで書かれていても拾う。前後の空白も許す。
FM_LINE_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*[:：]\s*(.*)$")
BOOL_KEYS = {"draft"}
TRUE_WORDS = {"true", "yes", "on", "1"}
FALSE_WORDS = {"false", "no", "off", "0", ""}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_SLUGS = {"index", "feed", "assets"}
DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d")


class ArticleError(ValueError):
    """記事1本の書き方の誤り。どのファイルかを必ず添える。"""


def parse_front_matter(raw: str, where: str) -> tuple[dict, str]:
    """YAMLライブラリを使わずに済む範囲の簡易フロントマター解析。"""
    raw = raw.lstrip("﻿").replace("\r\n", "\n")
    m = FM_RE.match(raw)
    if not m:
        raise ArticleError(f"{where}: フロントマター（--- で囲んだ冒頭）がありません")
    meta: dict = {}
    for lineno, line in enumerate(m.group(1).splitlines(), start=2):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        hit = FM_LINE_RE.match(line)
        if not hit:
            # 黙って捨てると「書いたのに効かない」に化けるので必ず止める
            raise ArticleError(f"{where}:{lineno}: フロントマターの書き方が読めません → {line!r}")
        key, value = hit.group(1).strip(), hit.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
            continue
        value = value.strip("\"'").strip()
        if key in BOOL_KEYS:
            low = value.lower()
            if low in TRUE_WORDS:
                meta[key] = True
            elif low in FALSE_WORDS:
                meta[key] = False
            else:
                raise ArticleError(f"{where}: {key} は true / false で書く（いまは {value!r}）")
        else:
            meta[key] = value
    return meta, m.group(2)


def parse_date(value: str, where: str) -> date:
    s = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise ArticleError(f"{where}: date が読めません（{value!r}）。YYYY-MM-DD で書く")


def load_articles(include_future: bool) -> tuple[list[dict], list[str]]:
    """公開する記事の一覧と、見送った理由の一覧を返す。"""
    notes: list[str] = []
    if not ARTICLES_DIR.exists():
        return [], [f"{ARTICLES_DIR} がありません"]
    today = datetime.now(JST).date()
    posts: list[dict] = []
    seen_slugs: dict[str, str] = {}

    for path in sorted(ARTICLES_DIR.glob("*.md")):
        where = path.name
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"), where)

        if meta.get("draft") is True:
            notes.append(f"{where}: draft: true のため見送り")
            continue
        for required in ("title", "date"):
            if not meta.get(required):
                raise ArticleError(f"{where}: {required} が空です")

        slug = (meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)).strip()
        if not SLUG_RE.match(slug):
            raise ArticleError(
                f"{where}: slug「{slug}」は使えません。半角英小文字・数字・ハイフンだけで書く"
            )
        if slug in RESERVED_SLUGS:
            raise ArticleError(f"{where}: slug「{slug}」は news/ の予約語なので使えません")
        if slug in seen_slugs:
            raise ArticleError(f"{where}: slug「{slug}」が {seen_slugs[slug]} と重複しています")
        seen_slugs[slug] = where

        d = parse_date(meta["date"], where)
        if d > today and not include_future:
            notes.append(f"{where}: 掲載日 {d.isoformat()} がまだ来ていないため見送り（--include-future で出せる）")
            continue

        category = meta.get("category") or DEFAULT_CATEGORY
        if category not in CATEGORIES:
            raise ArticleError(f"{where}: 未定義のカテゴリ「{category}」")

        try:
            order = int(str(meta.get("order", 0) or 0))
        except ValueError:
            raise ArticleError(f"{where}: order は整数で書く（いまは {meta.get('order')!r}）")

        posts.append(
            {
                "slug": slug,
                "title": meta["title"],
                "description": meta.get("description", ""),
                "eyebrow": meta.get("eyebrow", ""),
                "date": d.isoformat(),
                "date_obj": d,
                "category": category,
                "source": meta.get("source", ""),
                "tags": meta.get("tags", []),
                # 同じ日付の記事の並び順。大きいほど前に出る（既定0）
                "order": order,
                "body": md_lib.markdown(body, extensions=["extra", "sane_lists"]),
                "path": path,
            }
        )

    posts.sort(key=lambda p: (p["date_obj"], p["order"], p["slug"]), reverse=True)
    return posts, notes


def jp_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.year}年{d.month}月{d.day}日"


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def ld_json(obj: dict) -> str:
    """構造化データ。</script> や & がそのまま出ると HTML を壊すので退避する。"""
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    return s.replace("<", "\\u003C").replace(">", "\\u003E").replace("&", "\\u0026")


# --------------------------------------------------------------------------
# 共通パーツ（ヘッダー・フッター・CSS）
# --------------------------------------------------------------------------

# 注: ヘッダーの折返し（1120px）・小さい画面の詰め（430px）・カード類は
#     colors_and_type.css が正本。ここではそれと重ならないものだけ持つ。
CHROME_CSS = """
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; overflow-x: hidden; }
  img { display: block; max-width: 100%; }
  a { text-decoration: none; }
  .wrap { max-width: var(--bt-container); margin: 0 auto; padding: 0 var(--bt-gutter); }

  /* HEADER */
  .site-header { position: sticky; top: 0; z-index: 100; background: rgba(252,252,250,0.82); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid var(--bt-line); }
  .header-inner { height: 64px; display: flex; align-items: center; gap: var(--bt-s-5); }
  .brand { display: flex; align-items: center; gap: 12px; flex-shrink: 0; }
  .brand img { width: 38px; height: 38px; }
  .brand-name { font-family: var(--bt-font-serif); font-weight: 600; font-size: 20px; color: var(--bt-primary); letter-spacing: 0.01em; line-height: 1; display: flex; align-items: baseline; gap: 7px; white-space: nowrap; }
  .brand-name .jp { font-size: 14px; color: var(--bt-ink-3); font-weight: 500; }
  .brand-name .sep { color: var(--bt-line); font-weight: 300; }
  .main-nav { display: flex; gap: 22px; margin-left: auto; }
  .main-nav a { font-size: 14px; font-weight: 500; color: var(--bt-ink-2); white-space: nowrap; letter-spacing: 0.01em; transition: color var(--bt-dur) var(--bt-ease); }
  .main-nav a:hover { color: var(--bt-accent); }
  .header-cta { display: flex; align-items: center; gap: 18px; flex-shrink: 0; }
  .header-phone { display: flex; align-items: center; gap: 7px; font-family: var(--bt-font-serif); font-weight: 600; font-size: 18px; color: var(--bt-primary); white-space: nowrap; }
  .header-phone svg { width: 17px; height: 17px; color: var(--bt-accent); }
  .btn-sm { display: inline-flex; align-items: center; justify-content: center; white-space: nowrap; height: 40px; padding: 0 20px; border-radius: var(--bt-r-pill); background: var(--bt-accent); color: #fff; font-weight: 600; font-size: 13px; letter-spacing: 0.03em; border: 1px solid transparent; transition: background var(--bt-dur) var(--bt-ease); }
  .btn-sm:hover { background: var(--bt-accent-hover); color: #fff; }

  .info-bar { background: var(--bt-accent); color: #fff; }
  .info-bar .wrap { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 6px 18px; padding-top: 9px; padding-bottom: 9px; font-size: 12.5px; font-weight: 500; letter-spacing: 0.03em; }
  .info-bar .wrap > span { white-space: nowrap; }
  .info-bar .dot { opacity: 0.5; }

  .breadcrumb { background: var(--bt-bg-sunk); border-bottom: 1px solid var(--bt-line-soft); }
  .breadcrumb .wrap { display: flex; gap: 8px; padding: 12px 0; font-size: 12px; color: var(--bt-ink-3); flex-wrap: wrap; }
  .breadcrumb a { color: var(--bt-ink-3); }
  .breadcrumb a:hover { color: var(--bt-accent); }
  .breadcrumb .sep { color: var(--bt-line); }
  .breadcrumb [aria-current="page"] { color: var(--bt-primary); font-weight: 600; }

  /* 紙テクスチャ */
  body { background-color: #FAF4EA; background-image: radial-gradient(circle at 10% 8%, rgba(255,232,212,0.55) 0%, transparent 35%), radial-gradient(circle at 92% 18%, rgba(255,225,210,0.40) 0%, transparent 40%), radial-gradient(circle at 22% 88%, rgba(232,221,200,0.45) 0%, transparent 45%), radial-gradient(circle at 88% 78%, rgba(255,232,217,0.35) 0%, transparent 38%); background-attachment: fixed; }

  .page-hero { position: relative; padding: 64px 0 40px; }
  .hero-text { max-width: 760px; margin: 0 auto; text-align: center; }
  .hero-text .eyebrow { font-size: 12px; letter-spacing: 0.18em; color: var(--bt-ink-4); font-weight: 600; display: block; margin-bottom: 18px; text-transform: uppercase; }
  .hero-text h1 { font-family: var(--bt-font-serif); font-weight: 600; font-size: clamp(28px, 3.8vw, 42px); line-height: 1.45; margin: 0 0 22px; color: var(--bt-primary); letter-spacing: 0.02em; }
  .hero-text p.lead { font-size: 15.5px; color: var(--bt-ink-2); line-height: 2; font-weight: 500; margin: 0; }
  section { position: relative; }
  .sec-pad { padding: 40px 0 64px; }

  .btn { display: inline-flex; align-items: center; justify-content: center; gap: 9px; height: 50px; padding: 0 30px; border-radius: var(--bt-r-pill); font-family: var(--bt-font-sans); font-weight: 600; font-size: 15px; letter-spacing: 0.03em; border: 1.5px solid transparent; transition: background var(--bt-dur) var(--bt-ease); }
  .btn--primary { background: var(--bt-accent); color: #fff; box-shadow: 0 2px 0 rgba(0,0,0,.04), 0 8px 18px rgba(194,122,101,.30); }
  .btn--primary:hover { background: var(--bt-accent-hover); }
  .btn--ghost { background: transparent; color: var(--bt-primary); border-color: var(--bt-line); }
  .btn--ghost:hover { background: var(--bt-bg-sunk); }
  .cta-row { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }

  .approach-final { background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.85); max-width: 920px; margin: 0 auto; border-radius: var(--bt-r-xl); box-shadow: var(--bt-shadow-1); border-top: 4px solid var(--bt-primary); padding: 40px 44px; text-align: center; }
  .approach-final h2 { font-family: var(--bt-font-serif); font-weight: 600; font-size: 22px; color: var(--bt-primary); margin: 0 0 16px; }
  .approach-final > p { font-size: 14.5px; color: var(--bt-ink-2); line-height: 2.05; margin: 0 0 26px; }

  /* FOOTER */
  .site-footer { background: #16202E; color: rgba(255,255,255,0.7); }
  .footer-top { padding: 64px var(--bt-gutter) 48px; display: grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 40px; }
  .f-brand img { width: 44px; height: 44px; margin-bottom: 16px; }
  .f-brand .name { font-family: var(--bt-font-serif); font-size: 20px; color: #fff; margin-bottom: 14px; }
  .f-brand p { font-size: 13px; line-height: 1.9; color: rgba(255,255,255,0.55); margin: 0 0 18px; max-width: 280px; }
  .footer-col h5 { font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--bt-group); margin: 0 0 18px; font-weight: 600; }
  .footer-col ul { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 11px; }
  .footer-col a { font-size: 13.5px; color: rgba(255,255,255,0.68); transition: color var(--bt-dur) var(--bt-ease); }
  .footer-col a:hover { color: #fff; }
  .footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); padding: 22px var(--bt-gutter); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 12px; color: rgba(255,255,255,0.45); }

  @media (max-width: 760px) { .footer-top { grid-template-columns: 1fr 1fr; } .approach-final { padding: 26px 22px; } }
  @media (max-width: 480px) {
    .footer-top { grid-template-columns: 1fr; }
    .info-bar .wrap { font-size: 11px; gap: 6px 12px; }
    /* 他ページと同じ畳み方にそろえる */
    .footer-bottom { flex-direction: column; align-items: flex-start; gap: 6px; }
    .header-inner { gap: 10px; }
    .brand-name { font-size: 17px; }
    .brand-name .jp { font-size: 12px; }
    .header-cta { gap: 10px; }
    .btn-sm { height: 38px; padding: 0 15px; font-size: 12px; }
  }

  /* ハンバーガー・ドロワー（表示の切り替えは colors_and_type.css の 1120px が持つ） */
  .nav-toggle { display: none; width: 44px; height: 44px; flex-shrink: 0; flex-direction: column; align-items: center; justify-content: center; gap: 5px; padding: 0; border: 1px solid var(--bt-line); border-radius: 10px; background: rgba(255,255,255,0.7); cursor: pointer; }
  .nav-toggle span { display: block; width: 20px; height: 2px; border-radius: 2px; background: var(--bt-primary); transition: transform var(--bt-dur) var(--bt-ease), opacity var(--bt-dur) var(--bt-ease); }
  body.drawer-open .nav-toggle span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  body.drawer-open .nav-toggle span:nth-child(2) { opacity: 0; }
  body.drawer-open .nav-toggle span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  .nav-drawer { position: fixed; top: 64px; left: 0; right: 0; bottom: 0; z-index: 99; background: rgba(252,252,250,0.98); -webkit-backdrop-filter: blur(10px); backdrop-filter: blur(10px); transform: translateX(100%); transition: transform var(--bt-dur-slow) var(--bt-ease); overflow-y: auto; visibility: hidden; }
  body.drawer-open .nav-drawer { transform: translateX(0); visibility: visible; }
  .nav-drawer-inner { display: flex; flex-direction: column; padding: 20px 24px 40px; }
  .nav-drawer-inner a { font-size: 16px; font-weight: 600; color: var(--bt-ink-1); padding: 17px 6px; border-bottom: 1px solid var(--bt-line-soft); white-space: nowrap; }
  .nav-drawer-inner a:hover { color: var(--bt-accent); }

  .fab-call{position:fixed;right:18px;bottom:18px;z-index:900;display:inline-flex;align-items:center;gap:10px;height:60px;padding:0 22px 0 19px;border-radius:40px;background:var(--bt-accent,#C27A65);color:#fff;box-shadow:0 12px 30px rgba(80,55,30,.30);text-decoration:none;font-family:var(--bt-font-sans,"Noto Sans JP",sans-serif);}
  .fab-call svg{width:25px;height:25px;flex:none;}
  .fab-call .fab-call-txt{display:flex;flex-direction:column;line-height:1.15;font-weight:700;font-size:15px;}
  .fab-call .fab-call-txt small{font-weight:600;font-size:11.5px;opacity:.9;letter-spacing:.2px;margin-top:1px;}
  .fab-call:hover{background:var(--bt-accent-hover,#A8634F);}
  @media(max-width:560px){.fab-call{right:12px;bottom:12px;height:54px;padding:0 18px 0 16px;gap:8px;}.fab-call svg{width:22px;height:22px;}.fab-call .fab-call-txt{font-size:13px;}.fab-call .fab-call-txt small{font-size:11px;}}
"""

# 注: カード本体（.news-grid / .news-card ほか）の CSS は colors_and_type.css が正本。
# ここではその上に乗る、一覧と記事だけで使うものを定義する。
NEWS_CSS = """
  /* ---- お知らせ 一覧 ---- */
  .cat-filter { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 0 auto 40px; max-width: 900px; }
  .cat-chip { display: inline-flex; align-items: center; height: 36px; padding: 0 18px; border-radius: var(--bt-r-pill); border: 1px solid var(--bt-line); background: rgba(255,255,255,0.7); font-size: 13px; font-weight: 600; color: var(--bt-ink-2); cursor: pointer; transition: background var(--bt-dur) var(--bt-ease), color var(--bt-dur) var(--bt-ease), border-color var(--bt-dur) var(--bt-ease); }
  .cat-chip:hover { border-color: var(--bt-accent); color: var(--bt-accent); }
  .cat-chip[aria-pressed="true"] { background: var(--bt-primary); border-color: var(--bt-primary); color: #fff; }

  /* ---- 記事本文 ---- */
  .article-head { max-width: 780px; margin: 0 auto; text-align: center; padding: 56px 0 8px; }
  .article-head .news-meta { justify-content: center; }
  .article-head .band { display: block; font-size: 13px; font-weight: 600; letter-spacing: 0.08em; color: var(--cat-color, var(--bt-accent)); margin: 0 0 14px; }
  .article-head h1 { font-family: var(--bt-font-serif); font-weight: 600; font-size: clamp(25px, 3.4vw, 36px); line-height: 1.6; color: var(--bt-primary); margin: 0 0 18px; letter-spacing: 0.02em; }
  .article-head .lead { font-size: 15px; color: var(--bt-ink-2); line-height: 2; margin: 0; }
  .article-source { display: inline-block; margin-top: 20px; font-size: 12.5px; color: var(--bt-ink-4); border: 1px solid var(--bt-line); border-radius: var(--bt-r-pill); padding: 6px 16px; background: rgba(255,255,255,0.6); }

  .article-body { max-width: 780px; margin: 0 auto; background: rgba(255,255,255,0.72); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.85); border-radius: 18px; box-shadow: 0 10px 30px rgba(80,55,30,0.08); padding: 44px 48px; }
  .article-body > *:first-child { margin-top: 0; }
  .article-body > *:last-child { margin-bottom: 0; }
  .article-body h2 { font-family: var(--bt-font-serif); font-weight: 600; font-size: 21px; color: var(--bt-primary); line-height: 1.6; margin: 44px 0 18px; padding-left: 14px; border-left: 4px solid var(--cat-color, var(--bt-accent)); letter-spacing: 0.01em; }
  .article-body h3 { font-weight: 600; font-size: 17px; color: var(--bt-ink-1); line-height: 1.7; margin: 32px 0 12px; }
  .article-body p { font-size: 15px; color: var(--bt-ink-2); line-height: 2.05; margin: 0 0 18px; }
  .article-body ul, .article-body ol { margin: 0 0 20px; padding-left: 1.4em; }
  .article-body li { font-size: 15px; color: var(--bt-ink-2); line-height: 2.0; margin-bottom: 8px; }
  .article-body strong { color: var(--bt-ink-1); font-weight: 700; }
  .article-body a { color: var(--bt-accent); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
  .article-body blockquote { margin: 0 0 22px; padding: 20px 24px; background: var(--bt-bg-sunk); border-radius: var(--bt-r-md); border-left: 3px solid var(--bt-line); }
  .article-body blockquote p { margin: 0; font-size: 14.5px; color: var(--bt-ink-3); }
  .article-body table { width: 100%; border-collapse: collapse; margin: 0 0 22px; font-size: 14px; }
  .article-body th, .article-body td { border: 1px solid var(--bt-line); padding: 11px 14px; text-align: left; line-height: 1.8; }
  .article-body th { background: var(--bt-bg-sunk); font-weight: 600; color: var(--bt-primary); }
  .article-body img { border-radius: var(--bt-r-md); margin: 0 auto 22px; }
  .article-body hr { border: none; border-top: 1px solid var(--bt-line); margin: 36px 0; }

  .article-foot { max-width: 780px; margin: 32px auto 0; display: flex; justify-content: center; }
  .related { max-width: 1000px; margin: 0 auto; }
  /* 直下の見出しだけ。カード内の見出しまで中央寄せにしないこと */
  .related > h2 { font-family: var(--bt-font-serif); font-weight: 600; font-size: 19px; color: var(--bt-primary); text-align: center; margin: 0 0 26px; }
  /* 関連が2本以下のとき、3列グリッドの左寄せにならないよう中央に寄せる */
  .related .news-grid { grid-template-columns: repeat(auto-fit, minmax(240px, 318px)); justify-content: center; }

  @media (max-width: 600px) { .article-body { padding: 28px 22px; } .article-head { padding-top: 36px; } }
"""

DRAWER_JS = """
(function(){
  var btn = document.querySelector('.nav-toggle');
  var drawer = document.getElementById('nav-drawer');
  var nav = document.querySelector('.main-nav');
  if (!btn || !drawer) return;
  if (!nav) { btn.style.display = 'none'; return; }
  drawer.innerHTML = '<nav class="nav-drawer-inner">' + nav.innerHTML + '</nav>';
  function setOpen(o){
    document.body.classList.toggle('drawer-open', o);
    btn.setAttribute('aria-expanded', o ? 'true' : 'false');
    drawer.setAttribute('aria-hidden', o ? 'false' : 'true');
  }
  btn.addEventListener('click', function(){ setOpen(!document.body.classList.contains('drawer-open')); });
  drawer.addEventListener('click', function(e){ if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') setOpen(false); });
})();
"""

FILTER_JS = """
(function(){
  var chips = document.querySelectorAll('.cat-chip');
  var cards = document.querySelectorAll('.news-card');
  var empty = document.querySelector('.news-empty');
  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      var cat = chip.dataset.cat;
      chips.forEach(function(c){ c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      var shown = 0;
      cards.forEach(function(card){
        var hit = (cat === 'all' || card.dataset.cat === cat);
        card.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      if (empty) empty.style.display = shown ? 'none' : '';
    });
  });
})();
"""


def nav_html(page_rel: str) -> str:
    """ナビの中身は sync_nav.py の NAV_ITEMS が正本。ここでは組み立てるだけ。"""
    links = "\n".join(f"      {a}" for a in build_nav(page_rel))
    return f'    <nav class="main-nav">\n{links}\n    </nav>'


PHONE_SVG = (
    '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M14 10 H 20 L 23 17 L 19 20 '
    'C 21 25 23 27 28 29 L 31 25 L 38 28 V 34 C 38 36 36 38 34 38 C 22 38 10 26 10 14 C 10 12 12 10 14 10 Z"/></svg>'
)


def header_html(prefix: str, page_rel: str) -> str:
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="べるつりーグループ">
      <img src="{prefix}assets/belltree-mark.svg" alt="" />
      <span class="brand-name">BellTree<span class="sep">／</span><span class="jp">べるつりー</span></span>
    </a>
{nav_html(page_rel)}
    <div class="header-cta">
      <span class="header-phone">
        {PHONE_SVG}
        042-682-2839
      </span>
      <a class="btn-sm" href="{prefix}contact/index.html">ご相談窓口</a>
      <button class="nav-toggle" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="nav-drawer">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="nav-drawer" id="nav-drawer" aria-hidden="true"></div>

<div class="info-bar">
  <div class="wrap">
    <span><strong>株式会社べるつりー</strong></span>
    <span class="dot">・</span>
    <span>八王子・南大沢・町田・日野・多摩</span>
    <span class="dot">／</span>
    <span>TEL 042-682-2839</span>
    <span class="dot">／</span>
    <span>平日 9:00〜18:00（日祝休）</span>
  </div>
</div>"""


def footer_html(prefix: str) -> str:
    return f"""<footer class="site-footer" id="final">
  <div class="wrap footer-top">
    <div class="f-brand">
      <img src="{prefix}assets/belltree-mark.svg" alt="" loading="lazy" />
      <div class="name">べるつりーグループ</div>
      <p>運動から介護、終活までを横断し、地域で人生後半を支える総合サポート企業です。</p>
    </div>
    <div class="footer-col">
      <h5>企業情報</h5>
      <ul>
        <li><a href="{prefix}index.html">ホーム</a></li>
        <li><a href="{prefix}about/index.html">会社概要</a></li>
        <li><a href="{prefix}team/index.html">スタッフ紹介</a></li>
        <li><a href="{prefix}recruit/index.html">採用情報</a></li>
        <li><a href="{prefix}news/index.html">お知らせ</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h5>サービス</h5>
      <ul>
        <li><a href="{prefix}services/home-visit/index.html">訪問鍼灸マッサージ</a></li>
        <li><a href="{prefix}services/fee-insurance/index.html">料金と保険</a></li>
        <li><a href="{prefix}services/home-care/index.html">居宅介護支援</a></li>
        <li><a href="{prefix}services/bellfit/index.html">べるフィット</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h5>お問い合わせ</h5>
      <ul>
        <li><a href="tel:0426822839" onclick="if(window.gtag){{gtag('event','generate_lead',{{method:'phone',page:'footer'}});}}">042-682-2839</a></li>
        <li class="line-cta line-cta--footer"><a href="https://lin.ee/tag9YEf" target="_blank" rel="noopener noreferrer" onclick="if(window.gtag){{gtag('event','line_click',{{method:'line',page:'footer'}});}}">LINEで相談する</a></li>
        <li><a href="{prefix}contact/index.html">お問い合わせフォーム</a></li>
        <li><a href="{prefix}faq/index.html">よくある質問</a></li>
        <li><a href="{prefix}privacy-policy/index.html">個人情報保護方針</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-nap" style="padding:0 var(--bt-gutter) 18px;">
    <address style="font-style:normal;font-size:12.5px;line-height:1.9;color:rgba(255,255,255,0.5);">株式会社べるつりー　〒192-0375 東京都八王子市下柚木3-7-2-401　TEL 042-682-2839</address>
  </div>
  <div class="wrap footer-bottom">
    <span>© 2026 株式会社べるつりー / Belltree Group</span>
    <span style="color:var(--bt-group);font-weight:600;letter-spacing:0.04em">わたしたちは、一本の木。</span>
  </div>
</footer>

<a class="fab-call" href="tel:0426822839" aria-label="電話で相談する 042-682-2839" onclick="if(window.gtag){{gtag('event','generate_lead',{{method:'phone',page:'fab'}});}}">
  {PHONE_SVG.replace('stroke-width="2.4"', 'stroke-width="2.6"')}
  <span class="fab-call-txt">電話で相談<small>042-682-2839</small></span>
</a>"""


def head_html(prefix: str, title: str, description: str, canonical: str,
              og_type: str = "website", extra: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-RQRJ45S3V3"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-RQRJ45S3V3');</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(description)}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:site_name" content="株式会社べるつりー" />
<meta property="og:type" content="{og_type}" />
<meta property="og:image" content="{SITE}/assets/img/og/og-default.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{SITE}/assets/img/og/og-default.jpg" />
<meta property="og:locale" content="ja_JP" />
<link rel="alternate" type="application/rss+xml" title="べるつりー お知らせ" href="{SITE}/news/feed.xml" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="{prefix}colors_and_type.css" />
<style>{CHROME_CSS}{NEWS_CSS}</style>
{extra}
</head>
<body>
"""


def card_html(post: dict, prefix_to_news: str) -> str:
    color = CATEGORIES[post["category"]]
    desc = post["description"] or ""
    return f"""    <a class="news-card" href="{prefix_to_news}{post['slug']}/index.html" data-cat="{esc(post['category'])}" style="--cat-color: {color};">
      <div class="news-meta">
        <span class="news-cat">{esc(post['category'])}</span>
        <time class="news-date" datetime="{post['date']}">{jp_date(post['date'])}</time>
      </div>
      <h3>{esc(post['title'])}</h3>
      <p>{esc(desc)}</p>
      <span class="news-more">続きを読む →</span>
    </a>"""


# --------------------------------------------------------------------------
# ページ生成
# --------------------------------------------------------------------------

def render_index(posts: list[dict]) -> str:
    prefix = "../"
    used_cats = [c for c in CATEGORIES if any(p["category"] == c for p in posts)]
    chips = '\n'.join(
        f'      <button class="cat-chip" type="button" data-cat="{esc(c)}" aria-pressed="false">{esc(c)}</button>'
        for c in used_cats
    )
    cards = "\n".join(card_html(p, "") for p in posts)

    breadcrumb_ld = ld_json({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "お知らせ・健康コラム", "item": f"{SITE}/news/"},
        ],
    })

    extra = f'<script type="application/ld+json">\n{breadcrumb_ld}\n</script>'

    return (
        head_html(
            prefix,
            "お知らせ・健康コラム｜株式会社べるつりー",
            "べるつりーグループからのお知らせと、毎月お配りしている「べるつりー通信」から生まれた健康コラム。季節ごとの体調の注意点、介護保険や医療保険のしくみ、地域での取り組みをご紹介します。",
            f"{SITE}/news/",
            "website",
            extra,
        )
        + header_html(prefix, "news/index.html")
        + f"""
<nav class="breadcrumb" aria-label="現在位置">
  <div class="wrap">
    <a href="{prefix}index.html">ホーム</a>
    <span class="sep">／</span>
    <span aria-current="page">お知らせ・健康コラム</span>
  </div>
</nav>

<section class="page-hero" id="top">
  <div class="wrap">
    <div class="hero-text">
      <span class="eyebrow">News &amp; Column</span>
      <h1>お知らせ・健康コラム</h1>
      <p class="lead">べるつりーグループからのお知らせと、毎月お配りしている「べるつりー通信」の健康コラムをここにまとめています。季節ごとの体調の注意点や、介護保険・医療保険のしくみなど、ご家族やケアマネジャーの方にも役立つ内容をお届けします。</p>
    </div>
  </div>
</section>

<section class="sec-pad" aria-labelledby="news-list-title">
  <div class="wrap">
    <h2 class="sr-only" id="news-list-title">記事の一覧</h2>
    <div class="cat-filter">
      <button class="cat-chip" type="button" data-cat="all" aria-pressed="true">すべて</button>
{chips}
    </div>
    <div class="news-grid">
{cards}
    </div>
    <p class="news-empty" style="display:none;">この分類の記事はまだありません。</p>
  </div>
</section>

<section class="sec-pad" style="padding-top:0;">
  <div class="wrap">
    <div class="approach-final">
      <h2>気になることは、お気軽にご相談ください</h2>
      <p>「うちの場合はどうだろう」と思われたら、まずはお電話ください。ご本人・ご家族・ケアマネジャーの方、どなたからのご相談もお受けしています。</p>
      <div class="cta-row">
        <a class="btn btn--primary" href="tel:0426822839" onclick="if(window.gtag){{gtag('event','generate_lead',{{method:'phone',page:'news'}});}}">042-682-2839 に電話する</a>
        <a class="btn btn--ghost" href="{prefix}contact/index.html">お問い合わせフォーム</a>
      </div>
    </div>
  </div>
</section>

"""
        + footer_html(prefix)
        + f"\n<script>{DRAWER_JS}{FILTER_JS}</script>\n</body>\n</html>\n"
    )


def render_article(post: dict, posts: list[dict]) -> str:
    prefix = "../../"
    color = CATEGORIES[post["category"]]
    related = [p for p in posts if p["slug"] != post["slug"] and p["category"] == post["category"]][:3]
    if len(related) < 3:
        chosen = {p["slug"] for p in related} | {post["slug"]}
        related += [p for p in posts if p["slug"] not in chosen][: 3 - len(related)]

    article_ld = ld_json({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "datePublished": post["date"],
        "dateModified": post["date"],
        "articleSection": post["category"],
        "inLanguage": "ja",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/news/{post['slug']}/"},
        "author": {"@type": "Organization", "name": "株式会社べるつりー"},
        "publisher": {
            "@type": "Organization",
            "name": "株式会社べるつりー",
            "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/belltree-mark.svg"},
        },
    })

    breadcrumb_ld = ld_json({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "お知らせ・健康コラム", "item": f"{SITE}/news/"},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": f"{SITE}/news/{post['slug']}/"},
        ],
    })

    extra = (
        f'<script type="application/ld+json">\n{article_ld}\n</script>\n'
        f'<script type="application/ld+json">\n{breadcrumb_ld}\n</script>'
    )

    band_html = f'      <span class="band">{esc(post["eyebrow"])}</span>\n' if post["eyebrow"] else ""
    source_html = ""
    if post["source"]:
        source_html = f'      <span class="article-source">この記事は「{esc(post["source"])}」からの再録です</span>\n'

    related_html = ""
    if related:
        cards = "\n".join(card_html(p, "../") for p in related)
        related_html = f"""
<section class="sec-pad" style="padding-top:24px;">
  <div class="wrap">
    <div class="related">
      <h2>あわせて読みたい</h2>
      <div class="news-grid">
{cards}
      </div>
    </div>
  </div>
</section>
"""

    return (
        head_html(
            prefix,
            f"{post['title']}｜株式会社べるつりー",
            post["description"],
            f"{SITE}/news/{post['slug']}/",
            "article",
            extra,
        )
        + header_html(prefix, f"news/{post['slug']}/index.html")
        + f"""
<nav class="breadcrumb" aria-label="現在位置">
  <div class="wrap">
    <a href="{prefix}index.html">ホーム</a>
    <span class="sep">／</span>
    <a href="../index.html">お知らせ・健康コラム</a>
    <span class="sep">／</span>
    <span aria-current="page">{esc(post['title'])}</span>
  </div>
</nav>

<article style="--cat-color: {color};">
  <div class="wrap">
    <header class="article-head">
      <div class="news-meta">
        <span class="news-cat">{esc(post['category'])}</span>
        <time class="news-date" datetime="{post['date']}">{jp_date(post['date'])}</time>
      </div>
{band_html}      <h1>{esc(post['title'])}</h1>
      <p class="lead">{esc(post['description'])}</p>
{source_html}    </header>
  </div>

  <section class="sec-pad">
    <div class="wrap">
      <div class="article-body">
{post['body']}
      </div>
      <div class="article-foot">
        <a class="btn btn--ghost" href="../index.html">← お知らせ一覧へもどる</a>
      </div>
    </div>
  </section>
</article>
{related_html}
<section class="sec-pad" style="padding-top:0;">
  <div class="wrap">
    <div class="approach-final">
      <h2>気になることは、お気軽にご相談ください</h2>
      <p>記事を読んで「うちの場合はどうだろう」と思われたら、まずはお電話ください。ご本人・ご家族・ケアマネジャーの方、どなたからのご相談もお受けしています。</p>
      <div class="cta-row">
        <a class="btn btn--primary" href="tel:0426822839" onclick="if(window.gtag){{gtag('event','generate_lead',{{method:'phone',page:'news-article'}});}}">042-682-2839 に電話する</a>
        <a class="btn btn--ghost" href="{prefix}contact/index.html">お問い合わせフォーム</a>
      </div>
    </div>
  </div>
</section>

"""
        + footer_html(prefix)
        + f"\n<script>{DRAWER_JS}</script>\n</body>\n</html>\n"
    )


def render_feed(posts: list[dict]) -> str:
    # 「中身が最後に変わった日」＝いちばん新しい記事の日付。
    # ここに実行時刻を入れると、走らせるたびに差分が出て git が汚れる。
    newest = datetime.strptime(posts[0]["date"], "%Y-%m-%d").replace(tzinfo=JST) if posts else datetime.now(JST)
    now = newest.strftime("%a, %d %b %Y 09:00:00 +0900")
    items = []
    for p in posts[:20]:
        pub = datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=JST)
        items.append(f"""    <item>
      <title>{esc(p['title'])}</title>
      <link>{SITE}/news/{p['slug']}/</link>
      <guid isPermaLink="true">{SITE}/news/{p['slug']}/</guid>
      <description>{esc(p['description'])}</description>
      <category>{esc(p['category'])}</category>
      <pubDate>{pub.strftime('%a, %d %b %Y 09:00:00 +0900')}</pubDate>
    </item>""")
    body = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>べるつりー お知らせ・健康コラム</title>
    <link>{SITE}/news/</link>
    <description>株式会社べるつりーからのお知らせと健康コラム</description>
    <language>ja</language>
    <lastBuildDate>{now}</lastBuildDate>
{body}
  </channel>
</rss>
"""


# --------------------------------------------------------------------------
# 派生ファイルの更新
#   どれも「静かに何もしない」が一番こわいので、
#   当たらなかったときは False を返して呼び出し側で失敗にする。
# --------------------------------------------------------------------------

TOP_START = "<!-- NEWS_LATEST_START -->"
TOP_END = "<!-- NEWS_LATEST_END -->"


def update_top_page(posts: list[dict], dry: bool) -> tuple[bool, str]:
    path = ROOT / "index.html"
    if not path.exists():
        return False, "トップページ index.html が見つからない"
    text = path.read_text(encoding="utf-8")
    if TOP_START not in text or TOP_END not in text:
        return False, "トップページに差し込み口（NEWS_LATEST マーカー）がない"
    latest = posts[:3]
    cards = "\n".join(card_html(p, "news/") for p in latest)
    block = f"""{TOP_START}
<section class="band-paper sec-pad" id="news" style="border-top:1px solid var(--bt-line-soft)">
  <div class="wrap">
    <div class="news-sec-head">
      <span class="news-eyebrow">News &amp; Column</span>
      <h2>お知らせ・健康コラム</h2>
      <p>毎月お配りしている「べるつりー通信」の健康コラムと、グループからのお知らせをお届けしています。</p>
    </div>
    <div class="news-grid">
{cards}
    </div>
    <div class="news-actions">
      <a class="btn btn--ghost" href="news/index.html">お知らせを一覧で見る</a>
    </div>
  </div>
</section>
{TOP_END}"""
    pattern = re.compile(re.escape(TOP_START) + r".*?" + re.escape(TOP_END), re.S)
    new_text = pattern.sub(lambda _: block, text)
    if new_text == text:
        return True, "トップページ: 変更なし"
    if not dry:
        path.write_text(new_text, encoding="utf-8")
    return True, f"トップページ: 最新{len(latest)}件を更新"


def update_sitemap(posts: list[dict], dry: bool) -> tuple[bool, str]:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return False, "sitemap.xml が見つからない"
    text = path.read_text(encoding="utf-8")
    if "</urlset>" not in text:
        return False, "sitemap.xml に </urlset> がない"
    # 既存の /news/ 行をいったん全部落としてから入れ直す（重複防止）
    text = re.sub(
        r"[ \t]*<url><loc>" + re.escape(SITE) + r"/news/[^<]*</loc>.*?</url>\n", "", text, flags=re.S
    )
    newest = posts[0]["date"] if posts else datetime.now(JST).strftime("%Y-%m-%d")
    lines = [
        f'  <url><loc>{SITE}/news/</loc><lastmod>{newest}</lastmod>'
        f'<changefreq>weekly</changefreq><priority>0.7</priority></url>'
    ]
    for p in posts:
        lines.append(
            f'  <url><loc>{SITE}/news/{p["slug"]}/</loc><lastmod>{p["date"]}</lastmod><priority>0.6</priority></url>'
        )
    block = "\n".join(lines) + "\n"
    new_text = text.replace("</urlset>", block + "</urlset>")
    if not dry:
        path.write_text(new_text, encoding="utf-8")
    return True, f"sitemap.xml: {len(posts) + 1} 件のURLを登録"


LLMS_START = "## お知らせ・健康コラム"


def update_llms(posts: list[dict], dry: bool) -> tuple[bool, str]:
    path = ROOT / "llms.txt"
    if not path.exists():
        return False, "llms.txt が見つからない"
    text = path.read_text(encoding="utf-8")
    lines = [LLMS_START, ""]
    lines.append(
        f"毎月お配りしている紙の「べるつりー通信」の健康コラムと、グループからのお知らせを掲載しています。一覧: {SITE}/news/"
    )
    lines.append("")
    for p in posts[:20]:
        desc = p["description"] or ""
        lines.append(f"- [{p['title']}]({SITE}/news/{p['slug']}/): {desc}")
    block = "\n".join(lines) + "\n"

    if LLMS_START in text:
        new_text = re.sub(
            re.escape(LLMS_START) + r".*?(?=\n## |\Z)", lambda _: block.rstrip("\n") + "\n", text, flags=re.S
        )
    else:
        new_text = text.rstrip("\n") + "\n\n" + block
    if LLMS_START not in new_text:
        return False, "llms.txt: 差し替えに失敗した"
    if not dry:
        path.write_text(new_text, encoding="utf-8")
    return True, f"llms.txt: {min(len(posts), 20)} 件を掲載"


def prune_orphans(posts: list[dict], dry: bool) -> list[str]:
    """記事mdが消えた・draftに戻ったのに news/ に残っているページを片づける。"""
    if not NEWS_DIR.exists():
        return []
    keep = {p["slug"] for p in posts}
    removed = []
    for child in sorted(NEWS_DIR.iterdir()):
        if not child.is_dir() or child.name in keep:
            continue
        if not (child / "index.html").exists():
            continue  # 生成物でなさそうなものは触らない
        removed.append(child.name)
        if not dry:
            shutil.rmtree(child)
    return removed


def run_check() -> tuple[bool, str]:
    """公開前チェック（_check.py）をそのまま通す。"""
    script = ROOT / "_check.py"
    if not script.exists():
        return True, "_check.py が無いので省略"
    proc = subprocess.run(
        [sys.executable, str(script)], cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8"
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    ok = "errors: 0" in out
    return ok, out.strip()


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="書き出さずに結果だけ表示（組み立ては実際に走らせる）")
    ap.add_argument("--include-future", action="store_true", help="掲載日がまだ来ていない記事も出す")
    args = ap.parse_args()

    try:
        posts, notes = load_articles(args.include_future)
    except ArticleError as e:
        print(f"記事の書き方に誤りがあります:\n  {e}", file=sys.stderr)
        return 1

    for n in notes:
        print(f"  見送り: {n}")
    if not posts:
        print("公開できる記事が _articles/ にありません", file=sys.stderr)
        return 1

    print(f"記事 {len(posts)} 件を読み込みました")
    for p in posts:
        print(f"  {p['date']}  [{p['category']}]  {p['title']}  → news/{p['slug']}/")

    # --dry-run でも組み立てだけは必ず走らせる（テンプレートの壊れをここで拾う）
    pages = {NEWS_DIR / "index.html": render_index(posts)}
    for p in posts:
        pages[NEWS_DIR / p["slug"] / "index.html"] = render_article(p, posts)
    pages[NEWS_DIR / "feed.xml"] = render_feed(posts)

    if not args.dry_run:
        for target, content in pages.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

    removed = prune_orphans(posts, args.dry_run)
    if removed:
        print(f"\n公開対象から外れたので news/ から削除: {', '.join(removed)}")

    print()
    failures = []
    for ok, msg in (update_top_page(posts, args.dry_run),
                    update_sitemap(posts, args.dry_run),
                    update_llms(posts, args.dry_run)):
        print(("" if ok else "【失敗】") + msg)
        if not ok:
            failures.append(msg)

    if args.dry_run:
        print("\n--dry-run のため書き込みはしていない（組み立ては通った）")
        return 1 if failures else 0

    print(f"\n生成しました: news/index.html ＋ 記事{len(posts)}本 ＋ feed.xml")

    ok, out = run_check()
    print("\n--- 公開前チェック（_check.py） ---")
    print(out)
    if not ok:
        failures.append("_check.py がエラーを出した")

    if failures:
        print("\n未完了のものがあります。上を見て直してから公開する。", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
