"""グリッド画像を個別素材に分割（純白→透過処理付き）

使い方:
  python scripts/split_material_grid.py <input.png> --out <out_dir> --rows R --cols C --prefix NAME [--margin PCT] [--no-transparent] [--threshold T]

例:
  python scripts/split_material_grid.py "C:/Users/sss_1/Downloads/印章L.png" \
    --out "images/materials/seals/L" \
    --rows 3 --cols 2 \
    --prefix seal-l \
    --margin 8
"""
import argparse
from pathlib import Path
from PIL import Image
import numpy as np
try:
    from scipy import ndimage
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def split_grid(input_path: Path, output_dir: Path, rows: int, cols: int,
               prefix: str, transparent: bool = True, white_threshold: int = 240,
               margin_pct: int = 10, tight: bool = True, padding: int = 24,
               overlap_pct: int = 15, group_distance: float = 1.3,
               group_area_min: float = 0.25, group_area_max: float = 4.0) -> int:
    """
    1. 外周マージン除去 → 残りを rows × cols で粗分割
    2. 各セルを overlap_pct % だけ広げてサンプル（隣接セルの素材まで掴まないよう中心寄せ）
    3. 純白を透過化
    4. tight=True の場合、透過じゃないピクセルの bbox を取得して padding を残して再 crop
       → 「絶妙にずれている」を解消し、素材ごとに中心揃え
    """
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    mx = int(w * margin_pct / 100)
    my = int(h * margin_pct / 100)
    inner = img.crop((mx, my, w - mx, h - my))
    iw, ih = inner.size

    cell_w = iw // cols
    cell_h = ih // rows
    # overlap で粗セルを少し広げてサンプル（中心ピクセルを取りこぼさない）
    over_w = int(cell_w * overlap_pct / 100)
    over_h = int(cell_h * overlap_pct / 100)

    output_dir.mkdir(parents=True, exist_ok=True)

    saved = 0
    for r in range(rows):
        for c in range(cols):
            saved += 1
            cx = c * cell_w + cell_w // 2
            cy = r * cell_h + cell_h // 2
            half_w = cell_w // 2 + over_w
            half_h = cell_h // 2 + over_h
            left = max(0, cx - half_w)
            top = max(0, cy - half_h)
            right = min(iw, cx + half_w)
            bottom = min(ih, cy + half_h)
            cell = inner.crop((left, top, right, bottom))

            if transparent:
                arr = np.array(cell)
                white_mask = (
                    (arr[..., 0] >= white_threshold)
                    & (arr[..., 1] >= white_threshold)
                    & (arr[..., 2] >= white_threshold)
                )
                arr[..., 3] = np.where(white_mask, 0, 255)
                cell = Image.fromarray(arr)

                if tight:
                    cw, ch = cell.size
                    cx_local, cy_local = cw // 2, ch // 2

                    if HAS_SCIPY:
                        # 連結成分解析：中央セル内の素材だけを抽出
                        mask = arr[..., 3] > 0
                        labeled, num = ndimage.label(mask)
                        if num > 0:
                            # 中心ピクセルのラベル
                            center_label = labeled[cy_local, cx_local]
                            if center_label == 0:
                                # 中心が透過 → 中央に最も近いコンポーネントを採用
                                objects = ndimage.find_objects(labeled)
                                best_label = None
                                best_dist = float("inf")
                                for i, obj in enumerate(objects, start=1):
                                    if obj is None:
                                        continue
                                    ys, xs = obj
                                    # 面積で minor noise を除外
                                    area = (ys.stop - ys.start) * (xs.stop - xs.start)
                                    if area < 100:
                                        continue
                                    ocy = (ys.start + ys.stop) / 2
                                    ocx = (xs.start + xs.stop) / 2
                                    d = (ocx - cx_local) ** 2 + (ocy - cy_local) ** 2
                                    if d < best_dist:
                                        best_dist = d
                                        best_label = i
                                center_label = best_label

                            if center_label:
                                # main コンポーネントの座標
                                main_pixels = labeled == center_label
                                ys_idx, xs_idx = np.where(main_pixels)
                                if len(ys_idx) > 0:
                                    main_t = int(ys_idx.min())
                                    main_b = int(ys_idx.max()) + 1
                                    main_l = int(xs_idx.min())
                                    main_r = int(xs_idx.max()) + 1
                                    main_area = (main_b - main_t) * (main_r - main_l)
                                    main_size = max(main_r - main_l, main_b - main_t)
                                    main_cx_obj = (main_l + main_r) / 2
                                    main_cy_obj = (main_t + main_b) / 2

                                    # keep_mask: main コンポーネント + 近傍同サイズコンポーネント
                                    keep_mask = main_pixels.copy()
                                    objects = ndimage.find_objects(labeled)
                                    for i, obj in enumerate(objects, start=1):
                                        if i == center_label or obj is None:
                                            continue
                                        ys2, xs2 = obj
                                        area2 = (ys2.stop - ys2.start) * (xs2.stop - xs2.start)
                                        if area2 < 100:
                                            continue
                                        cy2 = (ys2.start + ys2.stop) / 2
                                        cx2 = (xs2.start + xs2.stop) / 2
                                        dist = ((cy2 - main_cy_obj) ** 2 + (cx2 - main_cx_obj) ** 2) ** 0.5
                                        area_ratio = area2 / main_area
                                        if dist < main_size * group_distance and group_area_min < area_ratio < group_area_max:
                                            keep_mask = keep_mask | (labeled == i)

                                    # keep_mask 以外を完全透明にする
                                    arr_keep = arr.copy()
                                    arr_keep[..., 3] = np.where(keep_mask, 255, 0)
                                    cell = Image.fromarray(arr_keep)

                                    # bbox は keep_mask のみで計算
                                    ys_keep, xs_keep = np.where(keep_mask)
                                    union_t = int(ys_keep.min())
                                    union_b = int(ys_keep.max()) + 1
                                    union_l = int(xs_keep.min())
                                    union_r = int(xs_keep.max()) + 1

                                    # padding
                                    l = max(0, union_l - padding)
                                    t = max(0, union_t - padding)
                                    r2 = min(cw, union_r + padding)
                                    b = min(ch, union_b + padding)
                                    cell = cell.crop((l, t, r2, b))
                    else:
                        # scipy なしの fallback
                        bbox = cell.getbbox()
                        if bbox:
                            l, t, r2, b = bbox
                            if l <= cx_local <= r2 and t <= cy_local <= b:
                                l = max(0, l - padding)
                                t = max(0, t - padding)
                                r2 = min(cw, r2 + padding)
                                b = min(ch, b + padding)
                                cell = cell.crop((l, t, r2, b))

            out_path = output_dir / f"{prefix}-{saved:02d}.png"
            cell.save(out_path, "PNG")
            print(f"Saved: {out_path}  size={cell.size}")

    return saved


