#!/usr/bin/env python3
"""トップページの「ふだんの様子」（Instagramの最近の投稿）を作る。

Instagram の公式埋め込みは使わない。理由は3つ。
  ① 外部のJavaScriptとCookieが入る（同意まわりと表示速度の負担）
  ② 見た目をこちらで決められない
  ③ 投稿が止まると「止まっていること」がそのまま画面に出続ける

代わりに Graph API で最近の投稿を取り、**絵をこちらに持ってきて**静的なHTMLとして
書き出す。build_news.py と同じ考え方（手で走らせる・生成物をコミットする）。

  python _scripts/build_instagram.py            # 直近6か月・最大6件
  python _scripts/build_instagram.py --dry-run  # 取ってくるだけ（書き換えない）
  python _scripts/build_instagram.py --months 12 --max 3

**直近6か月の投稿が3件に満たなければ、枠ごと消える。** 古い投稿を並べて「更新が
止まっている会社」に見せないため、また1枚だけ並んで間が抜けるのを避けるため
（トップのお知らせ帯と同じ考え方）。件数は --min で変えられる。

認証は OneDrive の `.secrets/bellmfit_instagram.json`。リポジトリには入れない。
トークンの再交換は月次の自動処理 #17（MonthlyInstagram）が面倒を見ている。
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("Pillow が要ります: py -m pip install Pillow", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
SECRETS = Path.home() / "OneDrive" / "ドキュメント" / ".secrets" / "bellmfit_instagram.json"
GRAPH = "https://graph.facebook.com/v25.0"
IMG_DIR = ROOT / "assets" / "img" / "instagram"
IMG_URL = "assets/img/instagram"
PROFILE = "https://www.instagram.com/bellmfit/"

START = "<!-- INSTAGRAM_START -->"
END = "<!-- INSTAGRAM_END -->"

# キャプション1行目がこれだけなら「文字なし」とみなして次の行を見る
JUNK_LINE = re.compile(r"^[\s・.。…‥\-–—~〜*＊#＃･]*$")
HASHTAG_ONLY = re.compile(r"^\s*(#\S+\s*)+$")

PLAY_SVG = ('<svg class="ig-play" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
            '<circle cx="12" cy="12" r="11" fill="rgba(0,0,0,0.45)"/>'
            '<path d="M9.5 7.8v8.4L17 12z" fill="#fff"/></svg>')


def api_get(path: str, params: dict) -> dict:
    url = f"{GRAPH}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def jp_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.year}年{d.month}月{d.day}日"


def headline(caption: str) -> str:
    """カードに出す1行をキャプションから拾う。記号だけ・ハッシュタグだけの行は飛ばす。"""
    for line in (caption or "").split("\n"):
        line = line.strip()
        if not line or JUNK_LINE.match(line) or HASHTAG_ONLY.match(line):
            continue
        line = re.sub(r"\s*#\S+", "", line).strip()
        if not line:
            continue
        return line[:42] + ("…" if len(line) > 42 else "")
    return ""


def fetch(limit: int) -> tuple[dict, list[dict]]:
    if not SECRETS.exists():
        sys.exit(f"認証ファイルがありません: {SECRETS}")
    sec = json.loads(SECRETS.read_text(encoding="utf-8"))
    token, ig = sec["access_token"], sec["ig_user_id"]
    account = api_get(ig, {"fields": "username,followers_count,media_count", "access_token": token})
    if account.get("username") is None:
        sys.exit(f"[FAIL] アカウント情報が取れませんでした（応答: {str(account)[:300]}）")
    media = api_get(f"{ig}/media", {
        "fields": "id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp",
        "limit": limit, "access_token": token,
    }).get("data", [])
    # 空のまま書き出すと、壊れたことに誰も気づけない（月次#17で実際にやった）
    if not media:
        sys.exit("[FAIL] 投稿が1件も取れませんでした")
    for m in media:
        if not m.get("media_url") and not m.get("thumbnail_url") and m.get("media_type") == "CAROUSEL_ALBUM":
            kids = api_get(f"{m['id']}/children",
                           {"fields": "media_url,thumbnail_url", "access_token": token}).get("data", [])
            if kids:
                m["media_url"] = kids[0].get("media_url")
                m["thumbnail_url"] = kids[0].get("thumbnail_url")
    return account, media


def save_square(url: str, out: Path, size: int = 640) -> tuple[int, int]:
    """投稿の絵を正方形に切って WebP で置く。

    Instagram が返す画像URLは数日で切れるので、リンクで参照せず必ずこちらに持ってくる。
    """
    with urllib.request.urlopen(url, timeout=60) as r:
        im = Image.open(io.BytesIO(r.read())).convert("RGB")
    side = min(im.size)
    left = (im.width - side) // 2
    top = max(0, round((im.height - side) * 0.35))  # 人が入るので少し上寄りで抜く
    im = im.crop((left, top, left + side, top + side))
    if side > size:
        im = im.resize((size, size), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "WEBP", quality=80, method=6)
    return im.size


def card_html(p: dict) -> str:
    play = PLAY_SVG if p["is_video"] else ""
    cap = f'\n        <p class="ig-cap">{esc(p["headline"])}</p>' if p["headline"] else ""
    click = ("onclick=\"if(window.gtag){gtag('event','instagram_click',"
             "{method:'instagram',page:'top'});}\"")
    return (f'      <a class="ig-card" href="{esc(p["permalink"])}" target="_blank"'
            f' rel="noopener noreferrer" {click}>\n'
            f'        <div class="ig-thumb"><img src="{IMG_URL}/{p["file"]}" width="{p["w"]}"'
            f' height="{p["h"]}" alt="" loading="lazy" decoding="async" />{play}</div>{cap}\n'
            f'        <time datetime="{p["date"]}">{jp_date(p["date"])}</time>\n'
            f'      </a>')


def build_block(posts: list[dict]) -> str:
    if not posts:
        # 直近に投稿が無い月は枠ごと消える
        return f"{START}\n{END}"
    cards = "\n".join(card_html(p) for p in posts)
    more_click = ("onclick=\"if(window.gtag){gtag('event','instagram_click',"
                  "{method:'instagram',page:'top-more'});}\"")
    return f"""{START}
