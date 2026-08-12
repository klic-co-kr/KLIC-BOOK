# Day 3

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 注意事項: 本資料の再利用(2次利用)について

## ●

## 本資料について

## ○

## 東京大学松尾・岩澤研究室が作成し、2025年10月から11月にかけて開催されたLLM大規模言語モデル講座基礎編

## の講義資料です。

## ○

## クリエイティブ・コモンズのCC BY-NC-SA 4.0 DEED(表示– 非営利– 継承4.0 国際)のライセンス登録を

## しています。

## ●

## ライセンスの表示について

## ○

## 各スライドのページ最下部にライセンスの記載があります。再利用時には本ライセンス表示を必ずご記載ください。

## 再利用時に複製が困難な場合は、下記のテキストボックスを利用の上、ハイパーリンクも含めてライセンスの表記を

## するようお願いします。

## ○

## 再利用するページに参照論文等の引用がある場合は、巻末にあるReferenceより引用箇所を掲載してください。

## ●

## 非営利目的での利用について

## 再利用(2次利用)が許諾されています。

## ●

## 営利目的での再利用について

## こちらからお問い合わせください。

## ●

## その他

## ○

## 元の表現が変わらない範囲(フォント、サイズ等)であれば改変可能です。

## ○

## それ以外の改変その他ライセンスについての詳細は、こちらをご覧の上適切な取り扱いをお願いします。

## 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 3. Pre-training

## 内山史也

## 大規模言語モデル講座2025

許諾なく撮影や第三者

への開示を禁止します

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

3

## Pre-training（Day3）

## ●目的：

## ○LLM(大規模言語モデル)の主流なモデル構造であるTransformerと、

## その事前学習の仕組みを理解する

## ●目標：

## ○言語モデルにおけるTransformerの位置づけについて説明できる

## ○LLMで主流となっているTransformerのモデル構造について説明できる

## ○LLMの事前学習のパイプラインについて説明できる

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

4

## 全体の流れ

## ●講義：

## ○言語モデルとは何か？

## ○Transformer

## ○事前学習

## ○発展的話題

## ●演習：

## ○PyTorchを用いてTransformerを実装・学習

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

5

## 目次

## • 言語モデルとは何か？

## • Transformer

## • 事前学習

## • 発展的話題

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

6

## 目次

## • 言語モデルとは何か？

## ＊大規模言語モデル

## • Transformer

## • 事前学習

## • 発展的話題

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

7

## 言語モデルとTransformerの関係

## 近年の大規模言語モデルで

## 一般的に利用されている

## モデル構造

## 言語モデル

## ニューラル言語モデル

## Transformer

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

8

## 言語モデル(Language Models)とは

## • 単語の系列（≒文章）の生起確率𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿をモデル化したもの

## • 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿を連鎖律で分解したものは自己回帰言語モデルと呼ばれる

## 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿= 𝑃𝑥1 𝑝𝑥2 𝑥1 ⋯𝑝𝑥𝐿𝑥1, ⋯, 𝑥𝐿−1

## • 条件付き確率がわかると生成ができる

## 𝑝東京日本, の, 首都, は= 0.2

## 𝑝パリ日本, の, 首都, は= 0.001

## ⋮

## 𝑝カイロ日本, の, 首都, は= 0.0005

## • 𝑥𝐿としてふさわしい予測は、arg max 𝑝𝑥𝐿𝑥1, ⋯, 𝑥𝐿−1

## • この条件付き確率をニューラルネットで表現したのがニューラル言語モデル

## Day1の復習

## 日本の首都は→ 東京

## = arg max 𝑝𝑥日本, の, 首都, は

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

9

## （参考）DL以前の代表的な言語モデル

## • 条件付き確率を統計的に求める方法

## •

## 大規模コーパス内の単語列の出現頻度から求める

## •

## 単語列s の出現回数を#(s)とすると、

## • 課題

## •

## データスパースネス問題

## 単語列が長くなると、その出現回数が急速に減少し、条件付き確率の推定が困難になる

## •

## 類義語問題

## 類義語が個別の事象として扱われてしまう．言い方を微妙に変えただけでも異なる出現

## 頻度の語として扱われてしまう（例：”日本の首都は？”と”日本国の首都は？”）

## 𝑝東京

## 日本, の, 首都, は

## = #(日本, の, 首都, は, 東京)

## # 日本, の, 首都, は

## 1000回

## 200回

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

10

## （参考）DL以前の代表的な言語モデル

## • N-gram言語モデル

## •

## 直近のN-1個の単語を使って次の単語を予測する

## •

## 各単語の出現確率は出現頻度で推定する

## •

## （例）3-gram言語モデル

## • データスパースネス問題をある程度回避できる

## • 長距離の単語間の関係性を把握しづらいことが課題

## Transformerで解決（後述）

## 𝑝東京

## 日本, の, 首都, は

## ≈𝑝東京

## 首都, は

## 直近の２単語”首都は”だけから

## ”東京”と特定することは難しい

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

11

## ニューラル言語モデル

## • 条件付き確率を何らかのニューラルネットで推定したモデル

## • 他の機械学習と同様尤度を最大化するように訓練（誤差逆伝播）

## 日本

## の

## 首都

## は

## 東京

## 京都

## 東京

## 誤差

## 正解

## どのような

## ネットワーク構造が最適か？

## ニューラルネットワーク

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

12

## ニューラル言語モデル

## • ニューラル言語モデルは, 機械翻訳の分野で大きく発展してきた

## • ここから機械翻訳のタスクを例として検討する

## 吾輩

## は

## 猫

## である

## ニューラルネットワーク

## I

## am

## a

## cat

## I

## am

## a

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

13

## ニューラル言語モデル

## エンコーダ

## （入力）

## デコーダ

## （出力＋再帰的入力）

## 吾輩

## は

## 猫

## I

## am

## a

## cat

## I

## am

## a

## である

## • エンコーダ：文（翻訳元言語）の入力機構を持つニューラルネット

## • デコーダ：文（翻訳先言語）の出力機構および再帰的入力機構を持つNN

## 再帰的入力

## 入力

## 出力

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

[2] Ilya Sutskever et al. (2014), “sequence to sequence learning with neural networks”, NeurIPS2014 を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

14

## ニューラル言語モデル

## • RNN型言語モデル(代表的モデル：Seq2Seq)

## •

## RNN: Recurrent Neural Network

## •

## 冒頭の単語から一単語ずつニューラルネットワークに入力してニューロンを逐一更新

## •

## パラメータは使いまわし

## •

## 原理的には単語をいくつでも入力＆出力できる

## 吾輩

## は

## 猫

## である

## I

## am

## a

## cat

## I

## am

## a

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

[3] Tomáš Mikolov et al. (2010), “recurrent neural network based language model”, INTERSPEECH2010

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

15

## ニューラル言語モデル

## • RNN型言語モデル(代表的モデル：Seq2Seq)

## •

## 課題①：ニューロンが固定長なので、長文になると全ての情報を覚えきれない

## 結局、単語間の長距離依存性の把握が困難

## •

## 課題②：ネットワークが単語方向に深くなるため、学習が不安定(勾配消失, 勾配爆発)

## ＆学習が遅い

## 吾輩

## は

## 猫

## である

## I

## am

## a

## cat

## I

## am

## a

## ここまでBackProp

## するの大変。。。

## 入力文なんだったっけ

## ？（直近の単語は覚え

## てるけど。。。）

[1] 岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deck を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

16

## ニューラル言語モデル

## • Transformer（モデル構造については後述します）

## •

## アテンション機構を最大限活用することで, 先述したRNN型の問題を解決(*)

## •

## 単語間の長距離依存性を把握できるようになった

## •

## 誤差逆伝播(BackProp) のステップ数が単語数に依存しなくなり(短くなり)、学習の安

## 定化＆高速化を実現

## 吾輩

## は

## 猫

## である

## I

## am

## a

## アテンション機構

## （後述します）

## アテンション機構

## （後述します）

## I

## am

## a

## cat

(*) RNNにアテンション機構を導入する先行研究は存在するが, 全単語間ではなかった. Transformerは全単語間にアテンション機構を導入した. マルチヘッドアテンションも新規.

[4]Dzmitry Bahdanau et al. (2014),“Neural machine translation by jointly learning to align and translate” / 技術の差分についての解説は以下がわかりやすい.

[5]Masaki Hayashi (2022),Transformer とseq2seq with attention の違いは？系列変換モデル【Q and A 記事】| CVMLエキスパートガイド

## ここまでの

## BackPropステップ

## 数が短くなった！

## 長文の重要箇所を

## 覚えている！

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

17

## 目次

## • 言語モデルとは何か？

## • Transformer

## • 事前学習

## • 発展的話題

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

18

## LLMのモデル構造

## 2024/08/07 Gooogle Scholarにアクセス

## •

## Googleを中心とした研究チームが発表

## •

## Attention機構の採用で単語（トークン）の

## 長距離依存関係を効率的に学習

## •

## 学習時の並列計算も効率化できたことで

## 大規模化（分散学習）しやすくなった

## “Attention Is All You Need”, 2017

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

## Transformerが主流（”Attention Is All You Need”という論文で初出）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

19

## Transformerの凄さ

## •

## 2017年の発表以降, モデルの改良およびスケールによって、

## 数多くのベンチマークで当時の最高性能（SOTA）を達成し続けている

## •

## GPT-1~4、gpt-oss、Gemini 2.5等はTransformerが採用されている

## •

## GPT-4はモデルの詳細な構造については非公開だが、

## TransformerベースであるとTechnical Reportにて記載あり

## •

## GPT-5のアーキテクチャは不明だが、system cardにはLLMとして記述されている

## •

## GPT-5の評価事例

## •