def auto_split(input_path: Path, output_dir: Path, prefix: str,
               white_threshold: int = 240, margin_pct: int = 4,
               padding: int = 24, min_area: int = 20000,
               merge_distance_ratio: float = 0.25) -> int:
    """
    グリッド指定なしで Raw 画像全体を連結成分解析し、
    大きい素材コンポーネントを自動検出して個別保存。
    近傍の小コンポーネント（pen, clips など）は main にマージ。
    """
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    mx = int(w * margin_pct / 100)
    my = int(h * margin_pct / 100)
    inner = img.crop((mx, my, w - mx, h - my))
    arr = np.array(inner)

    rgb = arr[..., :3]
    white_mask = (
        (rgb[..., 0] >= white_threshold)
        & (rgb[..., 1] >= white_threshold)
        & (rgb[..., 2] >= white_threshold)
    )
    arr[..., 3] = np.where(white_mask, 0, 255)

    mask = arr[..., 3] > 0
    labeled, num = ndimage.label(mask)
    objects = ndimage.find_objects(labeled)

    comps = []
    for i, obj in enumerate(objects, start=1):
        if obj is None:
            continue
        ys, xs = obj
        a = (ys.stop - ys.start) * (xs.stop - xs.start)
        comps.append({
            "label": i,
            "l": int(xs.start), "t": int(ys.start),
            "r": int(xs.stop), "b": int(ys.stop),
            "area": a,
            "cy": (ys.start + ys.stop) / 2,
            "cx": (xs.start + xs.stop) / 2,
        })

    # 大きいコンポーネント = 素材本体候補
    mains = [c for c in comps if c["area"] >= min_area]
    smalls = [c for c in comps if c["area"] < min_area and c["area"] > 200]

    # 各 main から近傍の main + small をマージ（処理済みは除外）
    processed = set()
    materials = []
    for m in mains:
        if m["label"] in processed:
            continue
        size = max(m["r"] - m["l"], m["b"] - m["t"])
        bbox = [m["l"], m["t"], m["r"], m["b"]]
        keep_labels = {m["label"]}
        # 近傍の main をマージ
        for m2 in mains:
            if m2["label"] == m["label"] or m2["label"] in processed:
                continue
            d = ((m2["cy"] - m["cy"]) ** 2 + (m2["cx"] - m["cx"]) ** 2) ** 0.5
            if d < size * merge_distance_ratio:
                bbox[0] = min(bbox[0], m2["l"])
                bbox[1] = min(bbox[1], m2["t"])
                bbox[2] = max(bbox[2], m2["r"])
                bbox[3] = max(bbox[3], m2["b"])
                keep_labels.add(m2["label"])
                processed.add(m2["label"])
        # 近傍の small もマージ
        for s in smalls:
            d = ((s["cy"] - m["cy"]) ** 2 + (s["cx"] - m["cx"]) ** 2) ** 0.5
            if d < size * merge_distance_ratio:
                bbox[0] = min(bbox[0], s["l"])
                bbox[1] = min(bbox[1], s["t"])
                bbox[2] = max(bbox[2], s["r"])
                bbox[3] = max(bbox[3], s["b"])
                keep_labels.add(s["label"])
        processed.add(m["label"])
        # 中心を更新
        cy = (bbox[1] + bbox[3]) / 2
        cx = (bbox[0] + bbox[2]) / 2
        materials.append({"bbox": bbox, "labels": keep_labels, "cy": cy, "cx": cx})

    # 位置でソート：cy で Row 分類 → cx で Col 順
    # Row 分類：高さ平均の 60% で分ける
    if materials:
        avg_h = np.mean([m["bbox"][3] - m["bbox"][1] for m in materials])
        materials.sort(key=lambda m: m["cy"])
        rows = []
        current_row = [materials[0]]
        for m in materials[1:]:
            if m["cy"] - current_row[0]["cy"] < avg_h * 0.6:
                current_row.append(m)
            else:
                current_row.sort(key=lambda x: x["cx"])
                rows.extend(current_row)
                current_row = [m]
        current_row.sort(key=lambda x: x["cx"])
        rows.extend(current_row)
        materials = rows

    output_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    for m in materials:
        saved += 1
        l, t, r, b = m["bbox"]
        # keep_labels に含まれるラベルだけ保持
        keep_mask = np.isin(labeled, list(m["labels"]))
        arr2 = arr.copy()
        arr2[..., 3] = np.where(keep_mask, 255, 0)
        cell = Image.fromarray(arr2)
        # padding
        iw_a, ih_a = cell.size
        l = max(0, l - padding)
        t = max(0, t - padding)
        r = min(iw_a, r + padding)
        b = min(ih_a, b + padding)
        cell = cell.crop((l, t, r, b))
        out_path = output_dir / f"{prefix}-{saved:02d}.png"
        cell.save(out_path, "PNG")
        print(f"Saved: {out_path}  size={cell.size}")

    return saved


