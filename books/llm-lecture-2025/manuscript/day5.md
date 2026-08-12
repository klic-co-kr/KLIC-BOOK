# Day 5

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

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

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 5. Advanced Pre-training

## 大規模言語モデル講座2025

## 2025/10/29

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 山田育矢（やまだいくや）

3

## Studio Ousia チーフサイエンティスト

## 名古屋大学数理・データ科学・人工知能教育研究センター客員教授

## 東北大学言語AI研究センター特任教授（客員）

## 博士（学術）

## 主な実績：

## •

## 様々な言語モデルの開発

## •

## 開発した早押しクイズAIが全米クイズ王チームに勝利（NIPS Competition 2017）

## •

## 複数の国際コンペティションで好成績を獲得

## NeurIPS EfficientQA 2020 (2位), ISWC Challenge 2020 (1位),

## NIPS HCQA 2017 (1位), WSDM Cup 2017 (2位),

## NAACL HCQA 2016 (1位), ACL W-NUT 2015 (1位), etc.

## 主な著書：

## •

## 大規模言語モデル入門・大規模言語モデル入門II

## •

## ディープラーニングによる自然言語処理

## https://ikuya.net

## ikuyamada

## ikuya@ikuya.net

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMの開発ステップ

4

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMの開発ステップ

5

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Pre-trainingの位置付け

6

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Pre-trainingの位置付け

7

## 第3回と今日のトピック

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 事前学習はどのくらい重要？

8

[66]  iwiwi, github,

https://gist.github.com/iwiwi/fc174b1f2341c2c0170be87c5b2e1d31,

## GPT-4の各開発タスクにおける人数が全体に占める割合≒

## OpenAIの考えるLLM開発における重要度の割合！？

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 重要な問い：事前学習を自前で実施する必要はあるか？(1)

9

[65] weights & biases, 「LLMをゼロからトレーニングするためのベストプラクティス」より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 重要な問い：事前学習を自前で実施する必要はあるか？(2)

10

[65] weights & biases, 「LLMをゼロからトレーニングするためのベストプラクティス」より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 重要な問い：事前学習を自前で実施する必要はあるか？(3)

11

[65] weights & biases, 「LLMをゼロからトレーニングするためのベストプラクティス」より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 復習– スケール則–

12

## スケール則：言語モデルをスケール(大規模化) させることで性能が向上する関係

## 以下の3つの要素と性能(L) の間で成り立つ経験則

## ■計算資源(C)

## ■データセットサイズ(D)

## ■パラメータ数(N)

## ●

## 様々なドメインで大規模なモデルを開発する利点が確認された．

## ●

## スケール則により，大規模なモデルへの投資リスクが軽減された．

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Advanced Pre-trainingの目的

13

## （*第3回の続き）

## 言語モデルをスケール（＝大規模化）して事前学習することの発展的な話題について学ぶ.

## Goal 1

## モデルをスケールして事前学習する上での(発展的な) 課題について説明できる.

## モデルをスケールして事前学習する(発展的な) 方法について説明できる.

## 事前学習の一連の流れをコードで実装できる(モデルをスケールするための技術も含む).

## Goal 2

## Goal 3

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 全体の流れ

14

## ●講義：

## ○それぞれの要素のスケールにおける問題点

## ○スケールするための技術

## ●演習：

## ○PyTorchでTransformerモデルを事前学習するための一連の流れを実装

## (データの準備, 前処理からモデルをスケールする技術を使った学習まで)

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

15

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

16

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケールさせる上での課題

17

## パラメータ, 計算量, データをスケールする事で,

## スケール則に従って性能が上がることはわかったが,

## スケールさせる上で様々な課題がある

## 計算量（C）

## 十分な計算量/

## メモリ量を確保して

## 効率よく訓練する必要

## パラメータ数（N）

## モデルがスケール

## するにつれて増加する

## コストを抑える必要

## データ（D）

## 性能を発揮させるため

## の学習用データを用意

## する必要

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## N, C：モデルサイズの増加につれて必要なコストが増加

18

## “Mosaic LLMs (Part 1): Billion-Parameter GPT Training Made Easy” [14] より抜粋

## →効率的に大規模なモデルを訓練できれば、コストを減らすことができる

[14] Abhinav Venigalla, Linden Li, Billion-Parameter GPT Training Made Easy, MosaicMLより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## N, C: Transformerは系列長に対し必要な計算量/メモリが増加

19

## Self-Attentionでは，系列長nの2乗の計算量とメモリが必要になる

## [15] Vaswani+. Attention Is All You Need. 2017より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■復習|なぜ系列長の2乗の計算量/メモリが必要なのか？

20

## “Understanding Attention Mechanism in Transformer Neural Networks” [16]より抜粋

## 各トークンが他のすべてのトークンとの関連性を計算するため，