## AIME 2025（米国の高校生向け数学競技）で94.6%（ツールなし）を記録

## •

## 医療分野では、HealthBench Hardで46.2%

## •

## Gemini 2.5の評価事例

## •

## AIME 2025（米国の高校生向け数学競技）で88.0%を記録

## •

## 最適化されたフレームワークにて、ポケットモンスター青を406.5時間でクリア

## LLMのモデル構造

[7] OpenAI (2023), “GPT-4 Technical Report”

[8] OpenAI (2025), “GPT-5 System Card”

[9] OpenAI (2025), “GPT-5 が登場”

[10] Google (2025), “Gemini 2.5 tech report”

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

20

## Transformerのモデル構造

## •

## ”ブロック” : Transformerを構成する最小単位

## •

## 左側のEncoderブロックを縦にN層、

## 右側のDecoderブロックも縦にN層並べて構成

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

## Transformer

## Encoder

## Block

## Decoder

## Block

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

21

## Transformerのモデル構造| イメージ

## 吾輩

## は

## 猫

## である

## I

## am

## a

## cat

## I

## am

## a

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## Encoder

## Decoder

## Encoder/Decoder

## ブロックがそれぞ

## れ縦に積み重なる

## トークンの数だけ

## ブロックが横に増

## えていく

## Attention機構によ

## って横のブロック

## 同士はつながる

## (情報伝達を行う)

## <BOS>

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

22

## Transformerのモデル構造| イメージ（GPTシリーズ）

## 桜

## が

## 綺麗

## は

## 桜

## が

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ・

## ＊実はEncoderがなくても

## Decoderだけでテキスト生成可能

## （出力と再帰入力があるから）

## ＊GPTシリーズはこの形式

## ＊Transformerが当初提案された

## 領域が機械翻訳だったため、

## 先行研究のEncoder-Decoder形式に

## 倣う形でモデル構造が提案された

## 春

## Decoder

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

23

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

## Transformerのパーツ

## 各パーツごとに解説

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

24

## Transformerのパーツ| Embedding

## 各パーツごとに解説

## • Embedding：単語のベクトル変換

## • Multi-Head Attention

## • Feed Forward

## • Others

色をRGBの3次元ベクトル

に変換するのと似ている

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

25

## Transformerのパーツ| Embedding テキストをどうやってBlockに取り込むか？

## “春は曙”

## “春”, “は”, “曙”

## 1050, 80, 24567

## [0,0,…,0,1,0,…0]

## [0,0,…,0,1,0,…0]

## [0,0,…,0,1,0,…0]

## [0.2,-0.5,…,…0.4]

## [-0.3,1.0,…,…0.8]

## [1.7,-0.9,…,…-0.6]

## テキスト

## トークン

## トークンID

## One-hotベクトル

## Word

## Embedding

## 単語の分散表現,

## 単語埋め込み

## MLPによるより低次元への変換（学習対象）

## {トークンID}番目だけ1で、

## 他はすべて0であるベクトルの構成

## 各トークンに一対一で割り当てられている

## トークンIDへの変換

## トークナイザー（*後述）による分割

## 1050番目

## 80番目

## 24567番目

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

26

## Transformerのパーツ| Embedding Word Embedding (WE)

## • 単語(Sparseな情報)をDenseな表現に変換

## •

## Transformerなどのモデルの入力値として扱える

## • 学習完了後のWord Embeddingには、単語間の意味の近さや関係性が埋め

## 込まれている（下図はイメージ）

色をRGBの3次元ベクトル

に変換するのと似ている

[15] Shraddha Anala (2020), ”A Guide to Word Embedding. What are they? How are they more useful… | by Shraddha Anala | Towards Data Science”より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

27

## Transformerのパーツ| Embedding Positional Encoding (PE)

## i番目の

## トークン

## のPE

## 1番目の

## トークンのPE

## i番目の

## トークンのPE

## d: ベクトルの次元数

## 最後の

## トークン

## のPE

## ・Transformerブロックに取り込む前に、Word Embeddingに位置情報を追加

## •

## Transformerブロックのアルゴリズムはトークンの位置情報に依存しない

## •

## このままだと単語の位置関係が考慮されないので事前にベクトルに埋め込む.

## •

## 実装例：トークンの位置によって異なるPEを各WEに加える

## •

## WE(“春”) + PE(“これは1番目のトークンです”)

## •

## WE(“は”) + PE(“これは2番目のトークンです”)

## •

## WE(“曙”) + PE(“これは3番目のトークンです”)

[16] John Hewitt, Natural Language Processing with Deep Learning CS224N/Ling284 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

28

## Transformerのパーツ| Embedding

## 各パーツごとに解説

## • Embedding：単語のベクトル変換

## • Multi-Head Attention

## • Feed Forward

## • Others

## テキストをトークンに分割

## Word Embedding（ベクトル）に変換

## Positional Encodingと足し合わせて

## Transformerに入力

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

29

## Transformerのパーツ| Multi-Head Attention

## 各パーツごとに解説

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

30

## Transformerのパーツ| Attention

## 全トークン間の類似度を測ることによって、長距離のトークン間の依存関係を

## 把握することを可能にした機構

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

31

## Transformerのパーツ| Attention

## 数式による整理

## 次頁からこの数式を

## アニメーションで説明する

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

32

## Transformerのパーツ| Attention

## 春

## は

## 曙

## アテンション機構の入力値：

## トークンのベクトル表現

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

33

## Transformerのパーツ| Attention

## 線形変換（MLP）にて

## Keyベクトルを作成

## 線形変換（MLP）にて

## Valueベクトルを作成

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

34

## Transformerのパーツ| Attention

## 第一トークン（”春”）について、

## 線形変換（MLP）にて

## Queryベクトルを作成

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

35

## Transformerのパーツ| Attention

## QueryベクトルとKeyベクト

## ルの内積により、トークン間

## の類似度=Scoreを測る

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

36

## Transformerのパーツ| Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

## QueryベクトルとKeyベクト

## ルの内積により、トークン間

## の類似度=Scoreを測る

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

37

## Transformerのパーツ| Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

## QueryベクトルとKeyベクト

## ルの内積により、トークン間

## の類似度=Scoreを測る

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

38

## Transformerのパーツ| Attention

## 類似度を

## Softmaxにより正規化

## （つまり, 合計で1になる）

## 値が大きい方が類似度[=単語間の依存]が強い

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

39

## Transformerのパーツ| Attention

## 類似度(実数) と

## Valueベクトルを掛け算

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

40

## Transformerのパーツ| Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

## 類似度(実数) と

## Valueベクトルを掛け算

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

41

## Transformerのパーツ| Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

## 類似度(実数) と

## Valueベクトルを掛け算

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

42

## Transformerのパーツ| Attention

## 全ベクトルの総和をとる

## Attentionの類似度に従って、Valueベクトルの加重平均を算出

## これを第一トークンにおけるAttention機構の出力値とする

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

43

## Transformerのパーツ| Attention

## 第二トークン（”は”）について、

## 線形変換（MLP）にて

## Queryベクトルを作成

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

44

## Transformerのパーツ| Attention

## 同様の流れで、第二トーク

## ンにおけるAttention機構

## の出力値を算出

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

45

## Transformerのパーツ| Attention

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

## 第三トークン（”曙”）について、

## 線形変換（MLP）にて

## Queryベクトルを作成

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

46

## Transformerのパーツ| Attention

## 同様の流れで、

## 第三トークンにおける

## Attention機構の

## 出力値を算出

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

47

## Transformerのパーツ| Attention（高速で復習）

## 春

## は

## 曙

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

48

## Transformerのパーツ| Attention

## 春

## は

## 曙

## 入力

## 出力

## １ステップで全単語とつなが

## ることで, 遠くのトークンの情

## 報を効率よく取り込むことが

## 出来るようになった！

## 各トークンが必要なトークン

## の情報だけを柔軟に取捨選択

## (これは時系列に従ってトーク

## ンを取り込むRNN型では実現

## できなかったこと)

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

49

## Transformerのパーツ| Attention

## 春

## は

## 曙

## 入力

## 出力

## 例①：次のトークンを予測す

## るときに直近のトークンだけ

## が役に立つとき、

## 遠くを見る必要はない

## 例②：次のトークンを予測す

## るときに遠くのトークン情報

## が重要なとき、

## 近くを見る必要はない

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

50

## Transformerのパーツ| Attention

## 春

## は

## 曙

## 入力

## 出力

## １ステップで全単語と繋がる

## ことで、RNNの課題であった

## ①単語間の長距離依存関係を

## 把握できるようになった！

## ②誤差逆伝播が安定かつ高速

## になった！(*)

## (*)

## 安定：勾配消失や勾配

## 爆発が発生しない

## 高速：GPU等での並列

## 演算処理しやすい

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

51

## Transformerのパーツ| Attention

## 春

## は

## 曙

## 入力

## 出力

## つまり：

## アテンション機構にて、

## 各トークンのベクトルが

## 他トークンとの関係性を

## 取り込み、より良い表現に

## Transform＝変換された!

[17] Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

52

## Transformerのパーツ| Attentionの可視化例

## “it”は、”The” “animal” に対して強いアテンションが

## かかっていることがわかる

## ＊常にこのくらい分かりやすい関係が得られるとは限らない

## 全単語間のAttention Map

## （ヒートマップ）が作れる

The

The

animal

didn

'

cross

animal

didn

'

t

cross

t

[18] Jay Alammar (2018) The Illustrated Transformer – Jay Alammar – Visualizing machine learning one concept at a time. より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

53

## Transformerのパーツ| Attention

## 数式による整理（復習）

## ベクトルの次元数が増えるとQ

## とKの内積の値(分散)が増大

## それを抑えるためベクトルの

## 次元数(の平方根で)割り算.

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

