"""要約カード用アイコン（sp-icon-people / clock / yen / car）を作る。

    python scripts/make_card_icons.py [出力先ディレクトリ]

生成AIは使わない。既存の sp-icon-moon から三日月を消して**本物の水彩ディスク**を復元し、
その上にクリーム抜きのシルエットを描く。だから紙目・にじみ・色が既存アイコンと完全に一致する。

様式の基準は sp-icon-moon / sp-icon-dumbbell（テラコッタの円＋クリームの形・小枝なし）。
hp-icon-people は明暗が逆（クリームの円＋テラコッタの形）なので基準にしない。

44px 表示では細部が潰れる。硬貨の重ね・財布・五円玉の中心穴はいずれも実寸で判別できず、
「太い一形」に寄せた円記号（yen）だけが読めた。細部を足したくなったら必ず実寸で確認する。
"""
import sys
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = Path('images/materials/subpages/sp-icon-moon.png')
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'images/materials/subpages')
S = 4                                    # スーパーサンプル倍率


def _box(arr, r, axis):
    n = arr.shape[axis]
    c = np.cumsum(np.concatenate([np.zeros_like(np.take(arr, [0], axis)), arr], axis=axis), axis=axis)
    i = np.arange(n)
    lo, hi = np.clip(i - r, 0, n), np.clip(i + r + 1, 0, n)
    s = np.take(c, hi, axis) - np.take(c, lo, axis)
    shape = [1] * arr.ndim
    shape[axis] = n
    return s / (hi - lo).reshape(shape)


def fblur(arr, sigma):
    """箱ぼかし3回でガウスを近似（PIL は float 画像の GaussianBlur に非対応）。"""
    r = max(1, int(round(sigma * 1.2)))
    out = arr.astype(np.float32)
    for _ in range(3):
        out = _box(_box(out, r, 0), r, 1)
    return out


