"""全ページの .plate プレースホルダーを <img class="editorial-photo"> に一括置換"""
import re
from pathlib import Path

ROOT = Path(r"c:/Users/sss_1/OneDrive/ドキュメント/GitHub/homepage - コピー")

# (file_rel_path, [(image_filename, alt, variant), ...])
# 順番はファイル内の Plate 01, 02, ... の順
PAGES = [
    ("services/acupuncture/index.html", "../../images/photos", [
        ("acupuncture-visit-hero.png", "ご自宅での訪問施術の風景", "hero"),
        ("acupuncture-care-coordination.png", "ご家族・ケアマネジャーとの連携", "hero"),
    ]),
    ("cases/index.html", "../images/photos", [
        ("cases-01-rehab.png", "歩行ケアの様子（80代女性）", "wide"),
        ("cases-02-training.png", "体幹トレーニングの様子（60代女性）", "wide"),
        ("cases-03-family.png", "ご家族との連絡風景", "wide"),
        ("cases-04-seminar.png", "終活の個別相談の様子", "wide"),
    ]),
    ("community/index.html", "../images/photos", [
        ("community-network.png", "地域包括ケアの連携の様子", "hero"),
    ]),
    ("services/shukatsu/index.html", "../../images/photos", [
        ("shukatsu-consultation.png", "終活のご相談の様子", "wide"),
    ]),
    ("services/fitness/index.html", "../../images/photos", [
        ("fitness-main-real.jpg", "べるフィット 実際のレッスン風景", "hero"),
    ]),
    ("services/fitness/seed/index.html", "../../../images/photos", [
        ("fitness-seed.png", "スタッフとお客様の様子", "hero"),
    ]),
    ("services/fitness/night/index.html", "../../../images/photos", [
        ("fitness-night.png", "夜間枠のレッスン風景", "hero"),
    ]),
    ("solutions/fall-risk/index.html", "../../images/photos", [
        ("fall-risk-walking.png", "歩行ケアの様子", "wide"),
    ]),
    ("solutions/frailty/index.html", "../../images/photos", [
        ("frailty-community.jpg", "地域サロンでの様子", "wide"),
    ]),
    ("solutions/home-care-start/index.html", "../../images/photos", [
        ("home-care-start-family.png", "ご家族との初回ご相談", "wide"),
    ]),
    ("solutions/knee-pain/index.html", "../../images/photos", [
        ("knee-pain-support.png", "膝のケアの様子", "wide"),
    ]),
]

PLATE_PATTERN = re.compile(
    r'<div class="plate plate--(hero|wide)">\s*'
    r'<span class="plate__index">Plate\s*\d+</span>\s*'
    r'<span class="plate__caption">[^<]*'
    r'<span class="plate__caption-note">写真調整中</span>'
    r'</span>\s*'
    r'</div>',
    re.DOTALL
)

summary = []
for rel, base_path, items in PAGES:
    p = ROOT / rel
    if not p.exists():
        summary.append((rel, "NOT FOUND", 0, len(items)))
        continue
    text = p.read_text(encoding='utf-8')
    matches = list(PLATE_PATTERN.finditer(text))
    if len(matches) != len(items):
        summary.append((rel, f"MISMATCH found={len(matches)} expected={len(items)}", 0, len(items)))
        continue
    # 後ろから置換
    new_text = text
    for match, (fname, alt, variant) in zip(reversed(matches), reversed(items)):
        replacement = (
            f'<img src="{base_path}/{fname}" alt="{alt}" '
            f'class="editorial-photo editorial-photo--{variant}" loading="lazy">'
        )
        new_text = new_text[:match.start()] + replacement + new_text[match.end():]
    p.write_text(new_text, encoding='utf-8')
    summary.append((rel, "OK", len(items), len(items)))

# Print summary
ok = sum(1 for _, status, _, _ in summary if status == "OK")
print(f"=== Photo injection summary ({ok}/{len(PAGES)} files OK) ===")
for rel, status, done, total in summary:
    mark = "OK" if status == "OK" else "FAIL"
    print(f"  [{mark}] {rel} ({done}/{total}) {status if status != 'OK' else ''}")
