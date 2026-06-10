# -*- coding: utf-8 -*-
# 2026-06-10: L素材シート5枚（膝痛/転倒/フレイル/腰痛/介護開始）を
# 2x3分割 → 内側5-95%トリム → bbox精密 → 純白透過 → 800x533 統一
import shutil
from pathlib import Path
from PIL import Image

DL = Path(r"C:\Users\sss_1\Downloads")
REPO = Path(r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー")
RAW_DIR = REPO / "images/materials/decoration/L/_raw"
TW, TH = 800, 533

SHEETS = {
    "knee-pain":       "ChatGPT Image 2026年6月10日 14_39_22 (1).png",
    "fall-risk":       "ChatGPT Image 2026年6月10日 14_39_22 (2).png",
    "frailty":         "ChatGPT Image 2026年6月10日 14_39_22 (3).png",
    "lower-back-pain": "ChatGPT Image 2026年6月10日 14_39_22 (4).png",
    "home-care-start": "ChatGPT Image 2026年6月10日 14_39_22 (5).png",
}

def trim(crop, white_th=240, pad=20):
    px = crop.load(); w, h = crop.size
    mx, my, Mx, My = w, h, 0, 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if not (r > white_th and g > white_th and b > white_th):
                if x < mx: mx = x
                if y < my: my = y
                if x > Mx: Mx = x
                if y > My: My = y
    if mx >= Mx or my >= My:
        return crop
    mx = max(0, mx - pad); my = max(0, my - pad)
    Mx = min(w, Mx + pad); My = min(h, My + pad)
    return crop.crop((mx, my, Mx, My))

for slug, fname in SHEETS.items():
    src = DL / fname
    raw = RAW_DIR / f"{slug}-objects-L-raw.png"
    outdir = REPO / f"images/materials/decoration/L/{slug}"
    outdir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, raw)

    im = Image.open(raw).convert("RGBA")
    W, H = im.size
    COLS, ROWS = 2, 3
    cw, ch = W // COLS, H // ROWS
    idx = 0
    for row in range(ROWS):
        for col in range(COLS):
            idx += 1
            x0, y0 = col * cw, row * ch
            x1 = (col + 1) * cw if col < COLS - 1 else W
            y1 = (row + 1) * ch if row < ROWS - 1 else H
            cell = im.crop((x0, y0, x1, y1))
            cw2, ch2 = cell.size
            cell = cell.crop((int(cw2 * 0.05), int(ch2 * 0.05), int(cw2 * 0.95), int(ch2 * 0.95)))
            cell = trim(cell)
            px = cell.load(); w, h = cell.size
            for y in range(h):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if r > 245 and g > 245 and b > 245:
                        px[x, y] = (r, g, b, 0)
            iw, ih = cell.size
            ratio = min(TW / iw, TH / ih) * 0.92
            nw, nh = int(iw * ratio), int(ih * ratio)
            resized = cell.resize((nw, nh), Image.LANCZOS)
            canvas = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
            canvas.paste(resized, ((TW - nw) // 2, (TH - nh) // 2), resized)
            canvas.save(outdir / f"{slug}-l-{idx:02d}.png")
    print(f"[done] {slug}: 6 cells -> {outdir.relative_to(REPO)}")
