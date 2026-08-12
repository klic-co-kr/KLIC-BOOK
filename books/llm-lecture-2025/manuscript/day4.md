# Day 4

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

## スケール則

## 座学：小島武

## 演習：余振軒

許諾なく撮影や第三者

への開示を禁止します

## 大規模言語モデル講座2025

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

3

## 小島武（こじまたけし）

3

## ❏略歴

## ❏2023.3 東京大学大学院工学系研究科TMI 博士課程修了

## ❏2023.4～同研究科特任研究員

## ❏2025.1～同研究科特任助教

## ＊以前はITエンジニアをしてました.

## ❏活動

## Weblab-10Bの開発，岸田総理・石破総理のLLM特別講座で講師担当，LLM開発コンペ

## 2024・2025運営側のコンテンツリーダー，AI白書2025でSafetyの章を執筆

## ❏研究

## LLMの動作原理の理解と制御（Reasoning Model, 多言語等），Safety (Unlear

## ning, 指示追従能力），Transformerモデル構造の改善，などなど+ ロボット

https://github.com/kojima-

takeshi188/zero_shot_cot

https://arxiv.org/abs/2505.12583

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Day4）

## 4

## ●目的：

## ○言語モデルをスケール（＝大規模化）する意義について学ぶ.

## ●目標：

## ○スケール則とはなにかおよびその重要性を説明できる．

## ○スケール則の具体的な求め方を説明、実装できる．

## ○推論時のスケーリングとはなにかについて説明できる．

## ●演習：

## ○PyTorchでスケール則を実際に求めるコードを実装する

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

5

## 目次

5

## ○スケール則とはなにか

## ○スケール則の使い方

## ○スケール則の具体的な求め方

## ○新たなトレンド：推論時のスケーリング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

6

## スケール＝大規模化

6

## 大規模言語モデル

## Day3で説明しました.

## ＊近年のLLMで使われている

## Transformerモデルは,

## ニューラル言語モデルの一種.

## Day4で(今から)説明します.

## ＊どうスケールさせるのか？

## なぜスケールさせるのか？

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■LLM学習フローの中での位置づけ

## 事前学習

## 大規模コーパスによる自己教師あり学習を通し、大規模言語モデルに

## 語彙・文法・基本知識といった基礎的な言語理解を獲得させる段階

## ファインチューニング

## ラベル付きデータによる教師あり学習を通し、事前学習済みモデルの

## 性能を改善したり、特定のタスクやドメインへの適応を実現する段階

## RLHF

## 人間からのフィードバックを用いた強化学習を通し、大規模言語モデルの

## 出力がより人間の価値観に沿ったものとなるよう調整する段階

## Step 1

## Step 2

## Step 3

## Day3（前回）& Day4（本日）& Day5（次回）

## Day6

## Day7

## 7

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 大規模言語モデルの進展

8

## • 2025年以降も、GPT-5、Gemini2.5、GPT-OSS、DeepSeek-R1、Qwen3など多くのLLM

## が公開されている（継続中）．

## “A Survey of Large Language Models”, 2023 (version 16)

