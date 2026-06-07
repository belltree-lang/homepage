"""
L sheet (2x3=6) を等分割→内側トリム→bbox→透過→800x533コンテイン正規化する。
slug を引数で受け取り、images/materials/decoration/L/_raw/<slug>-objects-L-raw.png を読み、
images/materials/decoration/L/<slug>/<slug>-l-01.png ~ -06.png を吐く。
"""
import sys
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー")
TW, TH = 800, 533
COLS, ROWS = 2, 3
INNER_LO, INNER_HI = 0.0, 1.0
WHITE_THRESHOLD = 240
PAD = 20
SCALE = 0.92

def white_to_alpha(img: Image.Image, thr=WHITE_THRESHOLD) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= thr and g >= thr and b >= thr:
                px[x, y] = (r, g, b, 0)
    return img

def tight_bbox(img: Image.Image, pad=PAD) -> Image.Image:
    bg = Image.new("RGBA", img.size, (255, 255, 255, 0))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox is None:
        return img
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(img.size[0], x1 + pad)
    y1 = min(img.size[1], y1 + pad)
    return img.crop((x0, y0, x1, y1))

def contain_resize(img: Image.Image, tw=TW, th=TH, scale=SCALE) -> Image.Image:
    iw, ih = img.size
    avail_w, avail_h = tw * scale, th * scale
    ratio = min(avail_w / iw, avail_h / ih)
    new_w = int(iw * ratio)
    new_h = int(ih * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (tw, th), (255, 255, 255, 0))
    cx = (tw - new_w) // 2
    cy = (th - new_h) // 2
    canvas.paste(img, (cx, cy), img)
    return canvas

def process(slug: str):
    raw = ROOT / "images" / "materials" / "decoration" / "L" / "_raw" / f"{slug}-objects-L-raw.png"
    outdir = ROOT / "images" / "materials" / "decoration" / "L" / slug
    outdir.mkdir(parents=True, exist_ok=True)

    img = Image.open(raw).convert("RGB")
    W, H = img.size
    cell_w = W / COLS
    cell_h = H / ROWS

    n = 0
    for r in range(ROWS):
        for c in range(COLS):
            n += 1
            x0 = c * cell_w
            y0 = r * cell_h
            x1 = (c + 1) * cell_w
            y1 = (r + 1) * cell_h
            cw = x1 - x0
            ch = y1 - y0
            ix0 = int(x0 + cw * INNER_LO)
            iy0 = int(y0 + ch * INNER_LO)
            ix1 = int(x0 + cw * INNER_HI)
            iy1 = int(y0 + ch * INNER_HI)
            cell = img.crop((ix0, iy0, ix1, iy1))
            cell_rgba = white_to_alpha(cell)
            cell_cropped = tight_bbox(cell_rgba)
            normalized = contain_resize(cell_cropped)
            out = outdir / f"{slug}-l-{n:02d}.png"
            normalized.save(out, "PNG", optimize=True)
            print(f"  {out.name}: {normalized.size}")
    print(f"[{slug}] done → {outdir}")

if __name__ == "__main__":
    for slug in sys.argv[1:]:
        process(slug)