54

## Transformerのパーツ| Attention

## Encoder側のアテンション機構

## • 入力テキスト内でのアテンション（Self-Attention）

## Decoder側のアテンション機構

## •

## 入力テキストと出力テキストを跨ったアテンション（Cross-Attention）

## •

## 出力テキスト内でのアテンション（Self-Attention）

## •

## 出力テキストについて：自身より未来のトークンについてアテンションを張れ

## ないようにマスク(Causal Attention Mask)をかける

## Decoderは未来のテキストを予測する機構なのでカンニングを防ぐ必要がある

## I

## am

## a

## cat

## I

## am

## a

## cat

## 黒いマスの部分は, Query側のトークンからすると未来

## のトークンなので, Causal Attention Maskをかけてア

## テンションを張れないようにする.

## ＊プログラム実装上は, AttentionMapのSoftmax直前に

## て, 該当要素に大きな負の値(例: -1.0e+10)を足す.

## Query

## Key

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

55

## Transformerのパーツ| Multi-Head Attention

## •

## アテンション処理を複数個並列で行う

## その後、出力を一つのベクトルに統合する

## •

## 1つのトークンが様々なトークンに、異なる形

## 式のアテンションをあてることが可能となる

## i番目のアテンション機構

## (⇒)の出力

## h個のアテンション機構からの出力

## (ベクトル)をConcatenate

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

56

## Transformerのパーツ| Multi-Head Attention

## 各パーツごとに解説

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

## 各トークンのベクトルを

## 他トークンとの関係性を取り込むことで

## より良い表現に変換

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

57

## Transformerのパーツ| Feed Forward

## 各パーツごとに解説

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

58

## Feed Forward

## Transformerのパーツ| Feed Forward

## 巨大な２階建てのMLP

## 活性化関数

## （ReLU）

## 学習パラメータ

## 入力

## 出力

## 入力層

## 出力層

## 中間層

## 中間層の次元数は

## 入力/出力層の次元数の数倍

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

59

## Transformerのパーツ| Feed Forward

## 巨大な２階建てのMLP

## 活性化関数

## （ReLU）

## 学習パラメータ

## 入力

## 出力

## 例えばGPT-3の場合,

## ・入力層/出力層の次元数：12,288

## ・中間層の次元数：12,288×4=49,152

## ・総ブロック数：96

## つまり,

## Feed Forwardのパラメータ数：(12,288×49,152)[ﾊﾟﾗﾒｰﾀ/層]×2[層/ﾌﾞﾛｯｸ]×96[ﾌﾞﾛｯｸ]≒116B[ﾊﾟﾗﾒｰﾀ]

## GPT-3の総パラメータ数：175B[ﾊﾟﾗﾒｰﾀ]

## Feed Forwardの全体に占めるパラメータの割合：約66%

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

60

## Transformerのパーツ| Feed Forward

## 巨大な２階建てのMLP

## 活性化関数

## （ReLU）

## 学習パラメータ

## 入力

## 出力

## gpt-oss120B

## Llama3.1

## DeepSeek-v3

## Qwen3

## FFのパラメータ

## 数（Billions）

## 3.6 (115)

## 329

## 23 (657)

## 14 (227)

## 全体パラメータ

## 数（Billions）

## 5.1 (117)

## 405

## 37 (671)

## 22 (235)

## パラメータ数に

## おける

## FFの割合（%）

## 71 (98.3)

## 81.4

## 62 (97.8)

## 64 (96.7)

## 最近の各モデルシリーズの最大モデルのパラメータ構成*

*

（）内はMoEモデルの総パラメータ数を示す。MoEモデルは入力に応じて使用するパラメータを変えるため、実際の予測時には（）の左側にある数のパラメータしか使用されない

近年のモデルは上の数式と若干異なるアルゴリズムが採用されている（SwiGLUなど）

huggingfaceのconfigに登録されているmlp層のパラメータ数をもとに計算

gpt-ossについてはModel CardのTable1, DeepSeek-v3についてはTechnical ReportのSection 4.2も参考にした

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

61

## Transformerのパーツ| Feed Forwardは何をやっているのか？

## Feed Forwardは、パラメータ数が大きいだけに重要？

## ・第一層のパラメータをKey(K)とおく

## ・入力のパターンを抽出

## ・第二層のパラメータをValue(V)とおく

## ・パターンが何を意味しているか表現

## ・ニューラルメモリ（↓）を模倣している

## と解釈できる

## ⇒ 知識を蓄える場所と考えられる.

[19] Mor Geva et al. (2021), “Transformer Feed-Forward Layers Are Key-Value Memories”, ACL2021 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

62

## Transformerのパーツ| Feed Forward

## 各パーツごとに解説

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

## 巨大な2階層のMLP

## Key-Valueで蓄積した知識を

## 抽出する機構として考えられている

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

63

## Transformerのパーツ| Others

## 各パーツごとに解説

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

64

## Transformerのパーツ| Add & Norm

## Add：残差接続(residual connection)

## 深い層の学習をする時のテクニック

## Feed Forward / Attentionの後で適用

## Norm：レイヤ正規化(Layer Normalization)

## 学習を安定させるテクニック

## 隠れ層の次元軸で平均と分散をとり

## 正規化

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し,一部改変

[20] Kaiming He et al. (2016), “Deep Residual Learning for Image Recognition”, IEEE2016 を参考

[21] Jimmy Lei Ba et al. (2016), “Layer Normalization” を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

65

## Transformerのパーツ| 出力層

## •

## 線形変換後、Softmax関数を適用

## •

## 次の単語の生起確率を出力する

## 東京

## 京都

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

66

## Transformerのパーツ（復習）

## • Embedding

## • Multi-Head Attention

## • Feed Forward

## • Others

## 残差接続

## レイヤー正規化

## 出力層

## テキストをトークンに分割

## Word Embedding（ベクトル）に変換

## Positional Encodingと足し合わせて

## Transformerに入力

## 各トークンのベクトルを

## 他トークンとの関係性を取り込むことで

## より良い表現に変換

## 巨大な2階層のMLP

## Key-Valueで蓄積した知識を

## 抽出する機構として考えられている

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

67

## 目次

## • 言語モデルとは何か？

## • Transformer

## • 事前学習

## • 発展的話題

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

68

## LLMの学習の流れ

## 事前学習

## 大規模コーパスによる自己教師あり学習を通し、大規模言語モデルに

## 語彙・文法・基本知識といった基礎的な言語理解を獲得させる段階

## ファインチューニング

## ラベル付きデータによる教師あり学習を通し、事前学習済みモデルの

## 性能を改善したり、特定のタスクやドメインへの適応を実現する段階

## 強化学習

## 人間からのフィードバックを用い、大規模言語モデルの出力が

## より人間の価値観に沿ったものとなるよう調整する段階

## Step 1

## Step 2

## Step 3

## Day3（本日）

## Day6

## Day7

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

69

## 事前学習とは

## LLM以前

## ・・・

## 翻訳モデル

## 要約モデル

## 読解モデル

## ・・・

## 学習

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

70

## 事前学習とは

## LLM以前

## LLM

## ・・・

## 翻訳モデル

## 要約モデル

## 読解モデル

## ・・・

## 事前学習

## 汎用

## LLM

## 学習

## 大規模コーパス

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

71

## 事前学習とは

## LLM以前

## LLM

## ・・・

## 翻訳モデル

## 要約モデル

## 読解モデル

## ・・・

## 翻訳モデル

## 要約モデル

## 読解モデル

## 事後学習

## •

## ファインチューニング

## •

## 強化学習

## 事前学習

## 汎用

## LLM

## 学習

## 大規模コーパス

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

72

## 事前学習とは

## ・事前学習の目的

## ・後続タスクに共通して必要な汎用知識（例：読み書きそろばん）を学習し

## その知識を後続タスクに転移する（c.f. Transfer Learning）

## ・後続タスクのための良いパラメータの初期値が得られるとも解釈できる

## ＊後続タスク：最終的に解きたいタスク（要約, 翻訳, 読解…）

[22] Rishi Bommasani et al. (2021), “On the Opportunities and Risks of Foundation Models”より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

73

## 事前学習のパイプライン

## データの収集

## データの前処理

## 訓練

## 評価

## 詳細な解説は

## 本資料“発展的話題”

## のセクションにて

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

74

## データの収集| データの構成要素

## • 例として、昨年リリースされかつデータソースの割合が公開されている

## OLMo2の事例が下図

## • 事前学習用データは、一般的にWEBからの大規模クロールデータ

## コード

## 百科事典

## 論文

## 一般的なWEBサイト

## (ニュース, ブログ, HP)

[12] Allen Institute for AI, Univ. of Washington, NYU (2025), “2 OLMo 2 Furious” より引用し,一部改変

## 数学特化データ

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

75

[13] OpenAI (2025), “gpt-oss-120b & gpt-oss-20b Model Card”

[14] Qwen (2025), “Qwen3 Technical Report”

[12] Allen Institute for AI, Univ. of Washington, NYU (2025), “2 OLMo 2 Furious”

[24] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”, NeurIPS2020 より引用

Llama3.1, DeepSeek-v3はHuggingfaceレポジトリの記載を引用

## データの収集| データの量

## 最近のモデルの事前学習トークン数

## • 1～40兆トークン*のテキストを利用

## *トークン：言語AIが処理することばの単位

## 日本語だと大体1文字1トークン

## • 書籍でいうと（１冊10万トークンとして）

## １兆トークンは約1000万冊に相当

## 参考：東大図書館が1000万冊以上

## 国会図書館が約4800万冊

## トークン数[兆]

## gpt-oss120B

## 数兆

## Llama3.1

## 15~

## DeepSeek-v3

## 14.8

## Qwen3