def main() -> None:
    p = argparse.ArgumentParser(description="Split a grid catalog image into individual transparent PNGs.")
    p.add_argument("input", help="Input grid image (e.g. Downloads/印章L.png)")
    p.add_argument("--out", required=True, help="Output directory")
    p.add_argument("--rows", type=int, required=True)
    p.add_argument("--cols", type=int, required=True)
    p.add_argument("--prefix", required=True, help="Output filename prefix (e.g. seal-l)")
    p.add_argument("--no-transparent", action="store_true", help="Disable white-to-transparent conversion")
    p.add_argument("--margin", type=int, default=10, help="Outer margin percent to crop (default 10)")
    p.add_argument("--threshold", type=int, default=240, help="White threshold 0-255 (default 240)")
    p.add_argument("--no-tight", action="store_true", help="Disable bbox-based tight crop (keep raw cell crop)")
    p.add_argument("--padding", type=int, default=24, help="Padding pixels around detected bbox (default 24)")
    p.add_argument("--overlap", type=int, default=15, help="Overlap percent for sampling each cell (default 15)")
    p.add_argument("--group-distance", type=float, default=1.3, help="Group neighbor components within main_size * X (default 1.3, set 0 to disable grouping)")
    p.add_argument("--group-area-min", type=float, default=0.25, help="Min area ratio for grouping (default 0.25)")
    p.add_argument("--group-area-max", type=float, default=4.0, help="Max area ratio for grouping (default 4.0)")
    p.add_argument("--auto", action="store_true", help="Auto-detect materials via connected components (ignore rows/cols)")
    p.add_argument("--min-area", type=int, default=20000, help="Min pixel area for main component in auto mode (default 20000)")
    p.add_argument("--merge-distance", type=float, default=0.25, help="Auto-merge distance ratio in auto mode (default 0.25)")
    args = p.parse_args()

    if args.auto:
        n = auto_split(
            Path(args.input),
            Path(args.out),
            prefix=args.prefix,
            white_threshold=args.threshold,
            margin_pct=args.margin,
            padding=args.padding,
            min_area=args.min_area,
            merge_distance_ratio=args.merge_distance,
        )
        print(f"\nDone. {n} materials saved to {args.out}")
        return

    n = split_grid(
        Path(args.input),
        Path(args.out),
        rows=args.rows,
        cols=args.cols,
        prefix=args.prefix,
        transparent=not args.no_transparent,
        white_threshold=args.threshold,
        margin_pct=args.margin,
        tight=not args.no_tight,
        padding=args.padding,
        overlap_pct=args.overlap,
        group_distance=args.group_distance,
        group_area_min=args.group_area_min,
        group_area_max=args.group_area_max,
    )
    print(f"\nDone. {n} materials saved to {args.out}")


if __name__ == "__main__":
    main()