## 全トークンの組み合わせに対して計算を行い，その値を記憶する必要がある．

[16] Jaiyam Sharma, Understanding Attention Mechanism in Transformer Neural Networks, LearnOpenCVより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## D：データの枯渇問題| データはどこまで増やせるのか？

21

## 過去のWebデータの増え方，学習データの増え方からの予測

## 良質な言語データは2024年頃に枯渇することが予測されている．

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

22

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

23

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## パラメータ(N)に関連する取り組みの全体像

24

## モデルがスケール

## するにつれて

## コストが増加する

## Self-Attentionそのものの

## 計算/メモリ効率を改善する

## 課題

## 方向性

## 解決策

## Efficient Attention

## 計算コストを肥大化させず

## モデルのパラメータを増やす

## 混合エキスパート

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## パラメータ(N)に関連する取り組みの全体像

25

## モデルがスケール

## するにつれて

## コストが増加する

## 課題

## 方向性

## 解決策

## Self-Attentionそのものの

## 計算/メモリ効率を改善する

## Efficient Attention

## 計算コストを肥大化させず

## モデルのパラメータを増やす

## 混合エキスパート

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Sparse Transformer：Sparse(疎)なAttentionの提案

26

## ・Attentionを計算する箇所を限定(計算しない箇所はマスク)することで計算量削減

## ・非常に長い系列長の入力（例: 画像や音声）に対しても効率的にTransformerの利用が可能に.

## [19] Child+. Generating Long Sequences with Sparse Transformers. 2019より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Sparse Transformer：Sparse(疎)なAttentionの提案

27

## 2回アテンション機構を

## 通せば全てのトークンに

## アテンションが当たる.

## [19] Child+. Generating Long Sequences with Sparse Transformers. 2019より引用

## [64] sunbluesome. Sparse Transformerを理解したいより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Big Bird：Sparse(疎)なAttentionの提案

28

## 方法

## 複数のSparseな

## Attentionを

## 組み合わせて，

## Attentionを近似し，

## 長い系列に対応する

## 結果

## 長い系列を扱う質問応

## 答や要約などのタスク

## で良い性能を獲得

## 類似アイデア：”Longformer: The Long-Document Transformer”, 2020

## [20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## FlashAttention：メモリアクセスを考慮し高速化を実現

29

## Attentionの計算は、計算ではなくメモリのI/Oにボトルネックがあることを指摘

## 入力行列をうまく分割して計算することで、系列長×系列長のAttention行列

## 全体のメモリの読み書きを回避。GPU SRAMで処理をなるべく完結させる

## （低速なGPU HBMメモリへのアクセス回数を削減）ようにし、大幅な高速化(e.g.GPT-2におい

## て最大7.6倍)に成功

## 実装の最適化

## （fused kernel）

## によって大幅な速

## 度の向上

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## FlashAttention2：FlashAttentionをさらに高速化

30

## “FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning” [22]

## 方法：実装上の3つの工夫を積み上げることによる高速化

## •

## アルゴリズムを工夫することで行列演算以外の演算をなるべく削減する

## （GPUは行列演算は専用の計算ユニットがあるため高速に処理できる）

## •

## バッチやAttentionのヘッドだけでなく系列方向にも並列演算を実施することでバッチや

## ヘッド数が少ない場合でも高速化できるようにする

## •

## ワープ（同時に走るスレッドのグループを指すGPUの用語）をクエリ行列で

## 分割することで、ワープ間の同期や通信を削減し、並列性を向上

## Flash-Attentionのおよそ２倍の高速化(PyTorchの標準Attentionの最大9倍高速)

[22] Tri Dao. FlashAttention-2: Faster Attention with Better

Parallelism and Work Partitioning. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## パラメータ(N)に関連する取り組み：混合エキスパート

31

## モデルがスケール

## するにつれて

## コストが増加する

## 課題

## 方向性

## 解決策

## Self-Attentionそのものの

## 計算/メモリ効率を改善する

## Efficient Attention

## 計算コストを肥大化させず

## モデルのパラメータを増やす

## 混合エキスパート

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 計算コストを肥大化させずモデルのパラメータを増やす？

32

## 用意する

## パラメータ数

## 必要な計算量

## 用意する

## パラメータ数

## 必要な計算量

## 用意する

## パラメータ数

## 必要な計算量

## 通常

## やりたい事

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 混合エキスパート(MoE)

33

## 複数個のエキスパート(ニューラルネットワーク)を用意しておき, 入力の値に

## 応じて, 一部のエキスパートだけにフォワードする. → すべてのパラメータを

## 使う事にはならないので, 計算量を抑えられる.

## エキスパートA

## （というネットワーク）

## エキスパートB

## （というネットワーク）

## エキスパートC

## （というネットワーク）

## 入力

## 出力

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 混合エキスパート(MoE)

34