[[48] Zhao+. A Survey of Large Language Models. 2023 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Transformerを使った言語モデルのスケール化[1]

9

## 2019年

## 2020年

## 2018年

## 2023年

## 基本的にはいずれも2017年に発明されたTransformerと呼ばれる構造を利用．

## GPT-3登場以降，米国企業を中心に複数の研究機関が独自の大規模言語モデルを開発．

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## What is Scaling? Why Scaling?

10

## 背景にあるのがスケール則と呼ばれる経験則．下記を中心に説明．

## 2020年1月by Open AI

## (GPT3は2020年6月）

## ■重要論文１

## ■重要論文2

## 2022年by DeepMind（当時）

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

11

## 事前学習は，Webから収集した大量の文章を使って，次の単語の予測をひたすら行う

## 事前学習の過程で，読み書きそろばんや世界中のあらゆる知識を学習する

## • GPTシリーズを代表とする現代のLLMは，この事前学習を必ず行う

## • 例えば以下の図のように，「春は桜が綺麗」というテキストの事前学習によって，「春」

## 「桜」「綺麗」という言葉の間に強い関係性があること（＝世界の知識）を学ぶ

## 春

## 春

## は

## 春

## は

## 桜

## 春

## は

## 桜

## が

## LLM

## LLM

## LLM

## LLM

## P(は|春）

## P(桜|春, は)

## P(が|…)

## 入力

## 予測

## は

## 桜

## が

## 綺麗

## 正解

## 予測と正解との誤差

## （＝交差エントロピー）

## が小さくなるように

## モデルを学習する

## 入力した単語の

## 次に来る単語は？

## 比較

## P(綺麗|…)

## 事前学習（復習）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 12

## 計算資源（C）、データセットサイズ（D）、パラメータ数（N）

## と誤差（L）の間に成立する経験則

## • 各図のデータ点は実測値．ただし他の2変数は十分大きいと仮定．

## • いずれの変数もTest Lossとの間に両対数グラフで線形の関係が見られる

## スケール則（Scaling Law) *Power-Law (べき乗則)とも呼ばれる

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 13

## ①パラメータ数（N）と誤差（L）の間に成立する関係性.

## Loss

## =交差エントロピー

## スケール則（Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 14

## ②データセットサイズ（D）と誤差（L）の間に成立する関係性.

## Loss

## =交差エントロピー

## スケール則（Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 15

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## PF-days：

## Peta FLOPs days（1 Peta FLOPS

## の処理速度を持つサーバを何

## 日分学習に使ったか）

## ＊FLOPs：次ページ

## スケール則（Scaling Law)

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| 計算量の単位FLOPs

## 16

## ・計算量は、合計で何回の浮動小数点演算をおこなうかで表現される

## ・浮動小数点演算の例：パラメータの足し算，掛け算

## ・必要な合計計算量を表す単位として紛らわしいがFLOPsが使われる

## ・FLoating Points OPerations

## ・スケール則の横軸はこちら

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| FLOPsとFLOPS

## 17

## •

## これはFLOPS:

## •

## Floating Points

## Operation Per

## Second

## •

## 単位時間あたりに

## どれくらい処理

## できるかのHWの性能

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 18

## ⚫Mega（M）：10^6

## ⚫Giga（G）：10^9

## ⚫Tera（T）：10^12

## ⚫Peta（P）：10^15

## ⚫Exa（E）：10^18

## ・・・・

## ちなみに、

## ⚫GPT-3の総計算量は、3.14 * 10^23 FLOPs.

## （最近のモデルのFLOPsは詳細が非公開なので不明）

## ■補足| 大きな数字の表現

## [9] Brown+. Language Models are Few-Shot Learners.

## 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 19

## 各青線が、異なるモデルサイズ（パラメータ）

## で学習した時の学習曲線を表している.

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 20

## パラメータ数Nで学習したときの学習曲線

## パラメータ数N’’ で学習したときの学習曲線

## パラメータ数N’ で学習したときの学習曲線

## *パラメータ数N <N’ < N’’

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 21

## *パラメータ数N <N’ < N’’

## N

## N’

## N’’

## モデルサイズが小さい

## と, 少ない計算資源で

## も速いスピードでLoss

## が下がるが, その後

## 学習を続けてもLossが

## 下がりづらくなる

## （サチる）

## モデルサイズが大きいと,

## 少ない計算資源ではLossが

## なかなか下がらないが,

## 学習を続けるとLossが

## 下がり続けて最終的に

## よいパフォーマンスとなる

## （サチらない）

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 22

## *パラメータ数N <N’ < N’’

## このレベル（横の点線）のLoss

## （パフォーマンス）を達成する

## のに最適なモデルサイズは

## 「N’」. NでもN’’でもない.

## N

## N’

## N’’

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 23

## *パラメータ数N <N’ < N’’

## 限られた計算資源（縦の点線）で最良のパ

## フォーマンス（Loss）を発揮するモデルサ

## イズは「N’」. NでもN’’でもない.

## N

## N’

## N’’

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則（Scaling Law)

## 24

## *パラメータ数N <N’ < N’’

## N

## N’

## N’’

## つまり, この直線は「任意の

## 計算資源量が与えられた時

## に, その計算資源内で最良の

## パフォーマンスを発揮する

## パラメータサイズのモデル

## で到達可能なLoss値(最適点)

## の集合」を意味する.

## ③計算資源（C）と誤差（L）の間に成立する関係性.

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| スケール則（Scaling Law) という名前の由来

## 25

## α: 両対数グラフ上での傾き

## Xc : 切片（のようなもの）

## X : スケール則の変数(C or D or N)

## 両対数上での傾き

