# 引継ぎ：material-pipeline 進行中作業

**日付**: 2026-06-07
**現セッション**: パーキンソン病ページ完成 → 脳卒中ページ専用L素材完成 → 残り5ページの素材生成待ち

---

## 別ターミナルで Claude を起動したら、最初にこれを読む

このファイルと、その下に書いてあるパス2つを Read すれば、別ターミナルの Claude が即座に文脈を引き継げる。

```
# 必読
1. このファイル
2. C:\Users\sss_1\.claude\skills\material-pipeline\SKILL.md
3. C:\Users\sss_1\.claude\skills\material-pipeline\references\06-placement-and-clean-split.md
```

スキル起動キーワード：「素材作って」「material-pipeline」「○○の続き」など、material-pipeline の description に該当する発話で自動起動する。

---

## 完成済みの素材・ページ

### 専用 L 素材（6素材ずつ・3:2 横長 800×533）

| ページ | 素材保存先 | ページ反映 |
|---|---|---|
| パーキンソン病 | `images/materials/decoration/L/parkinson/parkinson-l-01〜06.png` | ✅ 完成（v8） |
| 脳卒中 | `images/materials/decoration/L/stroke/stroke-l-01〜06.png` | ✅ お悩み4枚反映済 |

### M シート（20素材・500×500 正方）

| ページ | 素材保存先 | ページ反映 |
|---|---|---|
| パーキンソン病 | `images/materials/decoration/M/parkinson/parkinson-m-01〜20.png` | ✅ 対象者リスト4＋見出し3反映済 |

### 未生成 L 素材

**なし（2026-06-10 全7ページ完了）。**

膝痛・腰痛・フレイル・転倒リスク・介護の始め方の5枚は、一括バッチプロンプト
`internal/belltree-home/PROMPT-BATCH-5-LSHEETS-IMAGES2.txt`（5シート連続生成・写真トーン解除付き）で生成成功。
分割は `internal/belltree-home/_scripts/split_lsheets_20260610.py`（コミット b12154c）。
個別プロンプト5本（PROMPT-*-OBJECTS-L-IMAGES2.txt）は完了済みのため再投入不要。

補足（2026-06-10）: 全7ページに images2.0 写真の「訪問のひとこま」帯3本も反映済み
（`images/photos/section-shots/` + `universal/`、コミット 143739d）。

---

## 別ターミナル Claude の標準フロー（各ページ）

```
[1] 代表が「○○L来た」と一声＋ファイル名で告知
[2] Bash: mkdir + cp で Raw を _raw/ に保管
[3] Python (PIL) で 2×3 等分割 + トリム + bbox + 透過 + 800×533 リサイズ
[4] solutions/<slug>/index.html のお悩み4カードを新素材に差替え (Edit)
[5] Edge headless スクショで自分の目で確認 (memory: feedback_ui_verify_with_screenshot)
[6] SendUserFile でスクショを代表に送信
[7] git add 個別パス → commit → push origin staging
[8] 代表に「○○ページ反映完了、スマホで確認: bellmfit.com/test/internal/belltree-home/solutions/<slug>/」
```

### Python 処理コード（コピペで動く・page slug だけ差替え）

```python
from PIL import Image

slug = 'knee-pain'  # ← ここを切り替える: knee-pain / lower-back-pain / frailty / fall-risk / home-care-start
raw = f'images/materials/decoration/L/_raw/{slug}-objects-L-raw.png'
outdir = f'images/materials/decoration/L/{slug}'
TW, TH = 800, 533

im = Image.open(raw).convert('RGBA')
W, H = im.size
COLS, ROWS = 2, 3
cw, ch = W // COLS, H // ROWS

def trim(crop, white_th=240, pad=20):
    px = crop.load(); w,h = crop.size
    mx,my,Mx,My = w,h,0,0
    for y in range(h):
        for x in range(w):
            r,g,b,a = px[x,y]
            if not (r>white_th and g>white_th and b>white_th):
                if x<mx: mx=x
                if y<my: my=y
                if x>Mx: Mx=x
                if y>My: My=y
    if mx>=Mx or my>=My: return crop
    mx=max(0,mx-pad); my=max(0,my-pad)
    Mx=min(w,Mx+pad); My=min(h,My+pad)
    return crop.crop((mx,my,Mx,My))

idx = 0
for row in range(ROWS):
    for col in range(COLS):
        idx += 1
        x0, y0 = col*cw, row*ch
        x1 = (col+1)*cw if col<COLS-1 else W
        y1 = (row+1)*ch if row<ROWS-1 else H
        cell = im.crop((x0, y0, x1, y1))
        cw2, ch2 = cell.size
        cell = cell.crop((int(cw2*0.05), int(ch2*0.05), int(cw2*0.95), int(ch2*0.95)))
        cell = trim(cell)
        px = cell.load(); w,h = cell.size
        for y in range(h):
            for x in range(w):
                r,g,b,a = px[x,y]
                if r>245 and g>245 and b>245:
                    px[x,y] = (r,g,b,0)
        iw, ih = cell.size
        ratio = min(TW/iw, TH/ih) * 0.92
        nw, nh = int(iw*ratio), int(ih*ratio)
        resized = cell.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new('RGBA', (TW, TH), (0,0,0,0))
        canvas.paste(resized, ((TW-nw)//2, (TH-nh)//2), resized)
        canvas.save(f'{outdir}/{slug}-l-{idx:02d}.png')
        print(f'{slug}-l-{idx:02d}.png  {iw}x{ih} -> {TW}x{TH}')
```