## 複数個のエキスパート(ニューラルネットワーク)を用意しておき, 入力の値に

## 応じて, 一部のエキスパートだけにフォワードする. → すべてのパラメータを

## 使う事にはならないので, 計算量を抑えられる.

## エキスパートA

## （というネットワーク）

## エキスパートB

## （というネットワーク）

## エキスパートC

## （というネットワーク）

## 入力

## 出力

## ＊厳密にいうと, どのエキスパートに振り分けるか

## を決めるための小さなネットワーク（ルーターネ

## ットワーク）が追加で必要となるため, その分若

## 干計算量は増える.

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 混合エキスパート(MoE)

35

## ■

## 計算量を抑えつつ, パフォーマンスを改善できる事が実験で確認されている.

## →同じ計算量で学習するという制約下で, MoEを使ったモデルのほうが使わなかったモデル

## (通常のモデル)よりもパフォーマンスが高い.

## ■

## リーク情報によると, GPT-4はMoEモデル構造を採用しているらしい.

## ■

## 最近の多くのオープンモデル（DeepSeek、Qwen等）もMoEモデルを採用

## ルーターネットワークが

## データのクラスター中心点を

## 基準に各エキスパートに対して

## 事例を振り分け、

## 各エキスパートはその

## クラスター内での分類に特化する

## ような学習が行われた

## 複雑な分類問題にMoEを適用した場合の各事例に対するルータネットワークによる

## エキスパートの振り分けの視覚化

## （t-SNEでデータセットの事例を2次元で視覚化。色はエキスパートの振り分けを示す）

## [23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Switch Transformer：１兆6000億パラメータのMoEモデル

36

## 方法

## T5モデルのフィードフォワード層に

## MoEを適用して，大規模化

## 多くのMoEでは各トークンごとに

## 複数のエキスパートが使われるが

## これを一つのエキスパートのみを

## 使うようにすることで，通信・

## 計算コストの削減を実現

## 結果

## 1.6兆パラメータのモデルの学習で

## T5-XXLモデルに対して4倍の

## 事前学習のスピードアップ

## [25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with

## Simple and Efficient Sparsity. 2021より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## DeepSpeed-MoE: MoEモデルの学習効率の改善

37

## DeepSpeed MoEという最適化された実

## 装により，自己回帰モデルでの

## 品質が同等のDenseモデルと比較して

## 5倍程度学習コストを削減したMoEの

## 学習を実現

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## PR-MoE：MoEモデルの性能を維持したモデルサイズの削減

38

## 方法

## PR-MoEというアーキテクチャを提案

## •

## 各トークンが1つの固定されたMLPと

## 1つのエキスパートの双方を利用

## •

## Transformerの後半の層において

## より多くのエキスパートを活用する

## 結果

## 標準的なMoEより少ないパラメータ数で

## 同等の性能を達成

## •

## 350M: 1/3以下のパラメータで同等性能

## •

## 1.3B: Standard-MoEの約60%のパラメー

## タで同等性能

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■MoEを含む言語モデルにおけるスケール則

39

## (左図) エキスパート数を増やすと対数損失が下がっていくが、特に大きいモデルサイズで、

## 増やしすぎると効果が薄くなる（灰色の線が線形にフィットさせたもの）

## (右図) MoEモデルのパラメータ数を諸々の要素を加味して通常のモデルのパラメータ数に

## 換算すると, スケール則が成立

## 下の線ほど

## 損失が小さい＝

## モデルサイズが

## 大きい

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 通常モデルをMoE化した際に

## 効果のある最大パラメータ数

## ■MoEを含む言語モデルにおけるスケール則

40

## 通常モデルのパラメータ数が大きくなると

## MoE化する効果は比例して低くなっていく

## ↓

## モデルサイズに適したエキスパート数を選択すると良い

## 通常モデルのパラメータ数

## [27] Clark+. Unified Scaling Laws for Routed Language Models. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

41

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

42

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 計算量(C)に関連する取り組みの全体像

43

## 十分な計算量/

## メモリ量を確保し

## 効率よく

## 訓練する必要

## (主に推論時)モデルの軽量化

## を通じて、小規模なGPU環境

## での運用を可能にする

## 訓練において複数のGPUを

## 効率的に活用する

## 課題

## 方向性

## 解決策

## 量子化

## 並列計算

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 計算量(C)に関連する取り組み：並列計算

44

## 十分な計算量/

## メモリ量を確保し

## 効率よく

## 訓練する必要

## 課題

## 方向性

## 解決策

## (主に推論時)モデルの軽量化

## を通じて、小規模なGPU環境

## での運用を可能にする

## 訓練において複数のGPUを

## 効率的に活用する

## 量子化

## 並列計算

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 深層学習における並列化

45

## “DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレームワーク” [32]より抜粋，

## [32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoftより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ZeRO：データ並列時のメモリ効率化

