# -*- coding: utf-8 -*-
# 2026-06-10: 「訪問のひとこま」帯の全ページ同一問題を解消。
# 文言を症状別に書き分け、写真の組み合わせを変え、5ページに専用イラスト帯を導入。
import re
from pathlib import Path

BASE = Path(r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー\internal\belltree-home\solutions")

PHOTOS = {
    "P1": ("universal/care-planning.png", "お薬手帳を確認しながら施術計画を立てる訪問鍼灸師"),
    "P2": ("universal/post-treatment-debrief.png", "施術後に利用者様と施術記録を一緒に確認する様子"),
    "P3": ("universal/visit-beginning.png", "訪問鍼灸師が玄関先で訪問鞄を開く様子"),
}

def photo_band(label, key, eyebrow, copy):
    src, alt = PHOTOS[key]
    return f'''<!-- ===================== 訪問のひとこま（{label}） ===================== -->
<section class="band-paper sec-pad">
  <div class="wrap">
    <figure class="photo-moment reveal">
      <img src="../../../../images/photos/{src}" alt="{alt}" loading="lazy" />
      <figcaption class="pm-text">
        <span class="pm-eyebrow">{eyebrow}</span>
        <p>{copy}</p>
      </figcaption>
    </figure>
  </div>
</section>
'''

def illust_band(label, slug, fname, alt, eyebrow, copy):
    return f'''<!-- ===================== 訪問のひとこま（{label}） ===================== -->
<section class="band-paper sec-pad">
  <div class="wrap">
    <div class="illust-moment reveal">
      <div class="im-art"><img src="../../../../images/materials/decoration/L/{slug}/{fname}" alt="{alt}" loading="lazy" /></div>
      <div class="im-text">
        <span class="im-eyebrow">{eyebrow}</span>
        <p>{copy}</p>
      </div>
    </div>
  </div>
</section>
'''

KEEP = None  # 既存の帯（parkinson/strokeの専用写真）はそのまま

PLANS = {
    "parkinson": [
        KEEP,
        photo_band("記録の共有", "P2", "効き具合を記録して共有",
                   "その日の動きやすさやお薬の効き具合を毎回記録し、ご家族や担当のケアマネジャーと共有します。"),
        photo_band("訪問開始", "P3", "ご自宅へ伺います",
                   "通院がむずかしくなっても、ケアをあきらめる必要はありません。道具一式を持って玄関先まで伺います。"),
    ],
    "stroke": [
        KEEP,
        photo_band("記録の共有", "P2", "回復の歩みを記録",
                   "麻痺側の動きの変化を施術のたびに記録し、ご家族やケアマネジャー、リハビリ職との連携に活かします。"),
        photo_band("訪問開始", "P3", "退院後のご自宅へ",
                   "退院してリハビリが途切れがちな時期こそ。国家資格者が道具一式を持って、ご自宅へ伺います。"),
    ],
    "knee-pain": [
        photo_band("施術計画", "P1", "初回の問診から",
                   "立ち上がりや階段の昇り降りなど、どの場面で膝が痛むのかを丁寧に聞き取り、施術の計画を立てます。"),
        illust_band("目標", "knee-pain", "knee-pain-l-06.png", "履き慣れた歩きやすい靴のイラスト",
                    "目標は、また自分の足で",
                    "履き慣れた靴で近所まで歩く。その日常を取り戻すことを、施術の目標にしています。"),
        photo_band("記録の共有", "P2", "変化を記録して共有",
                   "歩ける距離や立ち上がりの様子を毎回記録し、ご本人・ご家族と一緒に確かめながら進めます。"),
    ],
    "lower-back-pain": [
        photo_band("訪問開始", "P3", "ご自宅で、そのまま",
                   "起き上がりや中腰がつらい毎日に。通う負担なく、ご自宅でそのまま施術を受けられます。"),
        photo_band("施術計画", "P1", "痛む動作から組み立てる",
                   "起き上がり・立ち上がり・中腰の家事。どの動作で痛むのかを確認しながら、施術の内容を組み立てます。"),
        illust_band("目標", "lower-back-pain", "lower-back-pain-l-06.png", "窓辺のロッキングチェアのイラスト",
                    "楽な時間を、少しずつ長く",
                    "痛みに身構えずに座れる、眠れる。そうした時間を少しずつ増やしていくことを目指します。"),
    ],
    "frailty": [
        photo_band("施術計画", "P1", "小さな変化から確認",
                   "体重や食欲、歩く速さの変化まで含めて伺い、いまのお身体に合った施術計画を立てます。"),
        illust_band("目標", "frailty", "frailty-l-06.png", "湯気の立つお茶と緑の葉のイラスト",
                    "できることを、少しずつ",
                    "お茶を淹れる、郵便を取りに出る。暮らしの中の小さな動作を保つことが、何よりの対策になります。"),
        photo_band("訪問開始", "P3", "こちらから伺います",
                   "外出がおっくうになってきた方こそ。ご自宅に伺う形なら、無理なくケアを続けられます。"),
    ],
    "fall-risk": [
        illust_band("住まいの点検", "fall-risk", "fall-risk-l-04.png", "杖と手すりのイラスト",
                    "住まいの中も、一緒に点検",
                    "施術だけでなく、敷居や廊下など「転びやすい場所」への気づきもあわせてお伝えします。"),
        photo_band("記録の共有", "P2", "ふらつきの変化を記録",
                   "歩き方やふらつきの変化を毎回記録し、ご家族や担当のケアマネジャーと共有します。"),
        photo_band("訪問開始", "P3", "玄関先から、気を配ります",
                   "伺うのは、段差や廊下のある実際の生活の場。その場だからこそできる助言があります。"),
    ],
    "home-care-start": [
        photo_band("現状の整理", "P2", "まずは現状の整理から",
                   "困りごとを一緒に書き出して整理するところから。介護保険の仕組みも、分かる言葉でご説明します。"),
        illust_band("最初の一歩", "home-care-start", "home-care-start-l-06.png", "開いた玄関と外出用の靴のイラスト",
                    "最初の一歩は、相談だけで",
                    "申し込みや契約ではなく、話を聞いてみるだけで大丈夫。それが介護の始め方の一歩目です。"),
        photo_band("訪問相談", "P3", "ご自宅へ伺います",
                   "ケアマネジャーへのご相談に費用はかかりません。ご自宅に伺い、暮らしの様子に合わせてご提案します。"),
    ],
}

ILLUST_CSS = """  /* ===================== ILLUST MOMENT（ページ専用イラスト帯）===================== */
  .illust-moment {
    display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 56px;
    align-items: center; max-width: 1040px; margin: 0 auto;
  }
  .illust-moment .im-art { position: relative; }
  .illust-moment .im-art::before {
    content: ""; position: absolute; inset: -4% 6%;
    background: radial-gradient(circle, rgba(255,235,215,0.75) 0%, transparent 62%);
    border-radius: 50%;
  }
  .illust-moment .im-art img { position: relative; width: 100%; height: auto; }
  .illust-moment .im-text .im-eyebrow {
    display: block; font-size: 12px; letter-spacing: 0.16em;
    color: var(--bt-accent); font-weight: 700; margin-bottom: 14px;
  }
  .illust-moment .im-text p {
    font-family: var(--bt-font-serif); font-weight: 600;
    font-size: clamp(15px, 1.55vw, 19px); line-height: 2.05;
    color: var(--bt-primary); margin: 0;
  }
  @media (max-width: 760px) {
    .illust-moment { grid-template-columns: 1fr; gap: 18px; }
    .illust-moment .im-art { max-width: 420px; margin: 0 auto; }
  }

"""
CSS_ANCHOR = "  .reveal { opacity: 1; }"

BAND_RE = re.compile(
    r'<!-- ===================== 訪問のひとこま（[^）]*） ===================== -->\r?\n'
    r'<section class="band-paper sec-pad">.*?</section>\r?\n',
    re.DOTALL,
)

for slug, plan in PLANS.items():
    f = BASE / slug / "index.html"
    html = f.read_text(encoding="utf-8")
    matches = list(BAND_RE.finditer(html))
    assert len(matches) == 3, f"{slug}: expected 3 bands, found {len(matches)}"
    # 後ろから差し替え（オフセットずれ防止）
    for m, new in reversed(list(zip(matches, plan))):
        if new is None:
            continue
        html = html[: m.start()] + new + html[m.end():]
    if "illust-moment" in html and "ILLUST MOMENT" not in html.split("</style>")[0]:
        assert CSS_ANCHOR in html, f"{slug}: CSS anchor missing"
        html = html.replace(CSS_ANCHOR, ILLUST_CSS + CSS_ANCHOR, 1)
    f.write_text(html, encoding="utf-8")
    kinds = ["keep" if b is None else ("illust" if "illust-moment" in b else "photo") for b in plan]
    print(f"[done] {slug}: {kinds}")
