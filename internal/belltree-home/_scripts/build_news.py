#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
belltree1102.com — お知らせ・健康コラムの生成（手動実行）

_articles/*.md を読んで、
  news/index.html          一覧ページ
  news/<slug>/index.html   記事ページ
  news/feed.xml            RSS
を書き出す。あわせて sitemap.xml・llms.txt・トップページの最新3件枠も更新する。

このサイトはビルドツールを入れない方針なので、CI では動かさない。
手元でこのスクリプトを走らせ、出来た HTML をコミットして公開する。

使い方:
    python _scripts/build_news.py --dry-run   何が作られるか見るだけ
    python _scripts/build_news.py             生成する

記事の書き方（_articles/2026-09-01-example.md）:
    ---
    title: 記事の見出し
    description: 一覧とSNSカードに出る一文
    date: 2026-09-01
    category: 健康コラム
    source: べるつりー通信 2026年9月号     ← 任意（紙面の再録なら書く）
    draft: false
    ---

    本文（Markdown）
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

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


def parse_front_matter(raw: str) -> tuple[dict, str]:
    """YAMLライブラリを使わずに済む範囲の簡易フロントマター解析。"""
    m = FM_RE.match(raw)
    if not m:
        raise ValueError("フロントマター（--- で囲んだ冒頭）がありません")
    meta: dict = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            meta[key] = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        elif value.lower() in ("true", "false"):
            meta[key] = value.lower() == "true"
        else:
            meta[key] = value.strip("\"'")
    return meta, m.group(2)


def load_articles() -> list[dict]:
    if not ARTICLES_DIR.exists():
        return []
    posts = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        if meta.get("draft"):
            continue
        for required in ("title", "date"):
            if not meta.get(required):
                raise ValueError(f"{path.name}: {required} が空です")
        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        category = meta.get("category") or DEFAULT_CATEGORY
        if category not in CATEGORIES:
            raise ValueError(f"{path.name}: 未定義のカテゴリ「{category}」")
        html_body = md_lib.markdown(body, extensions=["extra", "sane_lists"])
        posts.append(
            {
                "slug": slug,
                "title": meta["title"],
                "description": meta.get("description", ""),
                "date": str(meta["date"]),
                "category": category,
                "source": meta.get("source", ""),
                "tags": meta.get("tags", []),
                # 同じ日付の記事の並び順。大きいほど前に出る（既定0）
                "order": int(meta.get("order", 0) or 0),
                "body": html_body,
                "path": path,
            }
        )
    posts.sort(key=lambda p: (p["date"], p["order"], p["slug"]), reverse=True)
    return posts


def jp_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.year}年{d.month}月{d.day}日"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# --------------------------------------------------------------------------
# 共通パーツ（ヘッダー・フッター・CSS）
# --------------------------------------------------------------------------

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

  @media (max-width: 1000px) { .main-nav, .header-phone { display: none; } .header-inner { gap: 12px; } }
  @media (max-width: 760px) { .footer-top { grid-template-columns: 1fr 1fr; } .approach-final { padding: 26px 22px; } }
  @media (max-width: 480px) { .footer-top { grid-template-columns: 1fr; } .info-bar .wrap { font-size: 11px; gap: 6px 12px; } }

  /* ハンバーガー・ドロワー */
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
  @media (max-width: 1000px) { .nav-toggle { display: flex; } }
  @media (max-width: 480px) { .header-inner { gap: 10px; } .brand-name { font-size: 17px; } .brand-name .jp { font-size: 12px; } .header-cta { gap: 10px; } .btn-sm { height: 38px; padding: 0 15px; font-size: 12px; } }

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
  /* 直下の見出しだけ。カード内の h2 まで中央寄せにしないこと */
  .related > h2 { font-family: var(--bt-font-serif); font-weight: 600; font-size: 19px; color: var(--bt-primary); text-align: center; margin: 0 0 26px; }
  /* 関連が2本以下のとき、3列グリッドの左寄せにならないよう中央に寄せる */
  .related .news-grid { grid-template-columns: repeat(auto-fit, minmax(240px, 318px)); justify-content: center; }

  @media (max-width: 900px) { .news-grid { grid-template-columns: repeat(2, 1fr); } }
  @media (max-width: 600px) { .news-grid { grid-template-columns: 1fr; } .article-body { padding: 28px 22px; } .article-head { padding-top: 36px; } }
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


def nav_html(prefix: str) -> str:
    items = [
        ("ホーム", f"{prefix}index.html"),
        ("お悩み別解決策", f"{prefix}index.html#concerns"),
        ("サービス一覧", f"{prefix}index.html#model"),
        ("改善事例", f"{prefix}index.html#cases"),
        ("お知らせ", f"{prefix}news/index.html"),
        ("スタッフ紹介", f"{prefix}team/index.html"),
        ("会社概要", f"{prefix}about/index.html"),
    ]
    links = "\n".join(f'      <a href="{h}">{l}</a>' for l, h in items)
    return f'    <nav class="main-nav">\n{links}\n    </nav>'


PHONE_SVG = (
    '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.4" '
    'stroke-linecap="round" stroke-linejoin="round"><path d="M14 10 H 20 L 23 17 L 19 20 '
    'C 21 25 23 27 28 29 L 31 25 L 38 28 V 34 C 38 36 36 38 34 38 C 22 38 10 26 10 14 C 10 12 12 10 14 10 Z"/></svg>'
)