46

## “DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレームワーク” [32]より抜粋，

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoftより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ZeRO：データ並列時のメモリ効率化

47

## Stage 1

## Stage 2

## Stage 3

## • どの要素をメモリで並列するかに応じて，3段階の動作モードが存在

## • 段階が進めほどメモリを削減できるが，通信オーバーヘッドが増加する

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 3D並列化

48

## “DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレームワーク” [32]より抜粋，

## • 並列化の戦略ごとに通信オーバヘッドが異なる

## テンソル並列>> パイプライン並列

## • 3D並列化: GPU・ノードの配置に応じて通信コストをおさえて並列化

## パイプライン並列

## データ並列+ZeRO

## 4枚のGPUを持つ8ノードで

## 3D parallelismを構成した例

## 同色のGPUは同一ノードに配置されて

## いることをあらわす

## •

## 高オーバーヘッドのテンソル並列を

## ノード内に配置

## •

## 低オーバヘッドのパイプライン並列を

## ノードをまたいで配置

## •

## データ並列とZeRO stage 1の組み合わせ

## によって、GPUメモリの効率を高める

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoftより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| ZeROは環境設定を記述するだけで利用可能

49

## ＊代表的なライブラリ：deepspeed

## [34] Microsoft, https://github.com/microsoft/DeepSpeedより引用

## [35] DeepSpeed, https://www.deepspeed.ai/docs/config-json/より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## エキスパート並列化

50

## “NVIDIA NeMo Framework User Guide - Parallelisms” [55]より抜粋，

## • MoEモデル専用の並列化手法

## • MoEの各エクスパートを異なるGPUに配置する

## • 行列を分割して複数のGPUで保持するテンソル並列と類似している

## • 全ての層に適用されるテンソル並列化と異なり、エキスパート並列化は、

## エキスパート層にのみ適用される

## [55] NVIDIA NeMo Framework User Guide - Parallelisms, NVIDIAより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 計算量(C)に関連する取り組み：量子化

51

## 十分な計算量/

## メモリ量を確保し

## 効率よく

## 訓練する必要

## 課題

## 方向性

## 解決策

## (主に推論時)モデルの軽量化

## を通じて、小規模なGPU環境

## での運用を可能にする

## 訓練において複数のGPUを

## 効率的に活用する

## 量子化

## 並列計算

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 量子化とは

52

## •

## モデルパラメータのデータタイプを

## 浮動小数点(Float型)から整数(Int型)に変換して演算処理を行う

## •

## 推論時に, 必要メモリ量が削減できる.

## •

## ナイーブにこれを行うと性能劣化が発生する.

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers, Accelerate and bitsandbytes,

Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-summary-of-llmint8-zero-degradation-matrix-multiplication-for-large-language-modelsより引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLM.int8()：性能劣化なしに可能な量子化方法

53

## 方法

## 16ビットの行列乗算で異常値の特徴を

## 分離する混合精度分解を行い，

## 大部分の値を8ビットで，

## 外れ値のみを16ビットで表現する

## 結果

## 16ビットと比較して約50%のメモリ

## 削減が可能な場合を示す

## 175Bまでのパラメータを持つLLMに

## おいて，性能劣化なしに推論を行う

## ことが可能であることを経験的に示す

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLM.int8()：性能劣化なしに可能な量子化方法

54

## Step1. 入力された隠れ状態から,

## 列単位で外れ値（閾値より大きい値）

## を抽出する。

## Step2. 外れ値の行列については,

## FP16のまま行列演算. 外れ値ではな

## い行列については, INT8に変換して

## （量子化して）行列演算.

## Step3. ２つの出力値が存在する。

## INT8の出力値はFP16に戻して、２つ

## の出力値を加算して, FP16として出

## 力値をリターンする.

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers, Accelerate and

bitsandbytes, Hugging Faceより引用

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## k-bitスケール則

55

## •

## モデルのメモリ容量（ビット数）を

## 固定した際、モデルのサイズと

## 量子化をどのように設定すべきか

## 例：30Bの8-bitモデルと60Bの

## 4-bitモデルは同一のメモリ容量と

## なる

## •

## メモリ容量を固定した場合、

## 4bit量子化が最もゼロショットが

## 高かった

## •

## 3bitにおいてはモデルサイズが

## 大きくなると性能が不安定に

## →post-hocな量子化では、4-bitは

## 最低必要?

[56] Dettmers+. The case for 4-bit precision: k-bit Inference Scaling Laws. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 量子化によりEmergent Abilityは失われないか

56

## ・Emergent AbilityはLLMの重要な特性

## ・in-context learning, chain-of-thought reasoning, instruction-followingの能力を計測

## ・結果として4ビットまでの量子化モデルではEmergent Abilityの維持を確認

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 訓練時から1bit/1.58bit量子化を行う: BitNet

