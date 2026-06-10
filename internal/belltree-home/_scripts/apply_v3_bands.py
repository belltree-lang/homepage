# -*- coding: utf-8 -*-
# 2026-06-11: 帯コピー v3（瞬間と知見）を適用する。
# 第1弾: parkinson / stroke（既存写真のみ・即時反映可）
# 第2弾: 残り5ページ（新写真6枚の到着後に PHASE2 = True で実行）
import re
from pathlib import Path

BASE = Path(r"C:\Users\sss_1\OneDrive\ドキュメント\GitHub\homepage - コピー\internal\belltree-home\solutions")
PHASE2 = False  # 新写真6枚の保存後に True にして再実行

def photo_band(label, src, alt, eyebrow, copy):
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

ALT = {
    "P1": "お薬手帳を確認しながら施術計画を立てる訪問鍼灸師",
    "P2": "施術後に利用者様と施術記録を一緒に確認する様子",
    "P3": "訪問鍼灸師が玄関先で訪問鞄を開く様子",
}

PHASE1 = {
    "parkinson": [
        photo_band("動ける時間", "section-shots/parkinson-medication-stilllife.png",
                   "お薬手帳と施術記録、鍼の道具を並べた施術準備の様子",
                   "動ける時間、動けない時間",
                   "朝は新聞を取りに行けるのに、夕方は廊下が長く感じる。お薬手帳と施術記録を並べて、効き目の波からその方の一日を読み解きます。"),
        photo_band("波に合わせる", "universal/post-treatment-debrief.png", ALT["P2"],
                   "波に合わせて組み立てる",
                   "お薬が効いている時間に施術するのと、切れかけの時間に固縮をゆるめるのとでは、組み立てが変わります。記録を、ご家族・ケアマネジャーとも共有します。"),
        photo_band("ご自宅で続ける", "universal/visit-beginning.png", ALT["P3"],
                   "ご自宅で続ける",
                   "通院がむずかしくなっても、ご自宅でなら続けられます。パーキンソン病の施術は医療保険の対象になる場合があります。費用は無料体験のときにご説明します。"),
    ],
    "stroke": [
        photo_band("退院後", "section-shots/stroke-mobility-aids.png",
                   "杖・四点杖・車椅子のある住み慣れたお部屋の様子",
                   "退院した日から、ゼロになる",
                   "リハビリ病院では毎日あった訓練が、退院した日からゼロになる。ご本人の意欲より先に、環境のほうが途切れます。"),
        photo_band("固くなる前に", "universal/post-treatment-debrief.png", ALT["P2"],
                   "固くなる前に、ゆるめる",
                   "麻痺した側は、動かさない時間が長いほど固くなります。固縮がすすむ前にゆるめておくことが、在宅でのリハビリの土台になります。"),
        photo_band("入り口", "universal/visit-beginning.png", ALT["P3"],
                   "入り口はどこからでも",
                   "脳梗塞後遺症の施術は、医療保険でうかがえます。退院前の相談も、ケアマネジャー経由も、ご家族からの直接のお電話も、入り口はどこからでも構いません。"),
    ],
}

