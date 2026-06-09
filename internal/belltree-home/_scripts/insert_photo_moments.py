# -*- coding: utf-8 -*-
# 2026-06-10: images2.0 生成写真5枚（section-shots 2 + universal 3）を
# solutions 7ページに「訪問のひとこま」写真帯として挿入する
from pathlib import Path

BASE = Path(r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー\internal\belltree-home\solutions")
SLUGS = ["parkinson", "stroke", "knee-pain", "lower-back-pain", "frailty", "fall-risk", "home-care-start"]

CSS_ANCHOR = "  .reveal { opacity: 1; }"
CSS_BLOCK = """  /* ===================== PHOTO MOMENT（訪問のひとこま・写真帯）===================== */
  .photo-moment {
    position: relative; border-radius: 24px; overflow: hidden;
    max-width: 1080px; margin: 0 auto;
    box-shadow: 0 24px 60px rgba(80,55,30,0.16), 0 6px 18px rgba(80,55,30,0.10);
  }
  .photo-moment > img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; }
  .photo-moment::after {
    content: ""; position: absolute; inset: 0;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.5);
    border-radius: 24px; pointer-events: none;
  }
  .pm-text { position: absolute; top: 50%; transform: translateY(-50%); right: 4.5%; width: 34%; }
  .pm-text .pm-eyebrow {
    display: block; font-size: 12px; letter-spacing: 0.16em;
    color: var(--bt-accent); font-weight: 700; margin-bottom: 14px;
  }
  .pm-text p {
    font-family: var(--bt-font-serif); font-weight: 600;
    font-size: clamp(15px, 1.55vw, 19px); line-height: 2.05;
    color: var(--bt-primary); margin: 0;
    text-shadow: 0 0 18px rgba(252,252,250,0.95), 0 0 6px rgba(252,252,250,0.8);
  }
  @media (max-width: 760px) {
    .pm-text {
      position: static; transform: none; width: auto;
      padding: 18px 20px 22px;
      background: rgba(255,255,255,0.75);
    }
    .pm-text p { text-shadow: none; }
  }

"""

SECTION_TPL = """<!-- ===================== 訪問のひとこま（{label}） ===================== -->
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

"""

BAND_A = {
    "parkinson": dict(
        label="施術計画",
        src="section-shots/parkinson-medication-stilllife.png",
        alt="お薬手帳と施術記録、鍼の道具を並べた施術準備の様子",
        eyebrow="服薬と合わせた施術計画",
        copy="お薬手帳を一緒に確認し、お薬の効き目の波に合わせて施術の内容と時間帯を調整します。",
    ),
    "stroke": dict(
        label="施術の場",
        src="section-shots/stroke-mobility-aids.png",
        alt="杖・四点杖・車椅子のある住み慣れたお部屋の様子",
        eyebrow="ご自宅がそのまま施術の場に",
        copy="杖や車椅子をお使いのままで大丈夫です。住み慣れたお部屋で、いつもの姿勢のまま施術を受けられます。",
    ),
    "_default": dict(
        label="施術計画",
        src="universal/care-planning.png",
        alt="お薬手帳を確認しながら施術計画を立てる訪問鍼灸師",
        eyebrow="初回の問診から",
        copy="お薬手帳とこれまでの経過を確認し、お一人おひとりに合わせた施術計画を立てるところから始めます。",
    ),
}
BAND_B = dict(
    label="施術記録の共有",
    src="universal/post-treatment-debrief.png",
    alt="施術後に利用者様と施術記録を一緒に確認する様子",
    eyebrow="施術記録の共有",
    copy="施術のたびに身体の変化を記録し、ご本人・ご家族・担当のケアマネジャーと共有します。",
)
BAND_C = dict(
    label="訪問開始",
    src="universal/visit-beginning.png",
    alt="訪問鍼灸師が玄関先で訪問鞄を開く様子",
    eyebrow="ご自宅へ伺います",
    copy="特別な準備はいりません。国家資格者が道具一式を持って、玄関先までお伺いします。",
)

ANCHOR_A = "<!-- ===================== 訪問鍼灸マッサージでできること ===================== -->"
ANCHOR_B = "<!-- ===================== 専門職向けCTA ===================== -->"
ANCHOR_C = "<!-- ===================== アプローチ最終 ===================== -->"

for slug in SLUGS:
    f = BASE / slug / "index.html"
    html = f.read_text(encoding="utf-8")
    if "photo-moment" in html:
        print(f"[skip] {slug}: already inserted")
        continue
    assert CSS_ANCHOR in html, f"{slug}: CSS anchor missing"
    for a in (ANCHOR_A, ANCHOR_B, ANCHOR_C):
        assert html.count(a) == 1, f"{slug}: anchor not unique: {a}"

    html = html.replace(CSS_ANCHOR, CSS_BLOCK + CSS_ANCHOR, 1)
    band_a = BAND_A.get(slug, BAND_A["_default"])
    html = html.replace(ANCHOR_A, SECTION_TPL.format(**band_a) + ANCHOR_A, 1)
    html = html.replace(ANCHOR_B, SECTION_TPL.format(**BAND_B) + ANCHOR_B, 1)
    html = html.replace(ANCHOR_C, SECTION_TPL.format(**BAND_C) + ANCHOR_C, 1)
    f.write_text(html, encoding="utf-8")
    print(f"[done] {slug}: 3 bands inserted (A={band_a['src'].split('/')[-1]})")