57

## •

## 量子化を適用したモデルを事前学習して構築

## •

## 左図: Attention・MLPに含まれる線形層を全て1bit用に拡張された線形層（BitLinear）に置き換えて

## 構築

## •

## 右図: モデルのビット数（メモリ容量）で比較して既存のLLMの性能を大きく

## 超えたことを報告

## BitNet: パラメータを2値（{-1, +1}; 1bit）／3値（{-1, 0, 1}; 1.58bit）であらわす

[57] Wang+. BitNet: Scaling 1-bit Transformers for Large Language Models. 2023より引用

[58] Ma+. BitNet b1.58 2B4T Technical Report. 2025より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

58

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

59

## •

## それぞれの要素のスケールにおける問題点

## •

## スケールするための技術：パラメータ数(N)に関連する取り組み

## •

## スケールするための技術：計算量(C)に関連する取り組み

## •

## スケールするための技術：データ(D)に関連する取り組み

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## データセット(D)に関連する取り組みの全体像

60

## 性能を発揮させる

## ための学習用

## データを用意する

## 必要

## 課題

## 方向性

## 解決策

## データセットの品質を

## 改善する

## 性能を発揮するための

## データセットを探索する

## データ前処理

## データセット整備

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## データセット(D)に関連する取り組み：データセット整備

61

## 性能を発揮させる

## ための学習用

## データを用意する

## 必要

## 課題

## 方向性

## 解決策

## データセットの品質を

## 改善する

## 性能を発揮するための

## データセットを探索する

## データ前処理

## データセット整備

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## どのような学習データで学習するべきか

62

## ■主要なモデルの学習データの構成

## • 最近のモデルは多くのケースでCodeでの学習を行っている．GPT-3はなし．

## • Codeで学習したモデル（例：code-davinci-002）はGPT-3より推論性能が良い

## • ChatGPTもcode-davinci-002をベースに学習されているとされる．

## [2] Zhao+. A Survey of Large Language Models. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 特定ドメインのデータでの継続的な事前学習

63

## 事前学習後に特定ドメインの文書(e.g. arXivの論文要旨)を継続的に学習させる.

## 継続学習したモデルの下流タスクでの性能を評価

## 事前学習の後に継続学習することで、破滅的忘却が起きにくい上、

## 下流タスクでの優れた性能を発揮できることを示す

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

64

## • LLMの事前訓練の予算は計算量（GPU枚数や時間）に比例.

## • 計算量をパラメータ数と学習データ量にどのように配分するかが

## 重要となる.

## • OpenAIによる従来のスケール則[3]はパラメータに対して必要となる

## 学習データ量の見積もりが少なすぎることを指摘.

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chinchilla：最適計算配分に基づきNとDを決めたモデル

65

## データサイズD

## トークンを1.4Tまで増加

## （同じデータの別サブセット）

## ※ Gopherの約4.6倍

## モデルサイズN

## 70Bに設定

## ※ Gopherの約1/4倍

## 結果

## 多くのケースでGopherに勝利

## （提案した関係式の妥当性を示唆）

## [42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 実用的な小さいモデルでは、Chinchilla則よりも多くのデータが必要？

66

## • Chinchilla Trap:

## Chinchillaのモデルサイズ(70B)は

## 大きいため, 推論コストが高い*.

## 推論コストも考慮してより

## 小さなモデルを大規模なデータで

## 訓練するべきではという意見

## • Chinchilla最適なモデルサイズの

## 40-60%以内のモデルサイズで，

## 10-42%の計算量の追加で同性能の

## モデルを学習できる

## Chinchilla最適なモデルと

## 同じ性能を達成するために

## 必要なパラメータ比率（横軸）と

## 計算量（縦軸）の関係

## 最適モデルサイズ

## [43] Harm de Vries, Go smol or go home, Why we should train smaller LLMs on

## more tokens, 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 言語データの枯渇の問題

67

## “Will we run out of data? An analysis of the limits of scaling datasets in Machine

## Learning” [17]

## 過去のWebデータの増え方，学習データの増え方からの予測

## 良質な言語データの枯渇が予測されている．

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 事前学習を通じて知識はどのように学習されていくのか

68

## “How Do Large Language Models Acquire Factual Knowledge During Pretraining?” [60]

## 訓練ステップ数

## 正解のスパンの

## 対数確率の変化

## 黒の点線の部分で知識を記述した文で訓練

## Memorization: 注入した文をそのまま質問として利用

## Semantic: 注入した文を言い換えた質問を利用

## Composition: 複数の文の知識が必要な質問を利用

## •

## LLMの事前訓練時に知識がどのように獲得されていくかを調査

## •

## 知識を記述した文が出現する（点線）たびに正しい知識の生成される確率が高まり、

## 知識が徐々に学習されていく

## •