## 36

## GPT-3

## 0.5

## OLMo 2

## 3.9

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

76

## •

## Quality Filtering

## 分類器やヒューリスティックにより質の低いデータを取り除く

## •

## De-dup

## 近い場所で重複があると学習への悪影響が大きいため、文、文書、データセットなど様々

## な粒度で重複を排除する

## •

## Privacy Reduction

## 個人を特定できる情報を取り除く（＊）

## •

## Tokenization

## （次ページにて説明）

## LLMの事前学習のおいて典型的な前処理のパイプライン

## ＊データセットによって前処理の仕組みは異なります.本資料”発展的話題”も参照.

（＊）Our approach relies on a combination of logistic

classifiers (content tagging) and regular expressions (PII

detection). In practice: We detect and mask email

addresses, phone numbers, and IP addresses.

[25]Luca Soldaini (2023), AI2 Dolma: 3 Trillion Token

Open Corpus for LLMs | AI2 Blog

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

## データの前処理

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

77

## データの前処理| Tokenization：テキストのトークン化

## • トークン化：テキストを”トークン“と呼ばれる最小単位に分割すること

## • トークナイザー：トークン化を行うためのプログラム

## • 例：Byte Pair Encoding (BPE)、SentencePiece

## • 効率的にトークン化したい→ 一般に語彙の出現頻度に基づくアルゴリズ

## ムで実現

## • コーパスから定義したアルゴリズムに従ってトークナイザーが語彙辞書

## を作成した後トークン化を行う（詳細は本資料”発展的話題”にて解説）

## “吾輩は猫である。”

## ↓

## “吾輩”, “は”, “猫”, “で”, “ある”, “。”

## トークン化のイメージ

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

78

## 訓練（事前学習）| Next Token Prediction

## • 学習用のテキストデータを使って、次のトークンの生成確率をひたすら予測

## • 自己教師あり学習の一種

## 吾輩

## 吾輩

## は

## 吾輩

## は

## 猫

## 吾輩

## は

## 猫

## で

## 吾輩

## は

## 猫

## で

## ある

## LLM

## LLM

## LLM

## LLM

## LLM

## P(は|吾輩)

## P(猫|吾輩,は)

## P(で|吾輩,は,猫)

## P(ある|吾輩,は,猫,で)

## P(。|吾輩,は,猫,で,ある)

## 入力

## 予測

## は

## 猫

## で

## ある

## 。

## 正解

## 予測と正解の誤差(交差エントロピー)が

## 小さくなるように学習する

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

79

## 訓練（事前学習）| Next Token Prediction

## • 学習用のテキストデータを使い、次トークンの生起確率をひたすら予測

## • 予測と正解の誤差（交差エントロピー）が小さくなるように学習する

## • つまり事前学習の目的関数としてminimize(交差エントロピー)を用いる

## ＊上記サンプル文単位の交差エントロピーを、ミニバッチ内で

## 各サンプル文毎に計算して平均したものをLossとする

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

80

## 訓練（事前学習）| Next Token Prediction

## • 一般的に1epochのみ学習させる（1～3の範囲）

[28] Hugo Touvron et al. (2023),

“Llama 2: Open Foundation and Fine-Tuned Chat Models” より引用

[23] Hugo Touvron et al. (2023), “LLaMA: Open and Efficient Foundation Language Models” より引用

[27] Guilherme Penedo et al.(2023), “The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only”

より引用

## [23]

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

81

## 訓練（事前学習）| Next Token Prediction

## • 一般的に1epochのみ学習させる（1～3の範囲）

## • 複数epoch学習しすぎると, 過学習となりdegredationするか、差がない

## • モデルサイズが大きくなるほどdegredationの傾向が強くなる

81

[29] Fuzhao Xue et al. (2023), “To Repeat or Not To Repeat: Insights from Scaling LLM under Token-Crisis” より引用(左図)

