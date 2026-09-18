# /qr/ — 紙に刷るQRの受け口

作成: 2026-09-18

名刺・チラシに刷るQRは、事業所のページを直接指さず、この下の短いパスを指す。
紙は刷り直せないが、ここの1行なら直せる。

| パス | いまの飛び先 |
|---|---|
| `/qr/shinkyu/` | `https://belltree1102.com/services/home-visit/` |
| `/qr/kyotaku/` | `https://belltree1102.com/services/home-care/` |
| `/qr/bellregal/` | `https://bellregal.com/` |
| `/qr/bellfit/` | `https://bellmfit.com/` |

## 作りの決まり

- GitHub Pages なので 302 は返せない。`meta refresh` と `location.replace` の二段で飛ばす
- 飛び先には `?utm_source=meishi&utm_medium=qr&utm_content=<パス名>` を付ける。
  GA4 の「トラフィック獲得」で、どのQRが何回読まれたかが数えられる
- `noindex, nofollow` を入れる。`canonical` は UTM を外した本来のURLを指す
- **パス名は変えない。** 変えると刷った紙のQRが死ぬ。飛び先だけ差し替える

## 直すとき

`index.html` の3か所（`meta refresh` / 本文のリンク / `location.replace`）を同じURLに揃える。
`canonical` は UTM を外した形にする。

## 経緯

2024年版から3代、鍼灸とべるフィットのQRが入れ替わったまま刷られていた。
`bellmfit.com/shinkyu` も居宅のページへ転送される設定のままになっている。
どちらも紙が直せないので直せなかった。その再発を止めるための仕掛け。