<section class="band-paper sec-pad" id="instagram">
  <div class="wrap">
    <div class="news-sec-head">
      <span class="news-eyebrow">Instagram</span>
      <h2>ふだんの様子</h2>
      <p>べるフィット町田のインスタグラムから、最近の投稿をお届けしています。</p>
    </div>
    <div class="ig-grid">
{cards}
    </div>
    <div class="news-actions">
      <a class="btn btn--ghost" href="{PROFILE}" target="_blank" rel="noopener noreferrer" {more_click}>インスタグラムを見る</a>
    </div>
  </div>
</section>
{END}"""


def main() -> int:
    ap = argparse.ArgumentParser(description="トップの Instagram 枠を作り直す")
    ap.add_argument("--months", type=int, default=6, help="これより古い投稿は出さない（既定6か月）")
    ap.add_argument("--max", type=int, default=6, help="並べる最大件数（既定6）")
    ap.add_argument("--min", type=int, default=3,
                    help="これを下回る件数なら枠を出さない（既定3。1枚だけ並ぶ間の抜けた見え方を避ける）")
    ap.add_argument("--limit", type=int, default=25, help="APIから取ってくる件数")
    ap.add_argument("--dry-run", action="store_true", help="取ってくるだけ。ファイルは書き換えない")
    args = ap.parse_args()

    account, media = fetch(args.limit)
    cutoff = dt.date.today() - dt.timedelta(days=args.months * 30)
    recent = [m for m in media if dt.date.fromisoformat(m["timestamp"][:10]) >= cutoff][: args.max]
    print(f"@{account.get('username')}  フォロワー {account.get('followers_count')} / "
          f"投稿 {account.get('media_count')} / 取得 {len(media)}件 "
          f"→ 直近{args.months}か月に {len(recent)}件（{args.min}件から掲出）")
    if len(recent) < args.min:
        print(f"  → まだ{args.min}件に届かないので、枠は出さない")
        recent = []
    for m in media[:8]:
        mark = "○" if m in recent else "　"
        print(f"  {mark} {m['timestamp'][:10]} "
              f"{m.get('media_product_type', m.get('media_type'))}  {headline(m.get('caption', ''))}")
    if args.dry_run:
        print("[DRY-RUN] 書き換えていません")
        return 0

    posts = []
    for m in recent:
        src = m.get("thumbnail_url") or m.get("media_url")
        if not src:
            print(f"  ! 絵が取れないので飛ばした: {m['permalink']}")
            continue
        name = f"{m['timestamp'][:10].replace('-', '')}-{m['id'][-8:]}.webp"
        w, h = save_square(src, IMG_DIR / name)
        posts.append({
            "file": name, "w": w, "h": h, "permalink": m["permalink"],
            "date": m["timestamp"][:10], "headline": headline(m.get("caption", "")),
            "is_video": (m.get("media_type") == "VIDEO" or m.get("media_product_type") == "REELS"),
        })

    keep = {p["file"] for p in posts}
    if IMG_DIR.exists():
        for f in sorted(IMG_DIR.glob("*.webp")):
            if f.name not in keep:
                f.unlink()
                print(f"  片付け: {f.name}")

    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("トップページに差し込み口（INSTAGRAM マーカー）がありません", file=sys.stderr)
        return 1
    new = re.sub(re.escape(START) + r".*?" + re.escape(END),
                 lambda _: build_block(posts), text, flags=re.S)
    if new == text:
        print("トップページ: 変更なし")
    else:
        path.write_text(new, encoding="utf-8")
        print(f"トップページ: {len(posts)}件を掲出" if posts
              else "トップページ: 直近の投稿が足りないので枠を消した")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