PHASE2_PLANS = {
    "knee-pain": [
        photo_band("瞬間", "section-shots/knee-trash-pause.png",
                   "ゴミ袋を手に玄関先で一息つく様子",
                   "膝の痛みが削るもの",
                   "ゴミ出しまでの数十メートルに、気合いがいるようになった。痛むのは膝でも、削られていくのは「外に出る気持ち」のほうです。"),
        photo_band("知見", "universal/care-planning.png", ALT["P1"],
                   "痛む場所と、原因の場所",
                   "痛む膝そのものより、膝をかばって固くなった太ももやお尻の筋肉が、立ち上がりを重くしていることが多くあります。問診では、そこから探します。"),
        illust_band("一歩", "knee-pain", "knee-pain-l-06.png", "履き慣れた歩きやすい靴のイラスト",
                    "大げさじゃありません",
                    "「この程度で来てもらうのは大げさ」とよく言われます。大げさになる前に伺えるのが訪問の良さです。無料体験から始められます。"),
    ],
    "lower-back-pain": [
        photo_band("瞬間", "section-shots/lowerback-socks-wall.png",
                   "壁に手をつきながら靴下を履く様子",
                   "毎日に増える「段取り」",
                   "靴下を履くのに、壁が要る。床のものを拾うのに、一呼吸が要る。長年の腰痛は、そんな小さな段取りを毎日に増やしていきます。"),
        illust_band("知見", "lower-back-pain", "lower-back-pain-l-06.png", "窓辺のロッキングチェアのイラスト",
                    "揉んで戻る、を繰り返さない",
                    "「マッサージで楽になるのは数日だけ」という方こそ、痛みが出る動作と時間帯から組み立て直します。鍼・お灸・マッサージの配分は、その方の腰で変えます。"),
        photo_band("一歩", "universal/visit-beginning.png", ALT["P3"],
                   "医療保険が使えます",
                   "腰痛症は、鍼の施術に医療保険が使える症状です。整形外科に通いながらで構いません。まずは無料体験で、ご自身の腰で確かめてください。"),
    ],
    "frailty": [
        photo_band("瞬間", "section-shots/frailty-light-teacup.png",
                   "軽い湯のみを両手で持つ手元",
                   "先に気づくのは、まわり",
                   "湯のみが軽いものに替わっていた。歩幅が、敷居をまたぐだけの幅になっていた——弱り始めのサインは、本人より先に、まわりが気づきます。"),
        illust_band("知見", "frailty", "frailty-l-06.png", "湯気の立つお茶と緑の葉のイラスト",
                    "一つ動くと、残りがついてくる",
                    "「年のせい」と「戻せる衰え」の境目は、外から見るより曖昧です。筋肉と食欲と外出は連動していて、どれか一つが動き出すと、残りもついてきやすくなります。"),
        photo_band("一歩", "universal/visit-beginning.png", ALT["P3"],
                   "認定がなくても",
                   "介護保険の認定がなくても始められます。外出がおっくうになった方のところへ、こちらから伺います。費用は無料体験のときに分かりやすくご説明します。"),
    ],
    "fall-risk": [
        photo_band("瞬間", "section-shots/fallrisk-genkan-step.png",
                   "新聞を手に玄関の上がり框へ足をかける足元",
                   "転ぶのは、毎日の場所",
                   "夜中のトイレまでの数メートル。新聞を取りに出る玄関の一段。転ぶのは特別な場所ではなく、毎日通っている場所です。"),
        illust_band("知見", "fall-risk", "fall-risk-l-04.png", "杖と手すりのイラスト",
                    "転びやすさの正体",
                    "転びやすさの正体は、筋力だけではありません。足の裏の感覚と、足首の硬さ。施術では感覚と関節から整え、住まいの中の「転びやすい場所」への気づきもお伝えします。"),
        photo_band("一歩", "universal/visit-greeting.png",
                   "玄関先で出迎えを受ける訪問鍼灸師",
                   "見守る側の緊張ごと",
                   "「また転ぶんじゃないか」という見守る側の緊張も、ほぐす必要があります。状態によって医療保険が使えます。まずは一度、足を診せてください。"),
    ],
    "home-care-start": [
        photo_band("瞬間", "section-shots/homecare-kitchen-pause.png",
                   "実家の台所で手を止める娘",
                   "「そろそろ」の直感",
                   "冷蔵庫に、賞味期限の切れたものが増えていた。同じ話が、電話のたびに繰り返される——「そろそろかもしれない」というご家族の直感は、たいてい当たっています。"),
        illust_band("知見", "home-care-start", "home-care-start-l-06.png", "開いた玄関と外出用の靴のイラスト",
                    "迷うのは、あなたのせいではない",
                    "介護の入り口で迷うのは、制度が分かりにくいからで、ご家族のせいではありません。要介護認定の前にできることから、順番に並べ直します。"),
        photo_band("一歩", "universal/visit-greeting.png",
                   "玄関先で出迎えを受ける訪問ケアスタッフ",
                   "ご本人に言いにくければ",
                   "ケアマネジャーへの相談は無料です。ご本人に切り出しにくければ、まずはご家族だけでの相談でも構いません。"),
    ],
}

BAND_RE = re.compile(
    r'<!-- ===================== 訪問のひとこま（[^）]*） ===================== -->\r?\n'
    r'<section class="band-paper sec-pad">.*?</section>\r?\n',
    re.DOTALL,
)

plans = dict(PHASE1)
if PHASE2:
    plans.update(PHASE2_PLANS)

for slug, plan in plans.items():
    f = BASE / slug / "index.html"
    html = f.read_text(encoding="utf-8")
    matches = list(BAND_RE.finditer(html))
    assert len(matches) == 3, f"{slug}: expected 3 bands, found {len(matches)}"
    for m, new in reversed(list(zip(matches, plan))):
        html = html[: m.start()] + new + html[m.end():]
    f.write_text(html, encoding="utf-8")
    print(f"[done] {slug}")

# パーキンソン「対象です」: 難病医療費助成の記載を撤去（鍼灸マッサージ療養費は助成対象外）
pk = BASE / "parkinson" / "index.html"
html = pk.read_text(encoding="utf-8")
OLD = "公的な医療助成（難病医療費助成等）を受けられている方"
NEW = "お薬の効き目に波があり、体調に合わせたケアが必要な方"
if OLD in html:
    html = html.replace(OLD, NEW, 1)
    pk.write_text(html, encoding="utf-8")
    print("[done] parkinson 対象リスト: 難病医療費助成の記載を差し替え")