### お悩みカード差替えパターン（HTML）

ページ `internal/belltree-home/solutions/<slug>/index.html` の `.concern-grid-2` 内の 4 カードの `<img src=...>` を、新しい素材パスに差替える。

```html
<img src="../../../../images/materials/decoration/L/<slug>/<slug>-l-NN.png" alt="" />
```

セル割り当て例（各ページのお悩み4 と素材 01〜04 を意味で対応させる）：
- パーキンソン病: 01=固縮, 02=すくみ足, 03=薬切れ, 04=通院負担
- 脳卒中: 01=リハビリ不足, 02=麻痺・固縮, 03=在宅ケア, 04=送迎の負担

膝痛以降も同様に01〜04を順番にお悩み4へ。素材 05・06 は将来サポート見出し/アプローチ最終見出しのアクセントに使う。

---

## 直近完了した作業（このセッションで）

- パーキンソン病ページ v1〜v8（紙テクスチャ + 半透明カード + L 6素材 + M 20素材 + 対象者・見出しの意味アクセント）
- 脳卒中ページ v1〜v2（パーキンソン v8 テンプレ流用 + 専用L素材）
- 膝痛・腰痛・フレイル・転倒・介護開始ページ（HERO+お悩み4のみ最低差替え、下半分はパーキンソン仮置き）
- material-pipeline スキルに `references/06-placement-and-clean-split.md` 追加
- bellfit / 訪問鍼灸 / 居宅 / べるリーガル の各事業ロゴをサービスカードに反映
- 対応エリア地図を Leaflet + Stamen Watercolor + 市町村ポリゴンで実装

---

## staging URL（スマホ確認用）

```
https://bellmfit.com/test/internal/belltree-home/                         (home)
https://bellmfit.com/test/internal/belltree-home/about/                   (会社概要)
https://bellmfit.com/test/internal/belltree-home/solutions/parkinson/     (パーキンソン病)
https://bellmfit.com/test/internal/belltree-home/solutions/stroke/        (脳卒中)
https://bellmfit.com/test/internal/belltree-home/solutions/knee-pain/
https://bellmfit.com/test/internal/belltree-home/solutions/lower-back-pain/
https://bellmfit.com/test/internal/belltree-home/solutions/frailty/
https://bellmfit.com/test/internal/belltree-home/solutions/fall-risk/
https://bellmfit.com/test/internal/belltree-home/solutions/home-care-start/
```

push 後 1〜2 分でデプロイ反映。

---

## 将来の拡張（代表メモ・別途検討）

material-pipeline は元々 HP 用素材ライブラリのスキルだが、設計が「ブランド素材を images2.0 量産→切り抜き→規格保存」の汎用パイプラインなので、以下にも流用可能（2026-06-07 代表構想）：

- **スライド生成・プレゼン資料**（slidev / PowerPoint）の章扉・小物装飾・引用フレーム
- **社内説明資料**（運営マニュアル・スタッフ向け資料）のヘッダー装飾・セクション区切り
- **銀行向け資料**（融資面談、事業計画書）の表紙・章扉・ピクトグラム

新規ターゲットに展開する場合、変更点は主に：
1. プロンプトの「Subject of this sheet」だけ書き換え（業種・用途に合わせる）
2. ロゴ・キャプション領域の有無を canvas サイズで吸収
3. material-pipeline スキルの `references/02-material-catalog.md` に新カテゴリを追加

これは別タスクとして後日。