def header_html(prefix: str) -> str:
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{prefix}index.html" aria-label="べるつりーグループ">
      <img src="{prefix}assets/belltree-mark.svg" alt="" />
      <span class="brand-name">BellTree<span class="sep">／</span><span class="jp">べるつりー</span></span>
    </a>
{nav_html(prefix)}
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


def head_html(prefix: str, title: str, description: str, canonical: str, extra: str = "") -> str:
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
<meta property="og:type" content="article" />
<meta property="og:image" content="{SITE}/assets/img/og/og-default.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="{SITE}/assets/img/og/og-default.jpg" />
<meta property="og:locale" content="ja_JP" />
<link rel="alternate" type="application/rss+xml" title="べるつりー お知らせ" href="{SITE}/news/feed.xml" />
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
      <h2>{esc(post['title'])}</h2>
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
    if not posts:
        cards = ""

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "お知らせ・健康コラム", "item": f"{SITE}/news/"},
        ],
    }, ensure_ascii=False, indent=2)

    extra = f'<script type="application/ld+json">\n{breadcrumb_ld}\n</script>'

    return (
        head_html(
            prefix,
            "お知らせ・健康コラム｜株式会社べるつりー",
            "べるつりーグループからのお知らせと、毎月お配りしている「べるつりー通信」から生まれた健康コラム。季節ごとの体調の注意点、介護保険や医療保険のしくみ、地域での取り組みをご紹介します。",
            f"{SITE}/news/",
            extra,
        )
        + header_html(prefix)
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

<section class="sec-pad">
  <div class="wrap">
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
        rest = [p for p in posts if p["slug"] != post["slug"] and p not in related]
        related += rest[: 3 - len(related)]

    article_ld = json.dumps({
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
    }, ensure_ascii=False, indent=2)

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "お知らせ・健康コラム", "item": f"{SITE}/news/"},
            {"@type": "ListItem", "position": 3, "name": post["title"], "item": f"{SITE}/news/{post['slug']}/"},
        ],
    }, ensure_ascii=False, indent=2)

    extra = (
        f'<script type="application/ld+json">\n{article_ld}\n</script>\n'
        f'<script type="application/ld+json">\n{breadcrumb_ld}\n</script>'
    )

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
            extra,
        )
        + header_html(prefix)
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
      <h1>{esc(post['title'])}</h1>
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
    now = datetime.now(JST).strftime("%a, %d %b %Y %H:%M:%S +0900")
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
# --------------------------------------------------------------------------

TOP_START = "<!-- NEWS_LATEST_START -->"
TOP_END = "<!-- NEWS_LATEST_END -->"


def update_top_page(posts: list[dict], dry: bool) -> str:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if TOP_START not in text or TOP_END not in text:
        return "トップページに差し込み口（NEWS_LATEST マーカー）がないため未更新"
    latest = posts[:3]
    cards = "\n".join(card_html(p, "news/") for p in latest)
    block = f"""{TOP_START}
<section class="band-base sec-pad" id="news" style="border-top:1px solid var(--bt-line-soft)">
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
        return "トップページ: 変更なし"
    if not dry:
        path.write_text(new_text, encoding="utf-8")
    return f"トップページ: 最新{len(latest)}件を更新"


def update_sitemap(posts: list[dict], dry: bool) -> str:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    # 既存の /news/ 行をいったん全部落としてから入れ直す（重複防止）
    text = re.sub(r"[ \t]*<url><loc>https://belltree1102\.com/news/[^<]*</loc>.*?</url>\n", "", text)
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
    return f"sitemap.xml: {len(posts) + 1} 件のURLを登録"


LLMS_START = "## お知らせ・健康コラム"


def update_llms(posts: list[dict], dry: bool) -> str:
    path = ROOT / "llms.txt"
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
        text = re.sub(
            re.escape(LLMS_START) + r".*?(?=\n## |\Z)", lambda _: block.rstrip("\n") + "\n", text, flags=re.S
        )
    else:
        text = text.rstrip("\n") + "\n\n" + block
    if not dry:
        path.write_text(text, encoding="utf-8")
    return f"llms.txt: {min(len(posts), 20)} 件を掲載"


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="書き出さずに結果だけ表示")
    args = ap.parse_args()

    posts = load_articles()
    if not posts:
        print("公開できる記事が _articles/ にありません（draft: true は除外されます）")
        return 1

    print(f"記事 {len(posts)} 件を読み込みました")
    for p in posts:
        print(f"  {p['date']}  [{p['category']}]  {p['title']}  → news/{p['slug']}/")

    if not args.dry_run:
        NEWS_DIR.mkdir(exist_ok=True)
        (NEWS_DIR / "index.html").write_text(render_index(posts), encoding="utf-8")
        for p in posts:
            d = NEWS_DIR / p["slug"]
            d.mkdir(exist_ok=True)
            (d / "index.html").write_text(render_article(p, posts), encoding="utf-8")
        (NEWS_DIR / "feed.xml").write_text(render_feed(posts), encoding="utf-8")

    print()
    print(update_top_page(posts, args.dry_run))
    print(update_sitemap(posts, args.dry_run))
    print(update_llms(posts, args.dry_run))

    if args.dry_run:
        print("\n--dry-run のため書き込みはしていない")
    else:
        print(f"\n生成しました: news/index.html ＋ 記事{len(posts)}本 ＋ feed.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