## 知識が出現しないステップ（900ステップ以降）では、忘却されていく

## LLMに知識を教えるためには、訓練データ中に

## 繰り返し知識が出現している必要がある

## ↓

## 重要な知識が高い密度に含まれる高品質な訓練データの重要性を示唆

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 合成データでの事前学習

69

## 方法

## 合成データを使った事前学習の効果を1.000以上の

## LLMを10万GPU時間を使って訓練して検証

## 合成データの種類：

## •

## ウェブ言い換え: LLMを使ったウェブデータの

## 言い換えによる合成データ生成

## - HQ: 綺麗なテキストへの言い換え

## - QA: QAへの言い換え

## •

## TXBK: 合成テキストブック: LLMを使って

## 教科書スタイルのデータを0から作成

## 結果

## •

## ウェブデータと合成データを混ぜた場合に

## 訓練の効率が大幅に改善

## •

## 合成データのみで訓練すると性能悪化

## →特に合成テキストブックのみでは顕著に悪化

## •

## 全ての種類で、ウェブデータに33%の比率で

## 合成データを混ぜた場合に最善の性能を達成

## [59] Kang+. Demystifying Synthetic Data in LLM Pre-training: A Systematic

## Study of Scaling Laws, Benefits, and Pitfalls. 2025より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## データが有限で計算量が無限な設定での学習

70

## •

## LLMの事前訓練に投下される計算量は年々増えているが、

## データは限られている

## •

## データ量が有限であることを前提に、計算量をスケールする場合、性能を改善できるか？

## •

## LLMの標準的な訓練設定ではスケールできない（左枠）

## エポック数を増やす→オーバフィットして性能低下（左枠の左図）

## モデルのサイズを増やす→十分に訓練できず性能低下（左枠の右図）

## •

## 訓練設定を適切に調整すればスケールできる（右枠）

## 標準的な訓練設定での学習では固定のデータ量で計算量だけ増やしてもスケールしない

## 訓練設定を適切に設定すればスケールできる

## 大きいモデルほど

## •

## 小さい学習率

## •

## 少ないエポック数

## •

## 大きいweight decay

## （強い正則化）

## [61] Kim+. Pre-training under infinite compute. 2025より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## データセット(D)に関連する取り組みの全体像

71

## 性能を発揮させる

## ための学習用

## データを用意する

## 必要

## 課題

## 方向性

## 解決策

## 少量の高品質な

## データセットを用意する

## 性能を発揮するための

## データセットを探索する

## データ刈り込みなど

## データセット整備

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## RefinedWeb: データの前処理(フィルタリング)の工夫

72

## Webデータのみでの5T Tokenのデータセット．600GがPublic．

## フィルタリングの工夫(後述)などにより以前より大規模なデータを構築．

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Macrodata Refinement：データの厳密な絞り込みパイプライン

73

## ・複数のフィルタリング、重複削除を組み合わせた厳密なデータの絞り込みを実施

## ・一連のパイプラインでCommonCrawl中の約90%の文書が取り除かれる

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Macrodata Refinement：データの厳密な絞り込みパイプライン

74

## ●URL filtering: 有害なURLから取得したテキストを排除

## ●Text extraction: テキストのメインコンテンツテキストのみ抽出（ヘッダー

## や広告部分は要らない）

## ●Language identification: 特定の言語テキストのみ残す

## ●Repetition removal: テキスト内の繰り返し文を排除

## ●Document-wise filtering: スパムテキストをフィルタ

## ●Line-wise corrections: テキスト内の行レベルのフィルタ（例SNSの

## 「いいね」）

## ●Fuzzy deduplication: 異なるドキュメントに類似文章が存在した場合は排除

## (MinHash [40])

## ●Exact deduplication:異なるドキュメントに指定したトークン数以上の完全

## 一致が存在した場合は排除

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023より引用

[40] Daisuke Okanohara, MinHashによる高速な類似検索, Preferred Networks Research&Development, 2011より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## FineWeb-Edu: LLMが評価した教育的価値を使った前処理

75

## FineWeb-Edu: LLMが評価したテキストの教

## 育的価値を使って前処理を行う

## 方法

## 大規模テキストにLLMの推論を適用するのは

## コストが高いため、軽量化が必要。

## →LLMの評価結果を使って軽量分類器を訓練

## •

## 46万件のウェブ記事の「教育的価値」を

## LLMに評価させて訓練データを作成

## •

## 小さいモデルを学習して評価器を作成

## 結果

## •

## 前処理を行う前のデータ（FineWeb）や既

## 存データ（Matrix）と比べて、知識や

## 推論が必要なタスクの性能が大きく改善

[62] Penedo+. The FineWeb Datasets: Decanting the Web for the Finest Text

Data at Scale. 2024より引用

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 本日のまとめ

76

## モデルのスケールを支える技術動向について紹介しました．