# ===== 1. 三日月を消して無地の水彩ディスクを復元する =========================
# 水彩ウォッシュは「半径で決まる基準色」＋「ムラ（低周波）」＋「紙目（高周波）」に分解できる。
# 基準色とムラは穴の外から滑らかに外挿し、紙目だけを鏡像位置から借りる。
# 紙目まで含めて丸ごと借りると、消したはずの三日月が明るい亡霊として残る。
def restore_disc():
    a = np.array(Image.open(SRC).convert('RGBA')).astype(np.float32)
    H, W = a.shape[:2]
    inside = a[..., 3] > 128

    ys, xs = np.nonzero(inside)
    cy, cx = ys.mean(), xs.mean()
    R = math.sqrt(inside.sum() / math.pi)

    cream = inside & (a[..., :3].mean(axis=2) > 212)
    cm = Image.fromarray((cream * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
    hole = (np.array(cm) > 127) & inside          # 埋めるべき領域（アンチエイリアス込み）
    clean = inside & ~hole

    Y, X = np.mgrid[0:H, 0:W]
    rad = np.sqrt((Y - cy) ** 2 + (X - cx) ** 2)

    NB = 64
    bidx = np.clip((rad / (R * 1.05) * NB).astype(int), 0, NB - 1)
    prof, have = np.zeros((NB, 3), np.float32), np.zeros(NB, bool)
    for b in range(NB):
        m = clean & (bidx == b)
        if m.sum() >= 30:
            prof[b], have[b] = a[..., :3][m].mean(axis=0), True
    idx = np.arange(NB)
    k = np.array([1, 2, 3, 2, 1], np.float32) / 9.0
    for ch in range(3):
        prof[:, ch] = np.interp(idx, idx[have], prof[have, ch])
        prof[:, ch] = np.convolve(np.pad(prof[:, ch], 2, mode='edge'), k, 'valid')
    base = prof[bidx]

    resid = a[..., :3] - base
    cw = clean.astype(np.float32)
    den = fblur(cw, 18.0) + 1e-6
    resid_low = np.stack([fblur(resid[..., c] * cw, 18.0) / den for c in range(3)], axis=2)
    resid_hi = resid - resid_low

    xi = (2 * int(round(cx)) - X).clip(0, W - 1)
    yi = (2 * int(round(cy)) - Y).clip(0, H - 1)
    cands = [(Y, xi), (yi, X), (yi, xi),
             (np.clip(Y + 37, 0, H - 1), np.clip(X - 53, 0, W - 1)),
             (np.clip(Y - 61, 0, H - 1), np.clip(X + 29, 0, W - 1))]
    hi, todo = resid_hi.copy(), hole.copy()
    for sy, sx in cands:
        ok = todo & clean[sy, sx]
        hi[ok] = resid_hi[sy[ok], sx[ok]]
        todo &= ~ok
    hi[todo] = 0.0

    out = np.empty_like(a)
    out[..., :3] = np.clip(base + resid_low + hi, 0, 255)
    out[..., 3] = a[..., 3]
    return Image.fromarray(out.astype(np.uint8)), cx, cy, R


disc, CX, CY, R = restore_disc()
W, H = disc.size
d_arr = np.array(disc).astype(np.float32)
print('disc restored: center %.1f %.1f  R %.1f' % (CX, CY, R))


# ===== 2. その上にクリーム抜きのシルエットを描く =============================
class Pen:
    """単位は R（ディスク半径）。原点はディスク中心。c=0 で穴をあける。"""

    def __init__(self):
        self.img = Image.new('L', (W * S, H * S), 0)
        self.d = ImageDraw.Draw(self.img)
        self.dy = 0.0

    def p(self, u, v):
        return ((CX + u * R) * S, (CY + (v + self.dy) * R) * S)

    def ell(self, u, v, ru, rv, c=255):
        x, y = self.p(u, v)
        self.d.ellipse([x - ru * R * S, y - rv * R * S, x + ru * R * S, y + rv * R * S], fill=c)

    def rect(self, u0, v0, u1, v1, c=255):
        self.d.rectangle([self.p(u0, v0), self.p(u1, v1)], fill=c)

    def rr(self, u0, v0, u1, v1, rad, c=255):
        self.d.rounded_rectangle([self.p(u0, v0), self.p(u1, v1)], radius=rad * R * S, fill=c)

    def bar(self, u0, v0, u1, v1, w, c=255):
        self.d.line([self.p(u0, v0), self.p(u1, v1)], fill=c, width=int(w * R * S))
        for u, v in ((u0, v0), (u1, v1)):
            self.ell(u, v, w / 2, w / 2, c)


def people():
    """対象。中央に1人＋両脇に1人ずつ。輪郭が溶けないよう中央ぶんを一度あけてから描く。"""
    k = Pen()
    k.dy = 0.03
    for u in (-0.40, 0.40):
        k.ell(u, -0.20, 0.115, 0.115)
        k.rr(u - 0.20, -0.03, u + 0.20, 0.34, 0.20)
        k.rect(u - 0.20, 0.17, u + 0.20, 0.34)
    for c, g in ((0, 0.05), (255, 0.0)):
        k.ell(0, -0.30, 0.155 + g, 0.155 + g, c)
        k.rr(-0.24 - g, -0.09 - g, 0.24 + g, 0.34, 0.24 + g, c)
        k.rect(-0.24 - g, 0.15, 0.24 + g, 0.34, c)
    return k.img


def clock():
    """利用できる時間。短針11時・長針3時。44px で潰れないよう針は太めに取る。"""
    k = Pen()
    k.ell(0, 0, 0.60, 0.60)
    k.bar(0, 0, -0.27, -0.30, 0.115, 0)
    k.bar(0, 0, 0.44, 0.0, 0.100, 0)
    return k.img


def yen():
    """料金。硬貨1枚＋太い円記号。硬貨の重ね・財布は実寸で読めなかったのでこれを採る。"""
    k = Pen()
    k.ell(0, 0, 0.62, 0.62)
    w = 0.105
    k.bar(-0.26, -0.34, 0.0, -0.06, w, 0)
    k.bar(0.26, -0.34, 0.0, -0.06, w, 0)
    k.bar(0.0, -0.10, 0.0, 0.34, w, 0)
    k.bar(-0.22, 0.03, 0.22, 0.03, w, 0)
    k.bar(-0.22, 0.17, 0.22, 0.17, w, 0)
    return k.img


def car():
    """駐車場。真横から見た車。ホイールと窓を穴としてあける。"""
    k = Pen()
    k.dy = -0.09
    k.ell(-0.35, 0.33, 0.185, 0.185)
    k.ell(0.35, 0.33, 0.185, 0.185)
    k.rr(-0.66, -0.02, 0.66, 0.30, 0.13)
    k.rr(-0.34, -0.34, 0.26, 0.08, 0.13)
    k.ell(-0.35, 0.33, 0.075, 0.075, 0)
    k.ell(0.35, 0.33, 0.075, 0.075, 0)
    k.rr(-0.27, -0.26, 0.17, -0.03, 0.055, 0)
    return k.img


# クリームの塗り（moon のクリーム部を再現：上が明るく、下が少し温かい）
Y, X = np.mgrid[0:H, 0:W]
g = np.clip((Y - (CY - 0.6 * R)) / (1.3 * R), 0, 1)[..., None]
cream = np.array([253., 241., 224.]) * (1 - g) + np.array([248., 226., 194.]) * g

# ディスク自身の紙目を弱く載せて、同じ紙の上にあるように見せる
base_l = d_arr[..., :3].mean(axis=2)
grain = np.array(base_l - np.array(Image.fromarray(base_l.astype(np.uint8))
                                   .filter(ImageFilter.GaussianBlur(6))), np.float32)[..., None]

OUT.mkdir(parents=True, exist_ok=True)
for name, fn in (('people', people), ('clock', clock), ('yen', yen), ('car', car)):
    m = fn().resize((W, H), Image.LANCZOS)
    a = (np.array(m).astype(np.float32) / 255.0)[..., None]

    # 形の右下だけわずかに沈ませる（既存アイコンの陰の付き方に合わせる）
    sh = np.array(m.filter(ImageFilter.GaussianBlur(5 * S)).resize((W, H), Image.LANCZOS),
                  dtype=np.float32) / 255.0
    sh = np.roll(np.roll(sh, 3, axis=0), 3, axis=1)[..., None]
    fill = cream + grain * 0.55 - np.clip(a - sh, 0, 1) * 9.0

    out = d_arr.copy()
    out[..., :3] = d_arr[..., :3] * (1 - a) + np.clip(fill, 0, 255) * a
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    im.save(OUT / ('sp-icon-%s.png' % name))
    im.save(OUT / ('sp-icon-%s.webp' % name), quality=92, method=6)
    print('wrote sp-icon-%s' % name)
