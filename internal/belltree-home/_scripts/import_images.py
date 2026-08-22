#!/usr/bin/env python3
"""記事に使う画像を、紙面の素材から取り込む道具。

べるつりー通信の写真・イラストは `.company/design/<号のフォルダ>/` にある
1536x1024 の PNG（数MB）が正本。そのままウェブに置くと重すぎるので、
この道具で幅を詰めて WebP に焼き直し、`assets/img/news/<slug>/` に置く。

  # 写真をまとめて取り込む
  python _scripts/import_images.py akibate-yobo "<通信9月号>/photos/photo-02-aircon.png"

  # そのうち1枚を、SNS共有用のカード画像（1200x630）にもする
  python _scripts/import_images.py akibate-yobo "<...>/photo-01-cold-drink.png" --ogp

  # ツボ図に赤い点を焼き込む（位置は紙面と同じ％で指定する）
  python _scripts/import_images.py toyo-igaku-natsu-tsukare "<...>/body-01-leg-outer.png" \
      --name tsubo-01-ashisanri --dot 57,32 --width 600

覚えておくこと:

- **元の PNG はリポジトリに入れない**。正本は OneDrive の制作フォルダ。
  ここに置くのは軽くした WebP だけ（写真1枚 2〜3MB → 100KB 前後）。
- 赤い点の位置は紙面の組版（`_render/templates/.../Tsushin*.dc.html` の
  `left:○%;top:○%`）から写す。目分量で置かない。
- 出来上がりはいつも同じバイト列になる（同じ入力なら git が汚れない）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("Pillow が要ります: py -m pip install Pillow", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = ROOT / "assets" / "img" / "news"
OG_ROOT = ROOT / "assets" / "img" / "og"

# 紙面の赤点と同じ見た目（11px / 112px ＝ 画像の幅の約9.8%、白フチ付き）
DOT_COLOR = (224, 58, 32, 255)
DOT_RING = (255, 255, 255, 235)
DOT_RATIO = 0.098
# SNSカード画像の地色（サイトの紙色に合わせる）
PAPER = (250, 246, 239)

SLUG_OK = set("abcdefghijklmnopqrstuvwxyz0123456789-")


def kb(path: Path) -> str:
    return f"{path.stat().st_size / 1024:.0f} KB"


def draw_dot(im: Image.Image, x_pct: float, y_pct: float) -> Image.Image:
    """紙面と同じ位置に赤い点を焼き込む。"""
    from PIL import ImageDraw

    im = im.convert("RGBA")
    w, h = im.size
    r = w * DOT_RATIO / 2
    cx, cy = w * x_pct / 100, h * y_pct / 100
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ring = r * 1.36
    d.ellipse((cx - ring, cy - ring, cx + ring, cy + ring), fill=DOT_RING)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=DOT_COLOR)
    im.alpha_composite(layer)
    return im


def make_ogp(src: Image.Image, out: Path, transparent: bool) -> None:
    """SNS・LINEに貼ったときのカード画像（1200x630）。

    写真は上寄りで切り抜く（顔が切れないように）。透過イラストは切り抜かず、
    紙色の地の中央に置く（引き伸ばすとぼやけるため）。
    """
    target_w, target_h = 1200, 630
    canvas = Image.new("RGB", (target_w, target_h), PAPER)
    if transparent:
        im = src.convert("RGBA")
        scale = min(target_w * 0.72 / im.width, target_h * 0.86 / im.height, 1.0)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        canvas.paste(im, ((target_w - im.width) // 2, (target_h - im.height) // 2), im)
    else:
        im = src.convert("RGB")
        scale = max(target_w / im.width, target_h / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left = (im.width - target_w) // 2
        top = max(0, round((im.height - target_h) * 0.4))
        canvas = im.crop((left, top, left + target_w, top + target_h))
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "JPEG", quality=84, optimize=True, progressive=True)
    print(f"  OGP  {out.relative_to(ROOT)}  1200x630  {kb(out)}")


def main() -> int:
    ap = argparse.ArgumentParser(description="記事用の画像を取り込む（WebP化・軽量化）")
    ap.add_argument("slug", help="記事のスラッグ（news/<slug>/ と同じ）")
    ap.add_argument("src", nargs="+", help="元画像（制作フォルダの PNG / JPG）")
    ap.add_argument("--width", type=int, default=0,
                    help="長辺ではなく幅の上限。既定は写真1400・透過イラスト600。元より大きくはしない")
    ap.add_argument("--name", default="", help="出力の名前（拡張子なし）。省略すると元のファイル名")
    ap.add_argument("--dot", default="", help="赤い点を焼く位置「左%%,上%%」（紙面の組版から写す）")
    ap.add_argument("--ogp", action="store_true", help="1枚目から SNS カード画像も作る")
    ap.add_argument("--quality", type=int, default=0, help="WebPの品質（既定 写真82・イラスト88）")
    args = ap.parse_args()

    slug = args.slug.strip()
    if not slug or set(slug) - SLUG_OK:
        print(f"slug「{slug}」は使えません。半角英小文字・数字・ハイフンだけ", file=sys.stderr)
        return 1
    if args.name and len(args.src) > 1:
        print("--name は元画像1枚のときだけ使えます", file=sys.stderr)
        return 1

    dot = None
    if args.dot:
        try:
            x, y = (float(v) for v in args.dot.split(","))
            dot = (x, y)
        except ValueError:
            print("--dot は「57,32」のように 左%,上% で書く", file=sys.stderr)
            return 1

    out_dir = OUT_ROOT / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    for i, raw in enumerate(args.src):
        src = Path(raw)
        if not src.exists():
            print(f"元画像がありません: {src}", file=sys.stderr)
            return 1
        im = Image.open(src)
        transparent = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)

        if args.ogp and i == 0:
            make_ogp(im, OG_ROOT / f"og-news-{slug}.jpg", transparent)

        if dot:
            im = draw_dot(im, *dot)
            transparent = True

        width = args.width or (600 if transparent else 1400)
        width = min(width, im.width)
        if width < im.width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

        im = im.convert("RGBA" if transparent else "RGB")
        name = args.name or src.stem
        if set(name.lower()) - SLUG_OK - {"_", "."}:
            print(f"出力名「{name}」は半角英小文字・数字・ハイフンで（--name で付け直す）", file=sys.stderr)
            return 1
        out = out_dir / f"{name}.webp"
        im.save(out, "WEBP", quality=args.quality or (88 if transparent else 82), method=6)
        print(f"  {out.relative_to(ROOT)}  {im.width}x{im.height}  {kb(out)}")
        lines.append(f"![（ここに説明を書く）]({out.name})")

    print("\n記事（_articles/*.md）の本文に貼る行:")
    for line in lines:
        print("  " + line)
    print('  ※ 説明（alt）は写っているものを書く。図の名前を出したいときは '
          '![説明](file.webp "図の名前") のように後ろに足すとキャプションになる。')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