## 1. なぜモデルをスケールさせるのか

## 1) スケール則の成立, 2) Emergent Ability

## 3. モデルをスケールする上での問題は依然として存在

## •

## スケールにつれて必要となるコストの増加，データの不足，etc..

## 2. スケール則はモデルの性能と{パラメータ数, データ量, 計算量}の関係を明らかにした

## •

## スケール則で性能の予測ができるようになり, 大規模なモデルへの投資リスクが軽減.

## 4. モデルのスケールを支える様々な研究・開発が行われている

## •

## パラメータ数(P)：よりメモリ効率，演算効率の優れたモデルの提案

## •

## 計算量(C)：効率的な学習、推論方法の整備

## •

## データセットサイズ(D)：データの量と質の工夫

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

77

[1] Bao Hua Choo, The emergence of Large Language Models (LLMs), The low down, https://thelowdown.momentum.asia/the-emergence-of-large-language-

models-llms/, アクセス日: 2023/11/16

[2] Zhao+. A Survey of Large Language Models. 2023. In arXiv:2303.18223

[3] Kaplan+. Scaling Laws for Neural Language Models. 2020. In arXiv:2001.08361

[4] Wei+. Emergent Abilities of Large Language Models. 2022. In arXiv:2206.07682

[5] Schaeffer+. Are Emergent Abilities of Large Language Models a Mirage?. 2023. In arXiv:2304.15004

[6] Power+. Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets. 2022. In arXiv:2201.02177

[7] Liu+. Towards Understanding Grokking: An Effective Theory of Representation Learning. 2022. In NeurIPS2022

[8] Hestness+. Deep Learning Scaling is Predictable, Empirically. 2017. In arXiv:1712.00409

[9] Brown+. Language Models are Few-Shot Learners. 2020. In NeurIPS2020

[10] Anil+. PaLM 2 Technical Report. 2023. In arXiv:2305.10403

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

78

[11] Henighan+. Scaling Laws for Autoregressive Generative Modeling. 2020. In arXiv:2010.14701

[12] Ganguli+. Predictability and Surprise in Large Generative Models. 2023. In arXiv:2202.07785

[13] OpenAI. GPT-4 Technical Report. 2023. In arXiv:2303.08774

[14] Abhinav Venigalla, Linden Li, Billion-Parameter GPT Training Made Easy, MosaicML, https://www.mosaicml.com/blog/billion-parameter-gpt-

training-made-easy, アクセス日: 2023/11/16

[15] Vaswani+. Attention Is All You Need. 2017. In NeurIPS2017

[16] Jaiyam Sharma, Understanding Attention Mechanism in Transformer Neural Networks, LearnOpenCV, https://learnopencv.com/attention-

mechanism-in-transformer-neural-networks/, アクセス日: 2023/11/16

[17] Villalobos+. Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning. 2022. In arXiv:2211.04325

[18] Tay+. Efficient Transformers: A Survey. 2020. In arXiv:2009.06732

[19] Child+. Generating Long Sequences with Sparse Transformers. 2019. In arXiv:1904.10509

[20] Zahher+. Big Bird: Transformers for Longer Sequences. 2020. In NeurIPS2020

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

79

[21] Dao+. FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. 2022. In NeurIPS2022

[22] Tri Dao. FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. 2023. In arXiv:2307.08691

[23] Chen+. Towards Understanding Mixture of Experts in Deep Learning. 2022. In NeurIPS2022

[24] Shazeer+. Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer. 2017. In ICLR

[25] Fedus+. Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity. 2021. In arXiv:2101.03961

[26] Rajbhandari+. DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale. 2022. In ICML2022

Proceedings of the 39th International Conference on Machine Learning, PMLR 162:18332-18346

[27] Clark+. Unified Scaling Laws for Routed Language Models. 2022. In arXiv:2202.01169

[28] Zhai+. An Attention Free Transformer. 2021. In arXiv:2105.14103

[29] Peng+. RWKV: Reinventing RNNs for the Transformer Era. 2023. In arXiv:2305.13048

[30] Sun+. Retentive Network: A Successor to Transformer for Large Language Models. 2023. In arXiv:2307.08621

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

80

[31] Gu+. Efficiently Modeling Long Sequences with Structured State Spaces. 2022. In ICLR2022

[32] Microsoft DeepSpeed Team, DeepSpeed: Extreme-scale model training for everyone, Microsoft, https://www.microsoft.com/en-

us/research/blog/deepspeed-extreme-scale-model-training-for-everyone/, アクセス日: 2025/10/05

[33] Rajbhandari+. ZeRO: Memory Optimizations Toward Training Trillion Parameter Models. 2019. In arXiv:1910.02054

[34] Microsoft, https://github.com/microsoft/DeepSpeed, アクセス日: 2023/11/16

[35] DeepSpeed, https://www.deepspeed.ai/docs/config-json/, アクセス日: 2023/11/16