## べき乗で表現できる

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-3でのスケール則(OpenAI, 2020）

## 26

## •

## GPT3でもスケール則

## が利用されている

## •

## 先行研究(*)よりも

## ２桁オーダー大きい

## 計算量のスケール則

## を確認した.

## (*) “Scaling Laws for Neural Language Models”, 2020

## [9] Brown+. Language Models are Few-Shot Learners. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| スケーリングは新しい現象？

## 27

## •

## 少なくとも2017年by Baidu Researchでは検証されている

## •

## この研究ではスケール則の発生を多数のドメイン（機械翻訳、言語モデリング、画像

## 分類、音声認識など）で検証している。

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■初期のスケール則(Baidu, 2017）

## 28

## 同じ点

## データに関するスケール則

## を検証（モデルも少し）

## 左はMTの例．

## 相違点

## 1. 対象モデルが異なる

## （Transformer以前）

## 2. 規模が異なる

## （特にモデル）

## LSTM: RNN型言語モデルの一種

## [8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 異なるモデル構造での検証

## 29

## モデル構造の探索

## 深さ

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Mixture of Expert Modelのスケール則

## 30

## 図の点線が普通のTransformer，実践が

## Mixture of Expert (MoE)

## Q. MoEとは？A. Day 5でやります．

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022より引用

## [64] Ludziejewski+. Scaling Laws for Fine-Grained Mixture

## of Experts. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 様々なドメインでのスケール則（計算量とLoss）

## 31

## 画像生成，マルチモーダル，動画，数理等でも計算量に関するスケール則が成立

## [11] Henighan+. Scaling Laws for Autoregressive Generative Modeling.

## 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMの学習に必要な計算量とパラメータ数，トークン数の関係

## 32

## ・よく使われる近似式：6 × N（パラメータ数）× D（トークン数）

## （例）GPT3の場合

## 175B × 0.3T × 6 ≒ 3.14 * E+23 FLOPs

## ・なぜ６？A. １パラメータあたりのMLP層における行列演算数が６回だから.

## Forward

## Backward

## [47] Bahdanau. The FLOPs Calculus of Language Model Training.

## Medium. 2022より引用

## h(i)とwをかける

## a(j)に足す

## a(j)からの勾配をh(i)に伝える

## その勾配を集約する

## wに対する勾配を計算する

## その勾配を集計する

## [9] Brown+. Language Models are Few-Shot Learners. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足|Attentionは無視してよいのか？

## 33

## ・系列長が短い場合,

## MLPの計算量>> Attention機構の計算量（詳細は上記URLを参照）

## ・最近は系列長が長くなる傾向にあるので, 無視できなくなってきている可能性が高い.

## ・GPT-3：2,049トークン(*)

## ・ChatGPT：16,385トークン(*)

## ・GPT-4：32,768トークン(*)

## ・もっと正確な計算式の例：https://github.com/karpathy/nanoGPT/blob/master/scaling_laws.ipynb

## [47] Bahdanau. The FLOPs Calculus of Language Model Training. Medium. 2022より引用

## (*) [63] OpenAI. Models overview - OpenAI API Documentation. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ミニクイズ

## 34

## ・前提｜計算環境の計算能力を下記と仮定する

## GPU A100 ×1基：O(E+14 FLOPS)

## ※ こちらは単位時間あたりの計算量なので大文字

## ・クイズ｜A100を1000基使うとして，GPT-3の学習にはどれくらいの学習時間が必要か？

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■ここまでのまとめ| スケール則とはなにか

## 35

## •

## スケール則とは計算資源（C）、データセットサイズ（D)、

## パラメータ数（N）と誤差（L）の間に成立する以下のような経験則

## •

## 𝐿𝑋=

## ൗ

## 𝑿𝒄𝑋

## 𝜶

## •

## 冪乗の形をしている

## •

## Transformer以外のモデル，言語以外のタスクでもスケール則は確認さ

## れている

## •

## 計算量: FLOPs

## •

## C（計算量）= 6 × N（パラメータ数）× D（トークン数）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

36

## 目次

36

## ○スケール則とはなにか

## ○スケール則の使い方

## ○スケール則の具体的な求め方

## ○新たなトレンド：推論時のスケーリング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## (再掲)スケール則（Scale Law)

## 37

## DLにおけるスケール則とは？

## 1. 計算資源（C）

## 2. データセットサイズ（D）

## 3. パラメータ数（N）

## と誤差（L）の間に成立する次の経験則．

## ※ 他2つの変数が十分大きい場合．

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 38

## “GPT-4 Technical Report” [13] より抜粋

## X軸：GPT4を1.0とした計算量

## Y軸：性能

## ⇒1/1000程度のモデルまでで

## 性能を正確に予測できる．

## ※ GPT-4のパラメタ数は公開されていないがど

## んなに小さくても1010 (10B）より大．

## 左の図の最小が103だとしたら1013 (1T)

## “Scaling laws de-risk investments in large models”

## Q. あるモデルを1Tまでスケールするべきか？

## [13] OpenAI. GPT-4 Technical Report. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## より精緻なモデル選択

## 39

## モデル構造の探索

## ハイパラ探索

## スケールしてもおそらく

## Transformer > LSTM

## パラメータ小=> 層が少ないほうが良い

## パラメータ大=> 層が多いほうが良い

## Q. モデルAとモデルBはどちらが性能がよい？

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020

より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケーリングによって享受できるメリット|効率性

## 40

## パラメータ数が多いほど

## サンプル効率は良い

## 小さなモデルだと学習途中からロスが下がりづらくなる-> ある

## ロスを達成するのに小さなモデルで計算を継続するのは非効率

[3] Kaplan+. Scaling Laws for Neural

Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 与えられた計算量の下で最適なパラメータ数とトークン数を探す

## 41

## •

## 計算量を固定したときに，パラメータ数とトークン数を変動させた場合のプロット

## •

## 左：Chinchilla，右：PaLM2

## •

## どの計算量でもUカーブになっており．最適な値がありそうなことがわかる

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

## 42

## 与えられた計算量（この曲線の場合は

## 1e19 FLOPs）のもとで、異なるパラメ

## ータのモデル（50M, 100M, 300M,

## 1B・・・）をそれぞれ学習し、各モデ

## ルの最終的なTraining Lossをプロット

## すると、Uカーブができる。

## Q：なぜ下にUカーブになるのか？≒な

## ぜ右肩下がりの線にならないのか？

## A：大きなパラメータサイズのモデル

## になるほど、学習初期のLossが下がり

## づらいから（前頁の右図を参照）。

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

## 43

## 各曲線ごとにTraining Lossが最小と

## なるポイントが存在する（図の

## ☆）。これらが、各計算量（各

## FLOPs）における最適なパラメー

## タサイズ。

## 計算量を変えて、同じように曲線を

## 描いて最適なパラメータサイズを出

## していくと、FLOPsとParameterの

## 間の最適な関係を導出することがで

## きる。ほぼ直線の関係であることが

## わかる。

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

## 44

## • 計算量固定でトークン数とパラメータ数を変動させた結果（左）

## 参考）FLOPs = 6 × N（パラメータ数）× D（トークン数）

## • この結果を，各FLOPsでの最適なパラメータに直したもの（中央）

## • 同様にトークン数について最適な値をもとめたもの（右）

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

## 45

## データサイズD

## トークンを1.4Tまで増加

## （同じデータの別サブセット）

## ※ Gopherの約4.6倍

## モデルサイズN

## 70Bに設定

## ※ Gopherの約1/4倍

## 結果

## 多くのケースでより巨大なモデルに勝利

## （発見した関係式の妥当性を示唆）

## 最適トークン数= 20 * パラメータ数

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## PaLM2でのスケール則（Google, 2023）

## 46

## PaLM2でも同様の実験が行われており，Chinchilla同様のスケール則が確認．

## [10] Anil+. PaLM 2 Technical Report. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla則を超えた量の学習

## 47

## “Go smol or go home, Why we should train smaller LLMs on more tokens”より抜粋

## • Chinchilla Trap:

## Chinchillaのモデルサイズ(70B)は

## 大きいため, 推論コストが高い*.

## 推論コストも考慮してより

## 小さなモデルを長時間

## 訓練するべきではという意見

## • 最適モデルサイズの40-60%以内の

## モデルサイズを選択して，

## 10-42%の計算量の追加で同性能の

## モデルを学習できるという指摘

## 同じパフォーマンスを達成するため

## に必要なパラメータサイズ（横軸）

## と計算量（縦軸）の関係

[43] de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens.

Harm de Vries Blog. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q. Chinchilla則は本当に*最適*なのか？

## 48

## 学習だけを見ると、大きいモデル

## のほうが小さいモデルよりも同じ

## FLOPsで高い性能を発揮する

## 一方で、推論時は、大きいモデル

## のほうが小さいモデルよりも同じ

## 多くのFLOPsを必要とする

## 学習と推論のトレードオフが発生

## 学習と推論の両方のFLOPsを考慮

## した最適解（トークン数，パラメ

## ータ数）を出したほうがいいので

## は？

## [50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 推論時のコストを考慮した最適なトークン数

## 49

## • 横軸：推論時のトークン数の仮定

## • 色：学習時のトークン数をChinchilla

## に対して何倍にするか（1.01 ~ 40）

## • 推論回数が多くなるほどライフタイム

## 全体では学習トークン数を増やすほう

## が有利

## 推論時のトークン数と達成したい学習Lossを仮定したときの、ライフ

## タイム全体の総FLOPsを最小にするような最適なパラメータ数および

## 学習時のトークン数

## [50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■参考| 様々なモデルのToken to Parameter Ratio (D/N)

## 50

## Params (N)

## Token (D)

## D/N

## Gopher

## 280B

## 0.3T

## 1.07

## Chinchilla

## 70B

## 1.4T

## 20.0

## Llama 2

## 7B

## 1.8T

## 285

## 70B

## 1.8T

## 28.5

## Llama 3

## 70B

## 15T

## 214.2

## 405B

## 15T

## 37.7

## Qwen 3

## 32B

## 36T

## 1125

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| 予測可能な改善と予測不可能な改善

## 51

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023より引用

## 予測可能な例

## ・スケール則に従った性能の概算

## ・一般的な文章の次単語予測精度

## ・翻訳タスクやQAタスクでの平均的なスコア改善

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 予測不可能な性質の例| Emergent Ability

## 52

## モデルサイズを巨大にすると性能が”突如”大幅に上がるタスクがある

## [4] Wei+. Emergent Abilities of Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| 本当に創発能力なのか?

## 53

## • 本当に「創発」「相転移」して

## いるのかには反論もある

## – 性能の測り方による（左図）

## ※ これは本論文でも言われている

## – 横軸が対数なのは変では

## – そもそも何を持って創発？

## • 巨大モデル|巨大計算で思った

## よりできるようになるのは事実

## [5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 予測不可能な性質の例| Grokking

## 54

## “Progress measures for grokking via

## mechanistic interpretability”, ICLR2023

## “Grokking: Generalization Beyond Overfitting on

## Small Algorithmic Datasets”, 2022

## 学習を継続すると突然検証データでの正解率が高まる現象

## (学習データでの正解率はそれ以前にすでに高い. つまりOverfit後も学習を継続させると発生する現象)

## （下記はa○b = c（例：x+y=?）というタスクにおける性能調査）

## [6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| Grokking中にはモデル内部で何がおこっているのか？

## 55

## 類似研究：”Progress measures for grokking via mechanistic interpretability”, ICLR2023

## A. 記憶を汎化させている（上は学習過程の可視化）．

## 過学習中（中央）は覚えているだけだが，汎化後（右）には数字が綺麗に整列．

## [7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 様々なドメインでのスケール則（計算量とLoss）

## 56

## ある計算量が与えられたときの最適なモデルサイズのドメイン間での比較

## どのドメインも概ね同じような傾向にある

## [11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 下流タスクの性能とスケール則

## 57

## •

## WebText2：通常のテストデータ，それ以外：学習外の(分布外の)データ

## •

## WebText2以外で性能の劣化は見られるもの，オフセットの違い程度で

## 傾向は同じ（傾きもほぼ同じ）

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則がもたらすもの

## 58

## 下流タスクの性能との関係性

## Q. Loss(事前学習の交差エントロピー)が低い＝下流タスクの性能が高い？

## ①綺麗に上がる

## ②突然上がる

## (Emergent Ability)

## ③上がらない

## ④下がって上がる

## (Inverse scaling prize)

## ・基本的にはYES.

## ・例外もままある(例：下図②～③)

## ・タスクの種類や難易度による

“GPT-4 Technical Report”, 2023

“Language Models are Few-Shot Learners”, 2020

①～③：[9] Brown+. Language Models are Few-Shot Learners. 2020より引用, ④：[13] OpenAI. GPT-4 Technical Report. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケール則がもたらすもの

## 59

## 下流タスクの性能との関係性

## [69] Isik+. Scaling Laws for Downstream Task Performance in Machine Translation. 2024より引用

## 機械翻訳タスクによる検証結果：事前学習データ(*1)と下流タスクデータ(*2)

## の分布間の距離(*3)がアラインしている場合は、事前学習データ量と下流タス

## クの評価値の間にスケール則が成立する。

## (*1) MC4 (Multilingual C4) （*2）機械翻訳タスク(*3) Embedding 空間での分布距離を計測

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ここまでのまとめ｜スケール則の活用方法の大別

## 60

## 予測可能な性能改善により，次のような問いに答えられる．

## •

## 投資の判断｜より計算機に投資するか？

## •

## 効率的なモデル選択｜パラメータを増やしたときにどちらが良いモデル？

## •

## 効率的な計算資源の利用｜トークンとパラメータのどちらを増やすべき？

## •

## Chinchilla Optimal: 最適トークン数= 20 * パラメータ数

## •

## 推論コストを考えると最適トークン数の係数は変化する

## •

## 下流タスクにスケール則が必ず成立するとは限らない（線形になるとは限らな

## い）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

61

## 目次

61

## ○スケール則とはなにか

## ○スケール則の使い方

## ○スケール則の具体的な求め方

## ○新たなトレンド：推論時のスケーリング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

62

## スケール則の測り方

62

## 基本的には（比較的）小さないくつかの条件で実験してFittingする

## Q. モデルサイズはどう変える？

## Q. 学習率などのハイパーパラメータはどう設定する？

“GPT-4 Technical Report” [13]

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

63

## Q1. モデルサイズはどう変化させるのか？

63

## •

## 層数を増やす

## •

## 埋め込み次元を上げる

## •

## FFNの中間層の次元を大きくする

## •

## ヘッド数を増やす

## •

## Etc…

## •

## どれをどのくらいやる？

[65] Vaswani+. Attention Is All You Need. 2017より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルサイズはどう変化させるのか？

## 64

## 元の論文ではパラメータ数を固定したときにネットワークのいくつかの要素

## をいじって検討している=> 結果あんまり大きくは影響ないとの結論

## 例：アスペクト比：埋め込みサイズ/ 層数

## ＊横と縦の比率というイメージ

## [3] Kaplan+. Scaling Laws for Neural Language Models. 2020より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 実例１｜Llama 3

## 65

## アスペクト比はそれぞれ128, 102.4 130

## Model vs. FFN Dimensionはすべて3.5

## ヘッド数もModel Dimensionに対して同様にスケール

[66] AI@Meta+. The Llama 3 Herd of Models. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 実例2 | Cerebras GPT

## 66

## アスペクト比はそれぞれ76.8, 77.7, 85.3, 85.3 …

## Model vs. FFN Dimensionはすべて4.0

## ヘッド数はやや不規則に変化

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q2. ハイパーパラメータをどう変化させるか？

## 67

## 学習率やスケジューリングがバラバラ

## モデルパラメータサイズが大きいほど、学習率は徐々に小さく，バッチ

## サイズは大きくする傾向がある。

## !!!!?

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 通常の初期化の場合，最適なハイパラは変動する

## 68

## •

## 幅を変化させたときの最適な

## 学習率のプロット

## •

## 幅によって最適なハイパラは変

## 動する（とは言えある程度傾向

## はある）

## 経験則として，モデルサイズを大

## キックした時に学習率は小さく，

## バッチサイズは大きくすると良い

## 傾向

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## μTransfer：最適なハイパラの転移可能な方法

## 69

## μTransferを使えば、モデルサイズが異なっても、ほぼ同

## じくらいlearning rateの値で最適なLossを達成できる

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 70

## μTransfer：最適なハイパラの転移可能な方法

## ウェイトの初期化方法と、weightごとのLearning rateの設定方法を以下のように変更する（赤文字）

## [52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 事例｜Cerebras GPT + μTransfer

## 71

## μTransferを使う場合

## 普通のパラメタ設定

## つまり、小さいモデルで最適なLearning Rateを見つけ、その値

## を大きいモデルにゼロショットで転移することができる。

## [51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models

## Trained on the Cerebras Wafer-Scale Cluster. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ここまでのまとめ｜スケール則の求め方

## 72

## •

## スケール則を求めるためには基本的にはいくつかの設定で実験を行い

## フィッティングすればよい．

## •

## しかし，スケールさせるときにはいくつか問題が発生しうる

## •

## 問題１. モデルサイズをどうスケールさせる？

## • A. だいたい固定の係数を維持しながらスケールする

## •

## 問題２. モデルサイズをスケールさせるときにハイパラはどう変える？

## • A. 論文によるが，大体学習率は徐々に小さく，バッチサイズは大きく

## する．μTransferという方法もある．

## •

## スケール則の詳細に更に興味ある方は下記を参照

## •

## [62] Tatsunori Hashimoto, Percy Liang. CS336: Language Modeling from Scratch.

## Stanford University. 2024

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

73

## 目次

73

## ○スケール則とはなにか

## ○スケール則の使い方

## ○スケール則の具体的な求め方

## ○新たなトレンド：推論時のスケーリング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

74

## Motivation

74

## 問１：「バナナの色は何色ですか？」

## 問２：「スケール則の問題は何だと思いますか？」

## ２つの問いは，必要な思考のプロセスは明らかに異なると思える．

## 後者は推論時により負荷がかかる．

## Q. このような仕組みをLLMでどう実現できるか？

## Q. このような仕組みはLLMで効果的か？

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q. このような仕組みはLLMで効果的か？A. Yes

75

## •

## OpenAIが発表したo1もテスト時の推論をスケーリングさせることで性能向上を報告

## [53] OpenAI. Learning to reason with LLMs. OpenAI Blog. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## （Day 2振り返り）推論時に計算量をスケールさせる方法の例

76

## Chain-of-Thought Prompting

## Many-Shot ICL

## Promptingにより推論時のトークン数を増やすことで推論時の計算量を

## スケールさせる試み

[67] Wei+. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022より引用

[68] Agarwal+. Many-Shot In-Context Learning. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ・Decodingを複雑にする

## ・事前学習済みLLMを使って, テキストを出力（デコード）する.

## ・デコードには様々な方式が存在する.

## ・Greedy Decoding

## ・Beam Search

## ・Random Sampling

## ・Top K / Top P Sampling

77

## （Day 2,3 振り返り）推論時に計算量をスケールさせる方法の例

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 様々なデコーディング方法

78

## •

## デコード方式の一覧

## •

## 様々な方式が提案されている

[54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なデコーディング方法の例｜Contrastive Decoding

79

## Contrastive Decoding

## •

## 外部のモデルを使う方法の例

## •

## エキスパートモデルとアマチュア

## モデルを用いて確率密度比を取っ

## てそこからサンプリングを行う

## •

## アマチュアモデルには通常エキスと

## パートモデルよりも少ないパラメー

## タ数のモデルを用いる

## •

## エキスパートモデルの出力をより

## 強調し，アマチュアモデルの出力

## を減少させるように生成を行う

## [55] Li+. Contrastive Decoding: Open-ended Text Generation as Optimization. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

80

## Meta Generationとは？Token LevelのDecodingだけでなく，文章や段落ご

## とで生成過程を評価し，生成プロセス全体を最適化する概念

## From Decoding to Meta-Generation

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

81

## ①Parallel search

## 例：Best-of-N, Self-Consistency

## •

## 並列に複数の候補を生成してスコアリングや多数決などにより生成物を選ぶ

## ②Step level search

## 例：Process Reward Model (PRM)

## •

## Stepレベルに評価を行なって生成物を選ぶ

## ③Refinement

## 例：Self-Refine

## •

## 外部/内部のフィードバック結果を用いて，反復的に生成結果を更新する

## Meta-Generationの種類（いずれも推論時に計算量が大きくスケール）

[54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

82

## Best-of-N

## •

## N個の回答を出してスコアが一番高いものを

## 選択する

## •

## スコア関数は任意(タスクによって使い分け)

## •

## 例：LLMのスコアを使う

## •

## 例：学習した評価器を使う

## •

## 例：BLUEなど特定の指標を使う

## ①Parallel Searchの方法の例｜Best-of-N

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

83

## Self-Consistency（Day 2のおさらい）

## •

## LMに複数の推論を行わせて（下は3つの例），Majority Voting（多数決）

## ①Parallel Searchの方法の例｜Self-Consistency

## [58] Wang+. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ①Parallel Searchの方法の例｜MBR Decoding

84

## MBR Decoding(Minimum Bayes-Risk Decoding)

## •

## 機械翻訳の際に使用されるデコーディング方法

## •

## 効用関数を用いて出力のクオリティを最大化するようにデコーディング

## •

## 機械翻訳における効用関数: BLUE, METEOR, BLEURT, COMET

## •

## 詳細が知りたい人はURL

## [57] Eikema+. On the True Distribution Approximation of Minimum Bayes-Risk Decoding. 2020より引用

## ・y : モデルの出力文

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ①Parallel Searchの他の方法

85

## Aggregation typeやScoringの手法によって様々なアルゴリズムが存在

## [56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model

## Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ②Step Level Searchの方法の例｜Beam-Search (Step Level)

86

## Beam-Search(Step Level)

## •

## Token LevelのBeam Searchとは異なり，

## 文章や段落単位でサンプリングと評価を行

## う

## •

## 評価にはPRM(Process Reward Model)を

## 用いて途中結果の評価と選択を行う

## •

## Top-N Samplingによって途中結果を選択

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than

Scaling Model Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ②Step Level Searchの方法の例｜Tree-of-Thought

87

## Tree-of-Thought

## •

## 複数の思考列を一気通貫で出力して評価するSCとは違い，ToTは途中で分岐さ

## せる（木探索する）

## • ノードの評価もLMで行う

## •

## Game of 24での例と結果

## • タスク：与えられた4つの数字を四則演算して24を作る

## •

## 戦略的思考が必要なタスクで性能が大幅改善

[60] Yao+. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. 2023より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ②Step Level Searchの他の方法

88

## 探索方法や検証するステップの違いなどにより様々なアルゴリズムが存在

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

89

## •

## 一度生成した結果や，その結果に対するフィードバックをもとに再度生成

[59] Lightman+. Let‘s Verify Step by Step. 2023より引用

## ③Refinement

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

90

## 自分自身を使ってフィードバックを生成して出力を改善

## [61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023より引用

## ③Refinementの方法の例| Self-Refine（Day 2のおさらい）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

91

## •

## 7つのタスクで最大50%近くの精度向上

## [61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023より引用

## ③Refinementの方法の例| Self-Refine （Day 2のおさらい）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Majority Voting vs. Best-of-N (ORM)

92

## [59] Lightman+. Let‘s Verify Step by Step. 2023より引用

## Best-of-N (ORM)

## •

## Outcome-supervised Reward Model

## を使って出力全体を評価

## Majority Voting

## •

## 多数決して選択

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Majority Voting vs. Best-of-N (ORM) vs. Best-of-N (PRM)

93

## [59] Lightman+. Let‘s Verify Step by Step. 2023より引用

## Best-of-N (PRM)

## •

## Process-supervised Reward Model

## を利用して途中の仮定を評価

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q. 同じ計算資源のとき，パラメータを増やすより有効？

94

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q. 同じ計算資源のとき，パラメータを増やすより有効？

95

## •

## ランダムサンプリングによる推論回数を増やして、プロセスレベルの報酬モデ

## ル(PRM) を用いた推論パス/最終回答の適切な選択をする事で性能が向上.

## Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters より

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Q. 同じ計算資源のとき，パラメータを増やすより有効？

96

## •

## ランダムサンプリングによる推論回数を増やして、プロセスレベルの報酬モデ

## ル(PRM) を用いた推論パス/最終回答の適切な選択をする事で性能が向上.

## Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters より

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

97

## 本日のまとめ

97

## 言語モデルのスケール則について紹介しました．

## 1.スケール則とは何かについて説明しました。

## スケール則とは計算資源（C）、データセットサイズ（D)、パラメータ数（N）と誤

## 差（L）の間に成立する経験則；対数グラフ上でほぼ直線の関係が成立する。

## 3.推論時のスケーリングとはなにかについて説明しました。

## 訓練時だけでなく，推論時にも計算量をスケールさせることで性能を

## 改善することができる。推論時の工夫：Prompting，Decoding，Meta-Generation

## 2.スケール則の具体的な求め方について説明しました。

## スケール則を求めるためには基本的にはいくつかの異なる設定で実験を行い

## フィッティングする。ハイパラの設定（例：アスペクト比，学習率，バッチサイ

## ズ）については様々な知見が論文で発表されている。

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 98

[1] Bao Hua Choo. The emergence of Large Language Models (LLMs), The low down. 2023. https://thelowdown.momentum.asia/the-emergence-of-large-

language-models-llms/, アクセス日: 2023/11/16

[2] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223v12

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020. In arXiv:2001.08361

[4] Wei+. Emergent Abilities of Large Language Models. 2022. In arXiv:2206.07682v2

[5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023. In arXiv:2304.15004v2

[6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022. In arXiv:2201.02177v1

[7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022. In NeurIPS2022

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017. In arXiv:1712.00409v1

[9] Brown+. Language Models are Few-Shot Learners. 2020. In NeurIPS2020

[10] Anil+. PaLM 2 Technical Report. 2023. In arXiv:2305.10403v3

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 99

[11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023. In arXiv:2202.07785v2

[13] OpenAI. GPT-4 Technical Report. 2023. In arXiv:2303.08774v3

[14] Abhinav Venigalla, Linden Li. Billion-Parameter GPT Training Made Easy. MosaicML. 2022. https://www.mosaicml.com/blog/billion-parameter-gpt-

training-made-easy, アクセス日: 2023/11/16

[15] Vaswani+. Attention Is All You Need. 2017. In NeurIPS2017

[16] Jaiyam Sharma. Understanding Attention Mechanism in Transformer Neural Networks. LearnOpenCV. 2022. https://learnopencv.com/attention-

mechanism-in-transformer-neural-networks/, アクセス日: 2023/11/16

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022. In arXiv:2211.04325v1

[18] Tay+. Efficient Transformers: A Survey. 2020. In arXiv:2009.06732v3

[19] Child+. Generating Long Sequences with Sparse Transformers. 2019. In arXiv:1904.10509v1

[20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020. In NeurIPS2020

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 100

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022. In NeurIPS2022

[22] Tri Dao. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. 2023. In arXiv:2307.08691v1

[23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022. In NeurIPS2022

[24] Shazeer+. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. 2017. In ICLR

[25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity. 2021. In arXiv:2101.03961v3

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022. In ICML2022

Proceedings of the 39th

International Conference on Machine Learning, PMLR 162:18332-18346

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022. In arXiv:2202.01169v2

[28] Zhai+. An Attention Free Transformer. 2021. In arXiv:2105.14103v2

[29] Peng+. RWKV: Reinventing RNNs for the Transform. 2023. In arXiv:2305.13048v1

[30] Sun+. Retentive Network: A Successor to Transformer for Large Language Models. 2023. In arXiv:2307.08621v4

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 101

[31] Gu+. Efficiently Modeling Long Sequences with Structured State Spaces. 2022. In ICLR2022

[32] Microsoft. DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレームワーク.

https://www.deepspeed.ai/assets/files/DeepSpeed_Overview_Japanese_2023Jun7th.pdf. アクセス日: 2023/11/16

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019. In arXiv:1910.02054

[34] Microsoft. DeepSpeed. https://github.com/microsoft/DeepSpeed. アクセス日: 2023/11/16

[35] DeepSpeed Team. Configuration JSON. https://www.deepspeed.ai/docs/config-json/. アクセス日: 2023/11/16

[36] Belkada+. A Gentle Introduction to 8-bit Matrix Multiplication for Transformers at Scale using Hugging Face Transformers, Accelerate

and bitsandbytes. Hugging Face Blog. 2022. https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-introduction-to-8-bit-

matrix-multiplication-for-transformers-at-scale-using-hugging-face-transformers-accelerate-and-bitsandbytes. アクセス日: 2023/11/16

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022. In NeurIPS2022

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023. In arXiv:2307.08072

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023. In

arXiv:2306.01116

[40] Okanohara. MinHashによる高速な類似検索. Preferred Networks Research&Development. 2011.

https://tech.preferred.jp/ja/blog/minhash/. アクセス日: 2023/11/16

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 102

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022. In arXiv:2205.09357v1

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022. In NeurIPS2022

[43] de Vries. Go smol or go home, Why we should train smaller LLMs on more tokens. Harm de Vries Blog. 2023.

https://www.harmdevries.com/post/model-size-vs-compute-overhead/. アクセス日: 2023/11/16

[44] Sorscher+. Beyond neural scaling laws: beating power law scaling via data pruning. 2022. In NeurIPS2022

[45] Tirumala+. D4: Improving LLM Pretraining via Document De-Duplication and Diversification. 2023. In arXiv:2308.12284v1

[46] Zhou+. LIMA: Less Is More for Alignment. 2023. In arXiv:2305.11206v1

[47] Bahdanau. The FLOPs Calculus of Language Model Training. Medium. 2022. https://medium.com/@dzmitrybahdanau/the-flops-calculus-of-

language-model-training-3b19c1f025e4. アクセス日: 2023/11/16

[48] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223

[49] Gu+. Mamba: Linear-Time Sequence Modeling with Selective State Spaces. 2023. In arXiv:2312.00752

[50] Sardana+. Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. 2024. In ICML2024 (arXiv:2401.00448)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 103

[51] Dey+. Cerebras-GPT: Open Compute-Optimal Language Models Trained on the Cerebras Wafer-Scale Cluster. 2023. In arXiv:2304.03208

[52] Yang+. Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. 2022. In NeurIPS2022

[53] OpenAI. Learning to reason with LLMs. OpenAI Blog. 2024. https://openai.com/index/learning-to-reason-with-llms/ . アクセス日: 2026/05/25

[54] Madaan+. From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models. 2024. In arXiv:2406.16794

[55] Li+. Contrastive Decoding: Open-ended Text Generation as Optimization. 2023. In ACL2023

[56] Snell+. Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters. 2024. In arXiv:2408.03314

[57] Eikema+. On the True Distribution Approximation of Minimum Bayes-Risk Decoding. 2020. In EMNLP2020

[58] Wang+. Self-Consistency Improves Chain of Thought Reasoning in Language Models. 2023. In ICLR2023

[59] Lightman+. Let's Verify Step by Step. 2023. In ICLR2024 (arXiv:2305.20050)

[60] Yao+. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. 2023. In NeurIPS2023

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## 大規模言語モデルDay4

## 104

[61] Madaan+. Self-Refine: Iterative Refinement with Self-Feedback. 2023

[62] Tatsunori Hashimoto, Percy Liang. CS336: Language Modeling from Scratch. Stanford University. 2024. https://cs336.stanford.edu/

## [63] OpenAI. Models overview - OpenAI API Documentation. 2023. https://platform.openai.com/docs/models/overview. アクセス日: 2023/09/14

[64] Ludziejewski+. Scaling Laws for Fine-Grained Mixture of Experts. 2024 . アクセス日: 2026/05/25

[65] Vaswani+. Attention Is All You Need. 2017

[66] AI@Meta+. The Llama 3 Herd of Models. 2024

[67] Wei+. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. 2022

[68] Agarwal+. Many-Shot In-Context Learning. 2024

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0