[30] Niklas Muennighoff et al. (2023), “Scaling Data-Constrained Language Models”より引用(右図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

82

## 訓練（事前学習）| Next Token Prediction

## • 原理的には簡単だが、実際にやってみると難しい

## • 小規模なモデルの訓練だと発生しないが、大規模なモデルでの学習(+複数ノ

## ードでの分散学習)を行うと発生する現象

## •

## 交差エントロピーの発散（Lossのスパイク）

## •

## ハードウェア、ネットワークなど低レイヤでのエラー

82

## 計算する数値フォーマットによっても安定性が変わる（近年はbfloat16が主流）

82

[31] Stas Bekman (2022) The Technology Behind BLOOM Training より引用(左図)

[32] suchenxang (2023), metaseq/projects/OPT/chronicles/OPT175B_Logbook.pdf at main · facebookresearch/metaseq · GitHub より引用(右図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

83

## 訓練（事前学習）| ハイパーパラメータの例

## • Optimizer: Adam[33], AdamW[34]

## • Scheduler: Learning RateのWarmup + Decay

## • 浮動小数点精度：近年はBF16が主流

## • Batch Size: 数百万トークンが一般的

83

83

83

## ミニバッチ内のトークン数

## ＝

## サンプル数× 最大トークン長

サンプル数

サンプルあたりの最大トークン長

[33] Diederik P. Kingma & Jimmy Ba, (2014), “Adam: A Method for Stochastic Optimization”を参考

[34] Ilya Loshchilov & Frank Hutter, (2017), “Decoupled Weight Decay Regularization”, を参考

[23] Hugo Touvron et al. (2023), “LLaMA: Open and Efficient Foundation Language Models” より引用し,一部改変(左下表)

[35] Shikoan’s ML Blog (2021), Cosine DecayとWarmupを同時にこなすスケジューラー（timm）| Shikoan‘s ML Blog より引用し,一部改変(右上図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

84

## 評価| 定量評価（Upstream）

## • 交差エントロピーのValidation Loss:

## •

## Lossが下がっているか(事前学習自体が崩壊していないか)をモニタ

## •

## モデルごとのパフォーマンスの違いを確認する

## •

## Test Lossは論文上では(ほとんど)見ない*事前学習は, 1エポック学習が一般的なので

## Overfitしない前提だから？

## •

## 場合によっては, Training Lossだけで完結していることも多い.

84

[23] Hugo Touvron et al. (2023), “LLaMA: Open and Efficient Foundation Language Models” より引用し,一部改変(左図)

[24] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”,のarXiv版より引用(右図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

85

## 評価| 定量評価（Upstream）

## • 交差エントロピーの様々な呼び方

## •

## 交差エントロピー

## •

## Cross Entropy Loss

## •

## CELoss

## • 式変形したら交差エントロピーと実質同じ指標.

## •

## Perplexity (PPL)

## •

## Bits-Per-Character (BPC)

## •

## Bits-Per-Word (BPW)

85

[7] OpenAI (2023) “GPT-4 Technical Report”より引用し,一部改変(右上図)

[28] Hugo Touvron et al. (2023), “Llama 2: Open Foundation and Fine-Tuned Chat Models” より引用し,一部改変(右下図)

参考：[36] Chip Huyen (2019), Evaluation Metrics for Language Modeling

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

86

[24] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”のarXiv版より一部を抜粋し,改変

## 評価| 定量評価（Downstream）

## • 様々な下流タスク(最終的に解きたいタスク) (*1)で評価

## • In-Context Learning (Zero-shot, Few-shot) (*2)で評価することが多い

## • 事後学習(ファインチューニングやRLHF) (*3)で下流タスク性能は更に向上

## (*1) 本講義の“発展的話題”に評価ベンチマークについての説明あり.

## (*2) Day2を復習してください.

## (*3) Day5,Day7で説明する予定で

## す.

## 下流

## タスク

86

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

87

## 評価| 定性評価（サンプル評価）

## • 事前学習済みLLMを使って, テキストを出力（デコード）してみる

## • デコードには様々な方式が存在する

## •

## Greedy Decoding

## •

## Beam Search

## •

## Random Sampling

87

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

88

## 評価| 事前学習済モデルによるテキストの生成（デコード）方法

## • デコード方式①：Greedy Decoding

## •

## 生起確率が一番高い次のトークンを逐一選んでいく

88

[37] Kaito Sugimoto (2021) テキスト生成におけるdecoding テクニック: Greedy search, Beam search, Top-K, Top-p より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

89

## • デコード方式②：Beam Search

## •

## 高い生起確率となるようなトークン系列を探索して見つける

## 直近だけじゃなくその先まで見て決める

## •

## ただし全系列を探索(Exhaustive Search)すると計算量が爆発

## 事前に決めておいたビームサイズ内で探索する

## 評価| 事前学習済モデルによるテキストの生成（デコード）方法

89

## ビームサイズ=3の場合

[37] Kaito Sugimoto (2021) テキスト生成におけるdecoding テクニック: Greedy search, Beam search, Top-K, Top-p より引用し,一部改変

[38] mm_0824 (2020) ビームサーチ(Beam Search)を理解する| 楽しみながら理解するAI・機械学習入門より引用(右図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

90

## 評価| 事前学習済モデルによるテキストの生成（デコード）方法

## • デコード方式③：Random Sampling

## •

## 次のトークンの生起確率分布に従い, ランダムに選択する.

## •

## Top_p: 上位p％のトークンから選択する. (例) 0.9

## •

## Top_k: 上位k個のトークンから選択する. (例) 10

## •

## Temperature: 0以上の実数(スカラー値). Softmax手前のLogitの分母にかける.

## Temperature = 1だと普通のSoftmaxと同じ.

90

[39] cohere, Temperature より引用

[68] Harshit Sharma (2022), “Softmax Temperature” より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

91

## 評価| 事前学習済モデルによるテキストの生成（デコード）方法

## • 状況により望ましいデコード方式は変わる

## •

## 分類問題を解く場合は, 決定的な解答をするgreedy Decodingが好まれる

## •

## Beam Searchは機械翻訳のタスクを解くときに見ることが多い

## •

## 長文生成をする場合は, random samplingを行うことが多い

91

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

92

## 目次

## • 言語モデルとは何か？

## • Transformer

## • 事前学習

## • 発展的話題

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

93

## 発展的話題

## データ

## モデル

## 学習

## 評価、分析

## •

## 主要なデータセット

## •

## データ処理(クレンジング、トークナイズ)

## •

## 主要なモデル

## •

## アーキテクチャの構成要素

## •

## Attention

## •

## 目的関数

## •

## 評価

## •

## 分析

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

94

## 発展的話題

## データ

## モデル

## 学習

## 評価、分析

## •

## 主要なデータセット

## •

## データ処理(クレンジング、トークナイズ)

## •

## 主要なモデル

## •

## アーキテクチャの構成要素

## •

## Attention

## •

## 目的関数

## •

## 評価

## •

## 分析

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

95

## 学習に用いるデータセットの変遷

## “A Survey of Large Language Models”, 2023

## ■主要なモデルの学習データの構成

## • GPT-2ではWebページのコーパス(約40GB)のみで学習を行っていた

## • 近年はCodeや会話データなど多様なデータで学習するモデルが増加

95

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

96

## C4 | フィルタリングされた巨大なWebページ英語コーパス

## “Exploring the Limits of Transfer Learning with a Unified Text-to-Text

## Transformer”, 2019

## • Common Crawl…一般に公開されているウェブアーカイブをスクレイピング

## して収集したデータセット。月当たり約20TBのデータ量が存在。

## • C4… 2019年4月のWeb抽出データの中から、言語判定の結果が英語となり、

## 複数のデータフィルタリング、クレンジングを経て集められたデータセット

## ■C4由来のデータセットと既存のデータセットで学習した場合の性能の比較

## C4由来の

## データセット

## 既存の

## データセット

[41] Colin Raffel et al. (2020), “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer” より引用し,一部改変

96

[41] Colin Raffel et al. (2020), “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer” より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

97

## 多言語にわたって収集されたテキストコーパス

## “Unsupervised Cross-lingual Representation Learning at Scale”, ACL2020

## “mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer”, NAACL2021

## • 100言語に渡って、収集され

## たテキストコーパス

## • 各言語で訓練したモデルと

## fastTextを用いて

## フィルタリングを行う

## CC-100

## • 前述したC4と同様に、言語

## 判定したのちに、フィルタリ

## ングを行った101言語を含む

## テキストコーパス

## mC4

97

[42] Alexis Conneau et al. (2020), “Unsupervised Cross-lingual Representation Learning at Scale”, ACL2020 より引用

[43] Linting Xue et al. (2021), “mT5: A massively multilingual pre-trained text-to-text transformer”, ACL2021 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

98

## The Pile | 多様なソースを含む英語コーパス

## “The Pile: An 800GB Dataset of Diverse Text for Language Modeling”, 2020

## • the Pile…22の多様な

## ソースを組み合わせた

## 言語モデリング用の

## 825.18GBのデータセット

## 学習データセットの多様性を

## 高めることで、

## クロスドメインの性能を期待

## • the Pileで学習したモデルが

## CC-100やCommon Crawlで

## 学習したモデルの性能を

## 上回る

98

[44] Leo Gao et al. (2020), “The Pile: An 800GB Dataset of Diverse Text for Language Modeling” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

99

[25] Luca Soldaini et al. (2023) “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research” より引用

## Dolma：最大級の混合事前学習用公開データセット

## “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model

## Pretraining Research”, 2023

## • Dolma…

## ウェブコンテンツ、学術出版

## 物、コード、書籍、百科事典

## の多様な組み合わせからなる

## 5334GB(3T tokens)の

## 公開データセット

## • 過去の研究も踏まえ、

## データ処理のベストプラクテ

## ィス(後述)に従ったと言及

99

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

100

## Dolmaにおけるテキストデータ処理プロセス(1)

## “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model

## Pretraining Research”, 2023

## 1. fastTextの言語識別モデ

## ルを使用し、

## 英語である可能性が50%以

## 上の文書を保持

## 2. 出典のURLを元に

## 重複を削除する

## 3. 句読点で終わらない

## 全ての段落を

## フィルタリングする

100

[25] Luca Soldaini et al. (2023) “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research” より引用、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

101

## Dolmaにおけるテキストデータ処理プロセス(2)

## “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model

## Pretraining Research”, 2023

## 4. 有害または猥褻なである可

## 能性が60%以上と判定された

## ものを削除

## 個人情報も正規表現で検出し

## マスクする

## 5. 文書内で重複する段落を

## 削除する

## 6. 評価セットに

## 含まれる13トークン以上の

## 段落を学習セットから

## 除去する

101

[25] Luca Soldaini et al. (2023) “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research” より引用、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

102

## ■補足| 事前学習用データセットの前処理の違い

## “AI2 Dolma: 3 Trillion Token Open Corpus for Language Model

## Pretraining”, 2023

102

[25] Luca Soldaini et al. (2023) “Dolma: An Open Corpus of 3 Trillion Tokens for Language Model Pretraining Research” より引用、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

103

## FineWeb | WEBデータに特化したさらに大きなデータセット

## “The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale”

## • Llamaアーキテクチャの小規模モデルを70個以上学習して行ったアブレーシ

## ョン実験による経験的なベストプラクティスを発見

## • CommonCrawlから精製した18.5 T tokensからなるデータセット

## •

## WEBからの精製に特化することでより大きなデータセットを整備できる

## （c.f. RefinedWeb（5T）、RedPajama-v2（英仏西独伊の合計で30T））

103

[40] Hugging Face (2024) The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scaleのブログより引用

[27] Guilherme Penedo et al.(2023), The RefinedWeb Dataset for Falcon LLM:Outperforming Curated Corpora with Web Data, and Web Data Only

[45] Weber, et. Al. (2024), RedPajama: an Open Dataset for Training Large Language Models

## 小規模モデルでの実験で他の公開

## データセットより高い学習効率を実現

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

104

## FineWeb | WEBデータに特化したさらに大きなデータセット

## “The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale”

## •

## 派生データセット

## •

## FineWeb-edu

## 分類器を使用した、FineWebの「教育的」なサブセット1.3T tokens

## •

## FineWeb 2

## “FineWeb2: One Pipeline to Scale Them All -- Adapting Pre-Training Data Processing to

## Every Language”

## 多言語版FineWeb

## 日本語は331Billion words含まれており比較的豊富

104

[40] Hugging Face (2024) The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale

[69] Hugging Face, EPFL (2025) FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language

図はFineWeb-eduのHFレポジトリより引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

105

## テキストのトークン化

## 代表手法:Byte Pair Encoding (BPE)

## •

## テキストをサブワード(単語よりも細かい塊)に分割

## •

## トークナイザーの語彙作成方法は右図を参照.

## •

## 語彙サイズ（基本語彙数＋マージ数）は

## ハイパーパラメータ

## •

## GPT、GPT-2、RoBERTa、BART、DeBERTaなど多

## くのTransformerで用いられる

## •

## 絵文字などの処理

## •

## コーパスにない文字を使用する場合、その文字

## は<unk>に変換される

## •

## そのため、多くのNLPモデルが絵文字でコンテ

## ンツを分析するのが苦手としている

## •

## GPT-2とRoBERTaのトークナイザは、これに

## 対処するためにbyteレベルでBPEをおこなう

## 例）コーパスが次の５つの単語でできていると仮定

## ‘hug’, ‘pug’, ‘pun’, ‘bun’, ‘hugs’

## 1. それぞれの単語の出現回数をカウント

## (‘hug’, 10), (‘pug’, 5), (‘pun’, 12),

## (‘bun’, 4), (‘hugs’, 5)

## 2. 単語を文字に分割

## (‘h’ ‘u’ ‘g’, 10), (‘p’ ‘u’ ‘g’, 5), (‘p’ ‘u’ ‘n’, 12),

## (‘b’ ‘u’ ‘n’, 4), (‘h’ ‘u’ ‘g’ ‘s’, 5)

## 3. 最も頻出の隣接ペア(‘u’, ’g’) を(‘ug’) にマージ

## (‘h’ ‘ug’, 10), (‘p’ ‘ug’, 5), (‘p’ ‘u’ ‘n’, 12),

## (‘b’ ‘u’ ‘n’, 4), (‘h’ ‘ug’ ‘s’, 5)

## 4. 希望の語彙数まで頻度の高い組のマージを繰り返す

## (‘h’ ’ug’, 10), (‘p’ ‘ug’, 5), (‘p’ ‘un’, 12),

## ('b' 'un', 4), (‘h’ ’ug' 's', 5) …

[46] Hugging Face (2025), Hugging Face LLM Course のChapter6.5より例を引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

106

## BPE以外のサブワード単位でのトークン化

## その他のトークナイザ

## •

## BPEと違い、隣接ペアの２要素の

## 出現頻度が低いペア(その組み合わ

## せ以外であまりないペア)優先的に

## マージ

## Score =

## 隣接ペア(a,b)の出現回数

## aの出現回数× bの出現回数

## •

## 例１：(un, ##able)

## 各要素は他の単語でも頻出する

## 可能性大（このままにしたい）

## •

## 例２：(hug, ##ging)

## 各要素は他で頻出ではないので

## マージしてOK

## •

## BERT、ELECTRAなどで使用

## WordPiece

## •

## 事前の単語分割を必要とせず、そ

## のままのテキストを分割する

## •

## 語彙の集合にスペースを追加し、

## BPEやUnigramなどのアルゴリズ

## ムを用いて語彙をマージ

## •

## 日本語など英語以外の様々な言語

## でも容易にトークナイザを作成で

## き、サブワード分割アルゴリズム

## も選択可能

## •

## T5、ALBERTなどで使用

## SentencePiece

106

[46] Hugging Face (2025), Hugging Face LLM Course のChapter6.6より例を引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

107

## ■補足| ByT5：トークンフリーな言語モデル

## “ByT5: Towards a token-free future with pre-trained byte-to-byte

## models”, 2021

## 方法

## テキスト列をトークンで表現せ

## ず、代わりに文字コード(UTF-

## 8)で読み込んだバイト列で表現

## 結果

## サブワードでトークナイズし、

## 学習を行ったモデル(mT5)に

## 匹敵する性能を示す

107

[47] Linting Xue et al. (2022), “ByT5: Towards a token-free future with pre-trained byte-to-byte models” ACL2022 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

108

## 発展的話題

## 108

## データ

## モデル

## 学習

## 評価、分析

## •

## Attention

## •

## 目的関数

## •

## 評価

## •

## 分析

## •

## 主要なデータセット

## •

## データ処理(クレンジング、トークナイズ)

## •

## 主要なモデル

## •

## アーキテクチャの構成要素

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

109

## Transformerの分類

## Encoder-only

## Encoder-Decoder

## BERT、RoBERTaなど

## BART、T5など

## 認識系

## （クラス分類）

## テキスト

## 生成系

## Decoder-only

## GPT、Llamaなど

## テキスト

## 生成系

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

110

## Transformerの分類

## Encoder-only

## Encoder-Decoder

## BERT、RoBERTaなど

## BART、T5など

## 認識系

## （クラス分類）

## テキスト

## 生成系

## Decoder-only

## テキスト

## 生成系

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

## GPT、Llamaなど

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

111

## BERT：複数タスクでSoTAを達成した双方向型事前学習モデル

## “BERT: Pre-training of Deep Bidirectional Transformers for Language

## Understanding”, NAACL2019

## 方法

## •

## TransformerのEncoderを

## 24層積み重ねた

## 双方向言語モデル

## •

## 事前学習において

## 穴埋めタスクと次の文予測

## タスクを学習し、

## 目的とするタスクのデータ

## セットでファインチューニ

## ングすることで性能を発揮

## 結果

## •

## 11個のNLPタスクでSoTA

## [CLS] my dog is cute [SEP] he likes [MASK] ##ng [SEP]

## IsNext my dog is cute [SEP] he likes play ##ng [SEP]

## 穴埋め

## (MLM)

## 次の文予測

## (NSP)

111

[48] Jacob Devlin et al. (2019), “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding”, ACL2019 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

112

## RoBERTa：BERTを改良し性能向上

## “RoBERTa: A Robustly Optimized BERT Pretraining Approach”, 2019

## 方法

## •

## BERTと同じアーキテクチャで一

## 部の要素を変更

## – データセットサイズを

## 13GB→160GB

## – バッチサイズを256→8K

## – NSPを使用しない

## – マスクを動的に行う

## 結果

## •

## GLUEやSQuADでBERTを

## 上回る性能

112

[49] Yinhan Liu et al. (2019), “RoBERTa: A Robustly Optimized BERT Pretraining Approach”より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

113

## ALBERT：パラメータ共有により、学習を高速化

## “ALBERT: A Lite BERT for Self-supervised Learning of Language

## Representations”, ICLR2020

## 方法

## •

## 層間でパラメータを共有する

## ことで、BERT-largeと同様の

## アーキテクチャと比較して、

## パラメータが18倍少なくなり、

## 1.7倍高速に学習が可能に

## 結果

## •

## ALBERT-xxlargeにおいてBERT-

## largeよりも少ないパラメータ数

## であるにも関わらず、GLUE、

## SQuADでSoTA

113

[50] Zhenzhong Lan et al. (2020), “ALBERT: A Lite BERT for Self-supervised Learning of Language Representations” ICLR2020 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

114

## Transformerの分類

## Encoder-only

## Encoder-Decoder

## BERT、RoBERTaなど

## BART、T5など

## 認識系

## （クラス分類）

## テキスト

## 生成系

## Decoder-only

## テキスト

## 生成系

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

## GPT、Llamaなど

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

115

## BART：双方向エンコーダーと自己回帰型デコーダーの組み合わせ

## “BART: Denoising Sequence-to-Sequence Pre-training for Natural Language

## Generation, Translation, and Comprehension”, 2019

## 方法

## •

## BERTのような双方向エンコーダ

## ーとGPTのような自己回帰型デ

## コーダーを組み合わせたモデル

## •

## ランダムに入力文書の一部を

## 破損させ、その再構成を行う

## 複数のタスクの組み合わせで

## 事前学習を行う

## 結果

## •

## CNN/DailyMail XSumと

## いったタスクでSoTA

115

[51] Mike Lewis et al. (2020), “BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

116

## T5：全てのタスクをText-to-Textと扱うEncDecモデル

## “Exploring the Limits of Transfer Learning with a Unified Text-to-Text

## Transformer”, 2019

## 方法

## •

## 多くの自然言語処理タスクを

## Text-to-Textの形に変換し、

## 統一したフレームワークで

## 学習を行う

## •

## 事前学習においては、

## 入力文書の一部をランダムに

## 特殊トークンに置き換え、

## 置き換え元のトークンを

## 予測するタスクで学習を行う

## 結果

## •

## GLUEやSuperGLUEといった

## タスクでSoTA

116

[41] Colin Raffel et al. (2020), “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

117

## Transformerの分類

## Encoder-only

## Encoder-Decoder

## BERT、RoBERTaなど

## BART、T5など

## 認識系

## （クラス分類）

## テキスト

## 生成系

## Decoder-only

## テキスト

## 生成系

[6] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用し、一部改変

## GPT、Llamaなど

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

118

## GPT-3：さらにスケールさせたDec-onlyモデル

## • “Language Models are Few-Shot Learners”, 2020

## 方法

## •

## GPT-2の約120倍の

## パラメータ数を持ったモデルを

## 約14倍のデータで学習を行う

## •

## タスクに関する説明や

## 数ショットの例を入力に加える

## ことで、タスクが解けるように

## なる文脈内学習(In-context

## Learning)が可能に

## 結果

## •

## 数ショットの設定で既存のSoTAに

## 匹敵、あるいは上回る性能を確認

## •

## あまりの性能により、モデルの

## 公開を行わずAPIの公開に止める

118

[24] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”, NeurIPS2020 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

119

## ■補足|近年公開されるモデルはDec-onlyのモデルが多い

## “A Survey of Large Language Models”, 2023

119

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

120

## 正規化の位置に関して

## “A Survey of Large Language Models”, 2023

## Post Norm

## Pre Norm

## Sandwich

## Norm

## •

## 元々のTransformer同様、

## 残差接続後に正規化を配置

## •

## 出力層付近で勾配が大きくなり

## 学習が不安定になる傾向

## •

## 各サブレイヤの前と最終予測の

## 前に正規化を配置

## •

## 性能が低くなるが学習の安定性

## から、採用されることが多い

## •

## 特に残差接続の前で追加の

## 正規化を配置

## •

## 学習が破綻する場合も存在

## 数式表現

## 詳細

120

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

121

## 位置表現に関して

## “より良いTransformerをつくる”, 2022 参考に作成

## 絶対位置表現

## 相対位置表現

## 各トークンの絶対的な位置を

## 表す何らかの表現

## (e.g.sin波/cos波)を

## 入力の表現に加える

## トークン同士の相対的な距離

## をAttention計算時に活用する

## •

## 入力の内容とは独立した表現な

## ので、計算速度が速い

## •

## 未知の長さの系列の入力に弱い

## •

## トークン同士の相対的な位置を

## 利用するため、

## 未知の系列長でも頑健性が高い

## •

## 入力に固有の値を取るため、

## 追加の計算が必要

## 概要

## 詳細

121

[52] 清野舜(2022), より良いTransformerをつくる- Speaker Deck を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

122

## ALiBi：距離に線形なバイアスを組み込んだ相対位置埋め込み

## “Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation”, ICLR2022

## 方法

## •

## Attentionスコア計算時に

## KeyとQueryの相対的な距離

## に対して線形なペナルティを

## 加える

## •

## 近くのトークン間より

## 遠くのトークン間の方が

## Attentionスコアが低下する

## 結果

## •

## 絶対位置表現より性能が良い

## •

## 外挿性能も良い

122

[53] Ofir Press et al. (2021), “Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

123

## 近年のLLMモデル構造

## • 近年のモデルはAttention/Feed Forward/Normalizationに改良がされつつ

## ある

## •

## Potisional Embedding

## •

## RoPE

## •

## Attention

## •

## Grouped Query Attention

## •

## Sliding Window Attention

## •

## Multi-head Latent Attention

## •

## Feed Forward

## •

## SwiGLU

## •

## Mixture of Experts

## •

## Others

## •

## RMSNorm

## • 最新モデルのアーキテクチャの解説については以下を参照

## The Big LLM Architecture Comparison [70]

## https://magazine.sebastianraschka.com/p/the-big-llm-architecture-

## comparison

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

124

## 発展的話題

## データ

## モデル

## 学習

## 評価、分析

## •

## 主要なモデル

## •

## アーキテクチャの構成要素

## •

## 評価

## •

## 分析

## •

## 主要なデータセット

## •

## データ処理(クレンジング、トークナイズ)

## •

## Attention

## •

## 目的関数

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

125

## Sparse Attention：計算箇所を限定して効率的にAttentionを計算

## “Big Bird: Transformers for Longer Sequences”, NeurIPS 2020

## 問題意識

## 従来のAttentionでは

## 系列長に対し2乗の

## 計算複雑性がかかる

## 方法

## 全てのトークンに対して

## Attentionを計算するので

## なく、局所的に設定した

## トークンで学習を行い

## 計算量を削減

## 類似アイディア：[Iz Beltagy et al. 2020] “Longformer: The Long-Document Transformer” [55]

125

[54] Manzil Zaheer et al. (2020), “Big Bird: Transformers for Longer Sequences” NeurIPS2020 より引用(図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

126

## Grouped-Query Attention：KeyとValueを複数のヘッドで共有

## “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints”, 2023

## 問題意識

## Multi-headのAttentionでは

## デコードする際に全ての

## KeyとValueを読み込む

## 必要があり、推論速度の

## ボトルネックになる

## 方法

## KeyとValueをいくつか(Group-

## query)あるいは

## 一つ(Multi-query)のヘッドで

## 共有してメモリ負荷を削減し、推論

## 速度を向上させる

## Llama3などで採用されている

126

[56] Joshua Ainslie et al. (2023), “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

127

## UniLM：Attentionのマスク位置を変え、複合的な目的関数を設定

## “Unified Language Model Pre-training for Natural Language Understanding and Generation”, NeurIPS2019

## 方法

## •

## Attentionのマスクされたした

## 領域を変化させることで、

## 双方向言語モデリング、

## 単方向言語モデリング、

## 配列間言語モデリングを

## 組み合わせた複合的な

## 目的関数で事前学習を行う

## 結果

## •

## GLUEのような識別タスクで

## BERTに匹敵する性能を示し

## ながら、CNN/DMのような

## 言語生成タスクでSoTA

127

[57] Li Dong et al. (2019), “Unified Language Model Pre-training for Natural Language Understanding and Generation” NeurIPS2019 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

128

## UL2：複数のタスクを設定した統一的な目的関数での事前学習

## “UL2: Unifying Language Learning Paradigms”, 2022

## 方法

## •

## T5のような欠落したトークン

## の予測(R-Denoising,X-

## Denoising)とGPTのような連

## 続的なトークンの予測を組み合

## わせたMoD（Mixture-of-

## Denoisers）と呼ばれる統一的

## な目的関数で学習

## •

## MoDを継続的な事前学習に

## 用いるUL2R(UL2 Repair)

## という訓練方法も後に提案

## 結果

## •

## EncDecとDecの両方の

## アーキテクチャで

## バランス良く性能の向上を確認

128

[58] Yi Tay et al. (2022), “UL2: Unifying Language Learning Paradigms” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

129

## 発展的話題

## データ

## モデル

## 評価、分析

## 学習

## •

## 主要なモデル

## •

## アーキテクチャの構成要素

## •

## Attention

## •

## 目的関数

## •

## 主要なデータセット

## •

## データ処理(クレンジング、トークナイズ)

## •

## 評価

## •

## 分析

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

130

## 評価対象の広がり

## 主なデータセット

## 自然言語理解

## ドメイン知識

## 倫理性、信頼性

## ツール活用

## 評価対象

## •

## 入力系列の理解を行うタスク

## •

## 従来の主な評価の対象

## •

## 数学や科学、医学など

## 解答に専門的な知識を要するタスク

## •

## 社会的なバイアスを含まないか、

## どのような特性を持っているかを

## 検証するタスク

## •

## 外部のAPIなどを活用して

## 解答を作成できるか検証するタスク

## 概要

## GLUE，SuperGLUE

## SQuAD, MMLU

## MATH,

## MultiMedQA.

## APPS, CUAD

## FLASK, TrustGPT,

## TruthfulQA

## ToolBench

130

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

131

## FLASK：言語モデルの総合的な性能を評価するベンチマーク

## “FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets”, 2023

## • LLMに必要なスキルを

## 定義し、モデルの振る舞い

## に対して人間またはモデル

## によるスコアリングを

## 行うベンチマーク

## • 主に4つの能力（論理的思

## 考、背景知識、問題解決能

## 力、指示追従性）からなる

## 評価枠組みを構築し、これ

## らを12の詳細なスキル項目

## に細分化

131

[60] Seonghyeon Ye et al. (2023), “FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

132

## Attentionによる可視化分析

## “Attention in Natural Language Processing”, 2019

## •

## Attentionの大小は度々可視化され、それをAttention mapと呼ぶ。

## 上図のハイライトされているものはAttentionスコアが高い単語である

## •

## 一見Attentionは単語の重要性を表しているように見える一方で、

## Attentionには説明能力はないのではとする立場の論文も複数存在

132

[61] Andrea Galassi et al. (2019), “Attention in Natural Language Processing” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

133

## Attention Rollout / Flow：Attention mapから入力への寄与を計算

## “Quantifying Attention Flow in Transformers”, ACL2020

## • 従来のAttentionでは複数の層を経由して情報がやり取りされるので、

## Attention mapそのままを各状態の入力に対する寄与として解釈するには信頼性が不足

## • Attention Rolloutでは、自分より前にある層のAttention mapを掛け合わせていく

## • Attention Flowでは、各層のAttentionをフローネットワークとして解釈し入力トークン

## への注意の近似を行う

133

[62] Samira Abnar & Willem Zuidema (2020), “Quantifying Attention Flow in Transformers” ACL2020 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

134

## ■補足| 任意のタスクでAttentionを必ず使うべきとは限らない

## “Are Pre-trained Convolutions Better than Pre-trained Transformers?”, ACL2021

## •

## 現在において事前学習と

## Transformerはスタンダード

## になっているが、これはセッ

## トで意味があるのか？

## •

## CNNでも事前学習効果あり

## •

## 一部のタスクでCNNモデルが

## T5を上回る性能を発揮

## •

## CNNが常にTransformerの代

## 替となるわけではないが、事

## 前学習というパラダイムシフ

## トとアーキテクチャの変遷は

## 分けて考えるべきと主張

134

[63] Yi Tay et al. (2021), “Are Pre-trained Convolutions Better than Pre-trained Transformers?” ACL2021 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

135

## ■補足| ConvolutionとSelf Attentionの関係

## “On the Relationship between Self-Attention and Convolutional Layers”, ICLR2020

## Filter：

## パラメータ

## （静的）

## 範囲：

## 局所

## Filter：

## 入力依存（動的）

## 範囲：

## 大域

## ※ただし相対位置表現

## を使うとMulti-Head

## Self-AttentionはConv

## を内包

135

[64] Jean-Baptiste et al. (2020), “On the Relationship between Self-Attention and Convolutional Layers” ICLR2020 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

136

## 敵対的攻撃、敵対的防御：言語モデルの弱点に関する分析方法

## “What are adversarial examples in NLP?”, 2020

## 問題意識

## 人間に対しては些細な影響し

## か与えないような摂動でも、

## ニューラルネットは大きく

## 影響を受けてしまう場合が

## 存在している

## 方法

## 入力の一部を編集させた結果

## モデルの性能を劣化させる

## 攻撃を検証するとともに、

## その攻撃による失敗を防ぐ防

## 御方法を検討する

## ■極性分析での敵対的攻撃の例

136

[65] Jack Morris (2020), “What are adversarial examples in NLP?” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

137

## プロービング：言語モデルが内部的に獲得する能力の分析手法

## 品詞分類能力についてのプロービングの例

## 問題意識

## 言語モデルのタスクの性能は出力に

## よって評価できるが、言語モデルが

## 内部的に獲得している能力は

## 出力によっては簡単に評価できない

## 方法

## ある入力を与えた場合の言語モデルから

## 得られる埋め込み表現から

## 特定のタスク(左図では品詞分類)を行う

## 分類器(プローブ)を訓練した場合の

## タスクの成功率から埋め込み表現に

## そのタスクを示す表現がエンコードされている

## かを検証する

## 近年はモデルの埋め込み表現に介入を行い、

## 出力への因果関係を調査する場合も多い

## 言語モデル

## 入力：I am travelling the world

## 埋め込み表現

## 分類器(プローブ)

## 品詞タグ：NN(名詞)

## 訓練

137

[66] Yonatan Belinkov (2022), “Probing Classifiers: Promises, Shortcomings, and

Advances” ACL2022 を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

138

## 本日のまとめ

## 大規模言語モデル（LLM）の事前学習について紹介

## 1. 言語モデルにおけるTransformerの位置づけ

## ・Transformerはニューラル言語モデルの一つとして扱われる

## ・RNN型言語モデルが抱えていた課題を解決した

## 3. LLMの事前学習

## ・大規模コーパスによる学習を行うことで、モデルの汎用性を高めている

## ・Next Token Predictionという自己教師あり学習により最適化する

## 2. LLMで主流となっているTransformerモデル構造

## ・Self-Attention機構を持つモデル構造であり1ステップで全単語情報と接続できる

## ・課題①の解決: 単語間の長距離依存性が把握できるようになった

## ・課題②の解決: 誤差逆伝播の計算ステップが文長に非依存となり学習安定高速化

## 4. 発展的話題

## ・データ, モデル, 学習, 評価分析についての発展的な話題を解説

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 補足資料

139

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

140

## モデルごとの学習方法の違い

## “A Survey of Large Language Models”, 2023

140

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

141

## モデルごとの細かな要素の違い

## “A Survey of Large Language Models”, 2023

141

[26] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

142

## Accessibility of Models

## APIのみ

## 公開＆巨大

## 非公開

142

[67] Percy Liang (2022), “Holistic Evaluation of Language Models” より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

143

## Reference

[1]

岡崎直観(2023), 大規模言語モデルの驚異と脅威- Speaker Deckアクセス日: 2025/10/1

[2]

Ilya Sutskever et al. (2014), “sequence to sequence learning with neural networks”, NeurIPS2014

[3]

Tomáš Mikolov, et al. (2010), “recurrent neural network based language model”, Proc. Interspeech 2010, 1045-1048

[4]

Dzmitry Bahdanau et al. (2014), “Neural machine translation by jointly learning to align and translate”, arXiv:1409.0473

[5]

Masaki Hayashi (2022), Transformer とseq2seq with attention の違いは？系列変換モデル【Q and A 記事】| CVMLエキスパートガイドアクセス日: 2025/10/1

[6]

Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017

[7]

OpenAI (2023) “GPT-4 Technical Report”, arXiv:2303.08774

[8]

OpenAI (2025), “GPT-5 System Card”アクセス日: 2025/10/1

[9]

OpenAI (2025), “GPT-5 が登場” アクセス日: 2025/10/1

[10]

Google (2025), “Gemini 2.5 tech report” アクセス日: 2025/10/1

[11]

OpenAI (2024), “Learning to Reason with LLMs”

[12]

Allen Institute for AI, Univ. of Washington, NYU (2025), “2 OLMo 2 Furious”, arXiv: 2501.00656

[13]

OpenAI (2025), “gpt-oss-120b & gpt-oss-20b Model Card ”, arXiv: 2508.10925

[14]

Qwen (2025), “Qwen3 Technical Report” , arXiv: 2505.09388

[15]

Shraddha Anala (2020), ”A Guide to Word Embedding. What are they? How are they more useful… | by Shraddha Anala | Towards Data Science”

アクセス日: 2025/10/1

[16]

John Hewitt, Natural Language Processing with Deep Learning CS224N/Ling284 アクセス日:2025/10/1

[17]

Raimi Karim (2019) Illustrated: Self-Attention. A step-by-step guide to self-attention… | by Raimi Karim | Medium,

https://medium.com/data-science/illustrated-self-attention-2d627e33b20a アクセス日:2025/9/3

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

144

## Reference

[18]

Jay Alammar (2018) The Illustrated Transformer – Jay Alammar – Visualizing machine learning one concept at a time.

https://jalammar.github.io/illustrated-transformer/ アクセス日:2023/11/19

[19]

Mor Geva et al. (2021), “Transformer Feed-Forward Layers Are Key-Value Memories”, Proceedings of the 2021 Conference on Empirical Methods in Natural Language

Processing, pages 5484–5495

[20]

Kaiming He et al. (2016), “Deep Residual Learning for Image Recognition”,2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR) pages 770-778

[21]

Jimmy Lei Ba et al. (2016), "Layer Normalization”, arXiv:1607.06450

[22]

Rishi Bommasani et al. (2021), “On the Opportunities and Risks of Foundation Models”, arXiv:2108.07258

[23]

Hugo Touvron et al. (2023), “LLaMA: Open and Efficient Foundation Language Models”, arXiv:2302.13971

[24]

Tom Brown et al. (2020), “Language Models are Few-Shot Learners”, NeurIPS2020（図中のfigureはarXiv版より引用）

[25]

Luca Soldaini (2023), AI2 Dolma: 3 Trillion Token Open Corpus for LLMs | AI2 Blog, https://blog.allenai.org/dolma-3-trillion-tokens-open-llm-corpus-9a0ff4b8da64

アクセス日:2023/11/19

[26]

Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models”, arXiv:2303.18223

[27]

Guilherme Penedo et al.(2023), “The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only” arXiv: 2306.01116

[28]

Hugo Touvron et al. (2023), "Llama 2: Open Foundation and Fine-Tuned Chat Models” arXiv:2307.09288

[29]

Fuzhao Xue et al. (2023), “To Repeat or Not To Repeat: Insights from Scaling LLM under Token-Crisis”, arXiv:2305.13230

[30]

Niklas Muennighoff et al. (2023), “Scaling Data-Constrained Language Models”, arXiv:2305.16264

[31]

Stas Bekman (2022) The Technology Behind BLOOM Training https://huggingface.co/blog/bloom-megatron-deepspeed アクセス日: 2023/11/19

[32]

suchenxang (2023), metaseq/projects/OPT/chronicles/OPT175B_Logbook.pdf at main · facebookresearch/metaseq · GitHub,

https://github.com/facebookresearch/metaseq/blob/main/projects/OPT/chronicles/OPT175B_Logbook.pdf アクセス日:2023/11/19

[33]

Diederik P. Kingma & Jimmy Ba, (2014), “Adam: A Method for Stochastic Optimization”, arXiv:1412.6980

[34]

Ilya Loshchilov & Frank Hutter, (2017), “Decoupled Weight Decay Regularization”, arXiv:1711.05101

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

145

## Reference

[35]

Shikoan’s ML Blog (2021), Cosine DecayとWarmupを同時にこなすスケジューラー（timm）| Shikoan's ML Blog, https://blog.shikoan.com/?s=Cosine

アクセス日:2023/11/19

[36]

Chip Huyen (2019) Evaluation Metrics for Language Modeling, https://thegradient.pub/understanding-evaluation-metrics-for-language-models/

アクセス日:2023/11/19

[37]

Kaito Sugimoto (2021) テキスト生成におけるdecoding テクニック: Greedy search, Beam search, Top-K, Top-p https://zenn.dev/hellorusk/articles/1c0bef15057b1d

アクセス日:2023/11/19

[38]

mm_0824 (2020) ビームサーチ(Beam Search)を理解する| 楽しみながら理解するAI・機械学習入門https://data-analytics.fun/2020/12/16/understanding-beamsearch/

アクセス日:2023/11/19

[39]

cohere, Temperature,  https://docs.cohere.com/docs/temperature, アクセス日:2023/12/1

[40]

Hugging Face (2024) “The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale”, arXiv:2406.17557

[41]

Colin Raffel et al. (2020), “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer”,

The Journal of Machine Learning Research, Volume 21, Issue 1,

Article No.: 140, pp 5485–5551

[42]

Alexis Conneau et al. (2020), “Unsupervised Cross-lingual Representation Learning at Scale”,

Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 8440–8451

[43]

Linting Xue et al. (2021), “mT5: A massively multilingual pre-trained text-to-text transformer”,

Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 483–498

[44]

Leo Gao et al. (2020), “The Pile: An 800GB Dataset of Diverse Text for Language Modeling”, arXiv:2101.00027

[45]

Weber, et. Al. (2024), “RedPajama: an Open Dataset for Training Large Language Models“, NeurIPS2024

[46]

Hugging Face (2025 Hugging Face LLM Course アクセス日: 2025/10/1

[47]

Linting Xue et al. (2022), “ByT5: Towards a token-free future with pre-trained byte-to-byte models”

Transactions of the Association for Computational Linguistics, vol. 10, pp. 291–306

[48]

Jacob Devlin et al. (2019), “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding”, Proceedings of NAACL-HLT 2019, pages 4171–4186

[49]

Yinhan Liu et al. (2019), “RoBERTa: A Robustly Optimized BERT Pretraining Approach”, arXiv:1907.11692

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

146

## Reference

[50]

Zhenzhong Lan et al. (2020), “ALBERT: A Lite BERT for Self-supervised Learning of Language Representations” ICLR2020

[51]

Mike Lewis et al. (2020), “BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension” Proceedings of the

58th

Annual Meeting of the Association for Computational Linguistics, pages 7871–7880

[52]

清野舜(2022), より良いTransformerをつくる- Speaker Deck https://speakerdeck.com/butsugiri/yoriliang-itransformerwotukuru アクセス日: 2023/11/19

[53]

Ofir Press et al. (2021), “Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation” arXiv:2108.12409

[54]

Manzil Zaheer et al. (2020), “Big Bird: Transformers for Longer Sequences” NeurIPS2020

[55]

Iz Beltagy et al. (2020), “Longformer: The Long-Document Transformer”, arXiv:2004.05150

[56]

Joshua Ainslie et al. (2023), “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints” arXiv:2305.13245

[57]

Li Dong et al. (2019), “Unified Language Model Pre-training for Natural Language Understanding and Generation” NeurIPS2019

[58]

Yi Tay et al. (2022), “UL2: Unifying Language Learning Paradigms” arXiv:2205.05131

[59]

Yupeng Chang et al. (2023), “A Survey on Evaluation of Large Language Models” arXiv:2307.03109

[60]

Seonghyeon Ye et al. (2023), “FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets” arXiv:2307.10928

[61]

Andrea Galassi et al. (2019), “Attention in Natural Language Processing” arXiv:1902.02181

[62]

Samira Abnar & Willem Zuidema (2020), “Quantifying Attention Flow in Transformers” Proceedings of the 58th Annual Meeting of the Association for Computational

Linguistics, pages 4190–4197

[63]

Yi Tay et al. (2021), “Are Pre-trained Convolutions Better than Pre-trained Transformers?” Proceedings of the 59th Annual Meeting of

the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, pages 4349–4359

[64]

Jean-Baptiste et al. (2020), “On the Relationship between Self-Attention and Convolutional Layers” ICLR2020

[65]

Jack Morris (2020), “What are adversarial examples in NLP?”, https://towardsdatascience.com/what-are-adversarial-examples-in-nlp-f928c574478e

アクセス日: 2023/11/19

[66]

Yonatan Belinkov (2022), “Probing Classifiers: Promises, Shortcomings, and Advances” Computational Linguistics, Volume 48, Issue 1 - March 2022 pages 207-119

[67]

Percy Liang (2022), “Holistic Evaluation of Language Models” arXiv:2211.09110

[68]

Harshit Sharma (2022), “Softmax Temperature”

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

147

## Reference

[69]

Hugging Face, EPFL (2025) FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training Data Processing to Every Language, COLM2025

[70]

The Big LLM Architecture Comparison https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison

アクセス日: 2025/10/1

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0
