# /q/ — 紙に刷るQRの受け口

作成: 2026-09-18

名刺・チラシに刷るQRは、事業所のページやLINEを直接指さず、この下の短いパスを指す。
紙は刷り直せないが、ここの1行なら直せる。

**パスが3文字なのは、QRのマス目を粗くするため。**
`https://belltree1102.com/` だけで25バイトあり、ここに長い名前を足すとQRの型が上がって
マス目が細かくなる。名刺の1つ8mm弱という大きさでは、それが読み取りに効く。

| パス | 面 | いまの飛び先 |
|---|---|---|
| `/q/shi/` | 鍼灸マッサージ院・サイト | `belltree1102.com/services/home-visit/` |
| `/q/kyo/` | 居宅介護支援・サイト | `belltree1102.com/services/home-care/` |
| `/q/reg/` | べるリーガル・サイト | `bellregal.com/` |
| `/q/fit/` | べるフィット・サイト | `bellmfit.com/` |
| `/q/lsh/` | 鍼灸マッサージ院・LINE | `lin.ee/tag9YEf`（@083oynfl） |
| `/q/lky/` | 居宅介護支援・LINE | `lin.ee/tag9YEf`（@083oynfl） |
| `/q/lrg/` | べるリーガル・LINE | `lin.ee/ZRDwfEu`（@683gbqvt・経路「名刺」） |
| `/q/lft/` | べるフィット・LINE | `lin.ee/Tm3Ro6b`（@936dgdxs） |

## LINEの経路について

`lsh` `lky` `lft` は、いまのところ既存の経路（ホームページのフッター）を指している。
**鍼灸（@083oynfl）とべるフィット（@936dgdxs）に「名刺」の友だち追加経路を作ったら、
ここを差し替える。**そうすると管理画面の「追加経路」で名刺からの友だちが数えられる。

経路は作成後に編集も削除もできない。名前は最初に決めきる。

## 作りの決まり

- GitHub Pages なので 302 は返せない。`meta refresh` と `location.replace` の二段で飛ばす
- サイト行きには `?utm_source=meishi&utm_medium=qr&utm_content=<面の名前>` を付ける。
  GA4 の「トラフィック獲得」で、どのQRが何回読まれたかが数えられる
- **LINE行きには付けない。**`lin.ee` は付けたパラメータを捨てるので意味が無く、
  転送が壊れる余地だけが残る。LINE側の数は管理画面の「追加経路」で見る
- `noindex, nofollow` を入れる。`canonical` は UTM を外した本来のURLを指す
- **パス名は変えない。** 変えると刷った紙のQRが死ぬ。飛び先だけ差し替える

## 直すとき

`index.html` の3か所（`meta refresh` / 本文のリンク / `location.replace`）を同じURLに揃える。
`meta refresh` と本文のリンクは `&` を `&amp;` に書く。`location.replace` は生の `&` のまま
（`<script>` の中では実体参照が解釈されないため）。

## 経緯

2024年版から3代、鍼灸とべるフィットのQRが入れ替わったまま刷られていた。
`bellmfit.com/shinkyu` も居宅のページへ転送される設定のままになっている。
どちらも紙が直せないので直せなかった。その再発を止めるための仕掛け。