[36] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers,

Accelerate and bitsandbytes, Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-introduction-to-8-bit-matrix-

multiplication-for-transformers-at-scale-using-hugging-face-transformers-accelerate-and-bitsandbytes, アクセス日: 2023/11/16

[37] Dettmers+. LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale. 2022. In NeurIPS2022

[38] Liu+. Do Emergent Abilities Exist in Quantized Large Language Models: An Empirical Study. 2023. In arXiv:2307.08072

[39] Penedo+. The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only. 2023. In

arXiv:2306.01116

[40] Daisuke Okanohara, MinHashによる高速な類似検索, Preferred Networks Research&Development, 2011,

https://tech.preferred.jp/ja/blog/minhash/, アクセス日: 2023/11/16

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

81

[41] Cossu+. Continual Pre-Training Mitigates Forgetting in Language and Vision. 2022. In arXiv:2005.09357

[42] Hoffmann+. Training Compute-Optimal Large Language Models. 2022. In NeurIPS2022

[43] Harm de Vries, Go smol or go home, Why we should train smaller LLMs on more tokens, 2023, https://www.harmdevries.com/post/model-size-

vs-compute-overhead/, アクセス日: 2023/11/16

[44] Sorscher+. Beyond neural scaling laws: beating power law scaling via data pruning. 2022. In NeurIPS2022

[45] Tirumala+. D4: Improving LLM Pretraining via Document De-Duplication and Diversification. 2023. In arXiv:2308.12284

[46] Zhou+. LIMA: Less Is More for Alignment. 2023. In arXiv:2305.11206

[47] Dzmitry Bahdanau, The FLOPs Calculus of Language Model Training, Medium, 2022, https://medium.com/@dzmitrybahdanau/the-flops-

calculus-of-language-model-training-3b19c1f025e4, アクセス日: 2023/11/16

[48] Wan+. Efficient Large Language Models: A Survey. 2024. In arXiv:2312.03863

[49] Patro and Agneeswaran. Mamba-360: Survey of State Space Models as Transformer Alternative for Long Sequence Modelling: Methods,

Applications, and Challenges. 2024. In arXiv:2404.16112

[50] De+. Griffin: Mixing Gated Linear Recurrences with Local Attention for Efficient Language Models. 2024. In arXiv:2402.19427

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

82

[51] Qu+. A Survey of Mamba. 2024. In arXiv:2408.01129

[52] Feng+. Beyond Model Collapse: Scaling Up with Synthesized Data Requires Reinforcement. 2024. In arXiv:2406.07515

[53] Gerstgrasser+. Is Model Collapse Inevitable? Breaking the Curse of Recursion by Accumulating Real and Synthetic Data. 2024. In

arXiv:2404.01413

[54] Munkhdalai+. Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention. 2024. In arXiv:2404.07143

[55] NVIDIA NeMo Framework User Guide - Parallelisms, NVIDIA, https://docs.nvidia.com/nemo-framework/user-

guide/latest/nemotoolkit/features/parallelisms.html, アクセス日: 2025/10/05

[56] Dettmers+. The case for 4-bit precision: k-bit Inference Scaling Laws. 2023. In arXiv:2212.09720

[57] Wang+. BitNet: Scaling 1-bit Transformers for Large Language Models. 2023. In arXiv:2310.11453

[58] Ma+. BitNet b1.58 2B4T Technical Report. 2025. In arXiv:2504.12285

[59] Kang+. Demystifying Synthetic Data in LLM Pre-training: A Systematic Study of Scaling Laws, Benefits, and Pitfalls. 2025. In arXiv:2510.01631

[60] Chang+. How Do Large Language Models Acquire Factual Knowledge During Pretraining?. 2024. In arXiv:2406.11813

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## References

83

[61] Kim+. Pre-training under infinite compute. 2025. In arXiv:2509.14786

[62] Penedo+. The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale. 2024. In arXiv:2406.17557

[63] Younes Belkada, Tim Dettmers, A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers,

Accelerate and bitsandbytes, Hugging Face, https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-summary-of-llmint8-zero-

degradation-matrix-multiplication-for-large-language-models, アクセス日: 2026/05/25

[64] sunbluesome. Sparse Transformerを理解したい, Zenn, https://zenn.dev/sunbluesome/articles/5f6a86dfa1e1be, アクセス日: 2023/11/16

## [65] weights & biases, 「LLMをゼロからトレーニングするためのベストプラクティス」, https://wandb.ai/site/resources/whitepapers/llm-

whitepaper-japan/ アクセス日: 2026/05/25

[66]  iwiwi, github, https://gist.github.com/iwiwi/fc174b1f2341c2c0170be87c5b2e1d31, アクセス日:2026/05/25

大規模言語モデル講座講義資料

LLM

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0
