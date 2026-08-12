# Day 1

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

## Overview of Large Language Models

## 准教授岩澤有祐

許諾なく撮影や第三者

への開示を禁止します

## 大規模言語モデル講座2025

## ※ 今回は個別の技術を深ぼるというより概要を把握する目的です．

## たくさんの用語がでてきますが、すべてこの回で覚えてほしいわけではないです．

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

3

## 岩澤有祐（いわさわゆうすけ）

3

## 2017年東京大学工学系研究化博士課程修了（松尾研）．卒業後特任研究員，特任助教

## などを経て2024年1月より技術経営戦略学専攻で准教授．

## ■研究テーマ等

## -

## 修士までは障害者支援への機械学習技術の応用

## -

## 博士から深層学習の主に転移学習技術に関する研究

## ■生成AIに関連する活動

## -

## “Large-Language Models are Zero-Shot Reasoners”, NeurIPS2022 など

## -

## JSAI2023，CSS2023での「基盤モデルの技術と展望」のチュートリアル[Speaker Deck]

## -

## 松尾研主催大規模言語モデル講座の全体の設計

## -

## 岸田総理等への大規模言語モデルの講義（180分）

## DL輪読会

## 松尾研メンバ，講義受講生など

## が参加する勉強会を主催．

## 2015年~ 累計350回以上

## 実施（毎週金曜朝10:00）

## DL本（監訳，翻訳）

## Goodfellowらが執筆した深層学習

## の教科書の監訳，翻訳．2018年

## に出版．

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

4

## 目次

4

## • LLMの概要(LLMをなぜいま学ぶのか？）

## • 各回の概要

## • 日本のLLMを取り巻く環境

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

5

## モチベーション

5

## •

## 今，自然言語を操るアシスタントAIを作りたいとします

## •

## 例えば，質問に対して正しい答えを出力してほしいとします

## •

## 例：Q. 日本の首都は？A. 東京

## •

## 例えば，”文章を英語に翻訳して” と言ったら翻訳した文章を出力してほしい

## とします

## •

## 例えば，「テトリスのアプリを作って」といったらそのコードを生成してほ

## しいとします

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

6

## 今はこれらはWeb上や簡単なプログラムで実現できるように

6

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## AI + エコシステムの進展の例| Hugging Face

7

## ①100万を超えるモデル

## ②言語/ 画像/ 音声/

## マルチモーダルなど

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## AI + エコシステムの進展の例| Hugging Face

8

## ①100万を超えるモデル

## ②言語/ 画像/ 音声/

## マルチモーダルなど

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

9

## これらはどのように実現されているか？- 言語モデルの歴史

9

## •

## 単語の系列（文章）を𝑥1, 𝑥2, ⋯, 𝑥𝐿としたとき，その生成確率𝑝(𝑥1, 𝑥2, ⋯, 𝑥𝐿)

## を割り当てる確率モデル𝑝のこと

## 𝑝(日本, の, 首都, は, 東京) = 0.02

## 𝑝(日本, の, 首都, は, パリ) = 0.00001

## 𝑝(東京, の, 首都, は, 日本) = 0.0005

## •

## 様々な言語タスクがこの生成確率の推定問題として扱うことができる

## 例：QA（ある質問に続くのにふさわしい答えは？）

## 例：翻訳（ある英語文に続くのにふさわしい日本語は？）

## •

## 例：コード生成（ある指示文にふさわしいコードは？）

## •

## この生成確率をどう求めるか？が言語モデル技術的な問題の一つ

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

10

## 自己回帰言語モデル(Autoregressive Language Models)

10

## •

## 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿を条件分布の積として表現する

## 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿= 𝑝𝑥1 𝑝𝑥2 𝑥1 ⋯𝑝(𝑥𝐿|𝑥1, 𝑥2, ⋯, 𝑥𝐿−1)

## •

## このように確率の連鎖律で分解したモデルを特に自己回帰言語モデルと呼ぶ

## •

## 条件付き確率がわかると，生成することもできる

## 𝑝東京日本, の, 首都, は) = 0.2

## 𝑝パリ日本, の, 首都, は) = 0.001

## 𝑝カイロ日本, の, 首都, は) = 0.0005

## •

## この条件付き確率をどう求めるか？

## …

## 日本の首都は→ 東京

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

11

## ニューラル言語モデル

11

## •

## 条件付き確率を何らかのニューラルネットで推定したモデル

## •

## Webのデータを模擬するように（尤度を最大化するように）訓練

## 日本

## の

## 首都

## は

## 東京

## 京都

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

12

## Transformer以前のニューラル言語モデルの課題

12

## •

## 畳み込みネットやMLP等では，長いコンテキストの処理が難しい

## •

## 例えば翻訳では，元文をしっかり反映して翻訳文を決める必要がある．

## •

## ある程度長い系列情報を処理できないと解けないタスクがある

## •

## RNN系列のモデルは，学習が並列化できずにスケール化が困難

## •

## データを逐次的に処理する性質上，学習や推論の並列化が困難

## •

## そのほかにも学習が難しいという問題も（勾配消失問題）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Transformer

## “Attention is All You Need”, NeurIPS 2017

## 13

## • Googleを中心にした研究チームが2017年に発表

## • Self Attentionを中心にしたネットワーク構造（左）

## ※構造の詳細は別日に話します

## • 主に翻訳等の教師あり学習で性能検証（右）

## 例：英語文→Transformer →ドイツ語文

## となるように誤差逆伝播で訓練

[1] Ashish Vaswani et al. (2017) “Attention Is All You Need” NeurIPS 2017 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Generative Pretraining Transformer (GPT)

## “Improving Language Understanding by Generative Pre-training”, 2018

## 14

## Pre-training （事前学習）

## Transformer

## Input: Language models determine

## [mask]

## Output: word probability

## by analyzing text data

## Original: Language models determine word

## probability by analyzing text data

## • OpenAIにより2018年に発表されたモデル

## • 事前学習にTransformerを利用

## （Transformerを使った言語モデル）

## • 具体的には次に来る単語をTransformerで

## 予測するように学習（左図）

## Book Corpusという未発表書籍を利用

## • GPT, GPT-2, GPT-3とバージョンを経る

## ごとに学習データ数やモデルサイズが増加

[2] Alec Radford et al. (2018) “Improving Language Understanding by Generative Pre-training” を参考

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 2020年のGPT-3登場後，大規模モデルの発表は加速度的に増加

## 15

[3] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” arXiv:2303.18223より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-4の持つ知識

16

## • OpenAIにより2023年に発表されたモデル

## （詳細は未公開，リーク情報はあり）

## • 司法試験やSAT/GREなどの多様な試験で

## 好成績

## 例:Uniform Bar Examでは298/400

## (~90th)

## 例：GRE (Quantitative)が163/179

## (~80th)

## • 一方コーディング能力などではまだ低い

## スコア（現在は大幅に改善）

[4] OpenAI 2023 “GPT-4 Technical Report” より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Igak QA

## “Evaluating gpt-4 and ChatGPTt on Japanese medical licensing examinations”2023

## 17

## •

## 言語モデル(GPT-4 and ChatGPT）を新たに作成した日本の医療ライセンス試験6年分の

## データセット（Igaku-QA)を構築してベンチマーク

## •

## (1) 人間の平均的な受験者よりは悪い，(2) 禁忌技を選択する傾向にある，といった問題は

## あるものの試験ボーダーは突破

[5] Jungo Kasai et al. (2023), “Evaluating gpt-4 and ChatGPTt on Japanese medical licensing examinations” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 大規模言語モデルを活用する技術も進展｜Context Engineering

## “A Survey of Context Engineering for Large Language Models”, 2025

## 18

## •

## 言語モデルが持っている知識を使うだけでなく、必要なコンテキストを選択し処理する技術

## •

## RAG / ツール利用（検索）/ Deep Research / Memoryなど様々な技術が研究

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 2025年に登場した大規模言語モデル（Generated by GPT5)

## 19

## モデル名

## 開発元

## 公開時期（2025）

## オープン/クローズド

## GPT-5

## OpenAI

## 8月

## クローズド

## GPT-4.5

## OpenAI

## 2月

## クローズド

## GPT-OSS

## OpenAI

## 8月

## オープン

## Llama 4 Scout

## Meta

## 4月

## オープン

## Llama 4 Maverick

## Meta

## 4月

## オープン

## DeepSeek-R1

## DeepSeek

## 1月

## オープン

## DeepSeek-V3

## DeepSeek

## 3月頃

## オープン

## Qwen3 (Think)

## Alibaba/Qwen

## 4月

## オープン

## Qwen2.5-Max

## Alibaba/Qwen

## 初頭

## オープン

## Claude 3.7 Sonnet

## Anthropic

## 2月

## クローズド

## Grok-3

## xAI

## 2月

## クローズド

## BitNet b1.58 2B4T

## Ma 他

## 4月

## オープン

## LLaDA

## ML-GSAI 他

## 2月

## オープン

## MMaDA

## 研究チーム

## 5月

## オープン

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルに関するトレンド

## 20

## ①Reasoningモデルと呼ばれる，これまでより推論能力が著しく高いモデルの登場

## （自ら誤りに気づく”Aha Moment”）

## ⇒ これまでより複雑なベンチマークの整備、推論プロセスの分析などが進展

## ②性能の高い公開モデルの増加

## ③（様々な意味で）効率の良いモデル構造（拡散言語モデルなど）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ベンチマークの高度化

## 21

## ■SWE Bench：Issueに対するPRを作成する能力を評価

## ■Humanity Last Exam:

## Humanity Last Examというチャレンジングな問題（登場次点は

## SoTAが9%，今は21.6%

## 問題例

## 「アマツバメ目のハチドリは、尾羽下制筋の広がった交差状の腱膜の尾側

## 外側部分に埋め込まれた、左右対になった楕円形の種子骨を持つ。こ

## の種子骨によって支えられている腱ペアはいくつあるか？数字で答えよ」

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ここまでのまとめと本講座の趣旨

22

## ■ここまでのまとめ

## • 言語モデルとは単語列の生成確率をモデル化したもの

## 自己回帰言語モデル/ ニューラル言語モデル/ GPT

## • 2025年になってもその活用方法/ モデル自体（大規模推論モデル，拡散言語モデ

## ル）/ 評価方法に関する研究開発は進展している

## ■このあとの話し

## 原理は非常にシンプル．なぜいま言語モデルなのか？

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## なぜ今言語モデルなのか

23

## [1] 大規模化に伴う汎用性

## [2] 言語以外へのドメインへの影響

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Transformerを使った言語モデルの巨大化

24

## 2019年

## 2020年

## 2018年

## 2023年

## 基本的にはいずれも2017年に発明されたTransformerと呼ばれる構造を利用．

## GPT-3登場以降，米国企業を中心に複数の研究機関が独自の大規模言語モデルを開発．

[6] Momentum Works 2023 “The future by ChatGPT”より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## なぜいまLLMを学ぶのか？1. Scaling and Emergence

25

## モデルサイズが巨大なときのみ解けるタスクが存在

## Scaling Law

## Emergent Ability

## 3つの変数に関するべき乗に従って上がる.

## 計算資源C, データセットサイズD, パラメータ数N

[7] Jared Kaplan et al. (2020), “Scaling Laws for Neural Language Models” より引用(左図)

[8] Jason Wei et al. (2022), “Emergent Abilities of Large Language Models” より引用(右図)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-3の学習データ量

## “Language Models are Few-Shot Learners”, 2020

## 26

## GPT-3の事前学習トークン数

## • 約5000億トークン*のテキストを利用

## *トークンとは，言語AIが処理する単位．

## 日本語だと大体1文字1トークン

## • *書籍でいうとGPT-3は約500万冊に相当

## 参考：東大図書館が約130万冊，

## 国会図書館が約4700万冊

## • *リーク情報によるとGPT-4は約1.3億冊に相当

[9] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”, NeurIPS2020 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 大規模な計算を行うためのツール：GPU

## 27

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 大規模なモデル/ データを支える大規模な計算資源（GPU）

28

## AIの開発には、膨大なデータを高速に処理する計算資源が必要。現在よく用いられる計算資源はGPUと呼ばれるもの

## で、支配的なシェアを持つNVIDIAも急成長。日本もGPUの確保に動いているが、海外勢との格差は大きい

## GPU (H100, A100, V100などの種類が存在）

## GPT3相当の場合：A100 ×

## 1,200基× 30日

## GPT4相当の場合：A100 × 25,000基× 100日(*)

## 今回の演習の場合：A100 ×

## 8基× 1時間

## (*)リーク情報。OpenAIの公式発表ではない

## 世界のGPUシェアの90％を占めるNVIDIA（米）はAI需

## 要を追い風に急成長。一時は世界の時価総額首位に

## 国内外の代表的なGPUクラスタ(*)

## (*)GPUを搭載した複数の計算機をまとめて提供するシステム

## ・産総研のABCI：

## 960基のA100 GPU → 6,128基のH200 GPU

## *2025年1月アップグレード

## ・Softbank：6,000基のGPU

## ・さくらインターネット：2,000基のH100GPU

## 1企業で数十万~百万基のH100 GPUを保有

## (以下、24年単年の購入数)

## ・Google：169,000基

## ・Amazon：196,000基

## ・Meta：224,000基

## ・Microsoft：485,000基

## この差は、根本的には前述の構造的な問題、つまりITサービ

## スと生成AIの間の好循環が作り出せているか、から来ている

[10] Dan Swinhoe (2024), "Microsoft bought twice as

many Nvidia Hopper GPUs as other big tech

companies - report",

DataCenterDynamics,https://www.datacenterdynamics

.com/en/news/microsoft-bought-twice-as-many-nvidia-

hopper-gpus-as-other-big-tech-companies-report/

## 海外

## 国内

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## スケールがもたらしたもの– 汎用性ー

29

## Translation (Few-Shot)

## Translation (Zero-Shot)

## Summarization (Zero-Shot)

## •

## Starting with “TL;DR” drastically

## improves the performance

## Many other examples

## Pre-training （事前学習）

## LLMs (Transformer)

## Input: Language models determine

## [mask]

## Output: word probability

## by analyzing text data

## Original: Language models determine word

## probability by analyzing text data

[9] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■補足| 基盤モデル（補足）

## “On the Opportunities and Risks of Foundation Models”, 2021

## 30

## •

## 2021/8/16初出のホワイト

## ペーパーで登場した言葉

## •

## Stanfordの研究機関の名称にもなって

## いる（青枠）

## •

## 多様なタスクに適用可能な巨大モデル

## によるパラダイムシフト

## （Abstractより抜粋）

## “AI is undergoing a paradigm shift with the

## rise of models (e.g., BERT, DALL-E, GPT-

## 3) that are trained on broad data at scale

## and are adaptable to a wide range of

## downstream tasks. We call these models

## foundation models to underscore their

## critically central yet incomplete character”

[11] Rishi Bommasani et al. (2021) “On the Opportunities and Risks of Foundation Models より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## なぜ今言語モデルなのか

31

## [1] 大規模化に伴う汎用性

## [2] 言語以外へのドメインへの影響

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-4による画像の認識（とロボット応用）

## マルチモーダルな基盤モデル

32

## “GPT-4 Technical Report ”, 2024

## [13] Figure AI Inc. (2024), "Figure Official Website" https://www.figure.ai/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ■LLMの活用| Say-Can and Say-Can-PaLM

## “Do As I Can, Not As I Say: Grounding Language in Robotic Affordances”, 2022

## 33

## • 言語モデルが出力したスキルの実行可能性（Skill Affordance）を考慮して選択

## – 実行可能性はTDで学習

## • 言語モデルをよくする（PaLMを使う）と性能が改善する

## ※ 実行可能なスキル（低レベル方策）はあらかじめ用意されている点に注意

[14] Michael Ahn et al. (2022),“Do As I Can, Not As I Say: Grounding Language in Robotic Affordances” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 行動系列の生成（実行結果）

## 松尾研での研究例

## 34

## 成果例：RoboCup Japan Open 2023優勝，RoboCup世界大会3位

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Robotics Foundation Model

## Real World

## Envonment

## Robotics

## Foundation

## Model

## action

## observation

## Training with

## large and diverse data

## (action / observation pair)

## Industrial Application

## Autonomous Driving

## Life Support

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Robot Transformer  (RT-1)

## “RT-1: Robotics Transformer for Real-World Control at Scale”, 2022

## 36

## モデル

## •

## Efficient NetとTransformerの組

## み合わせ

## •

## インストラクションに従い

## 動作生成

## データ

## •

## EDR13台，17ヶ月，744タスク，

## 13万デモ

## •

## 訓練：97%で動作

## •

## 汎化：種々の意味で大幅向上

## （未知タスク，未知ソース等

## •

## Long Horizonなタスクも可

## ※ 類似研究にGato，BC-Zなど

[15] Anthony Brohan et al. (2022), “RT-1: Robotics Transformer for Real-World Control at Scale” より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Collaboration with Google

## RT-X Project

## - Awarded Best Paper at ICRA 2024

[16]O'Neill, Abby, et al. (2023), "Open x-embodiment: Robotic learning datasets and rt-x models.", arXiv preprint

arXiv:2310.08864, Available at: https://arxiv.org/abs/2310.08864

## ●

## Google Deepmind and 21 research institutes collect offline robot datasets with

## a unified format

## ●

## 22 robot types, 527 skills (160,266 tasks), over 1 million episodes

## ●

## Better performance than the model trained on individual data

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Vision Language Action Model

38

## • 𝜋0 [Black+ 2024]

## • VLA（Vision-Language-Action）モデル

## • 洗濯物を畳む，卵を割らずにケースに入れるなど，

## 様々なタスクを行うことができる

[17]Physical Intelligence (2024), "π0: A Generalist Model for Physical Intelligence", Physical

Intelligence Blog, Available at: https://www.physicalintelligence.company/blog/pi0より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## AIRoA | AI Robot Association

## Uniqueness

## ●

## Led by academia

## ●

## Openness

## ●

## Reward design

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## World Simulator | Sora（Open AI）

40

## Prompt: A young man at his 20s is

## sitting on a piece of cloud in the sky,

## reading a book.

## Prompt: Photorealistic closeup video of

## two pirate ships battling each other as

## they sail inside a cup of coffee.

## [18]OpenAI (2024), "Sora: Creating video from text", OpenAI Official Website, https://openai.com/sora

## [19] OpenAI (2024), "Video generation models as world simulators", OpenAI Research,

## https://openai.com/research/video-generation-models-as-world-simulators

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ここまでのまとめと本講座の趣旨

41

## ■ここまでのまとめ

## • 言語モデルとは単語列の生成確率をモデル化したもの

## 自己回帰言語モデル/ ニューラル言語モデル/ GPT

## • 2025年になってもその活用方法/ モデル自体（大規模推論モデル，拡散言語モデ

## ル）/ 評価方法に関する研究開発は進展している

## • 原理は非常にシンプル．なぜいま言語モデルなのか？

## • 1. モデル，データ，計算量のスケールによりできることが急速に広がっている（汎化性）

## • 2. 言語モデルの発展が他の領域にも影響を与えている

## ■本講座の趣旨

## • LLMの技術的背景，原理や限界を理解する．

## • ハイプとしてではなく活用する技術として捉えられるようになる

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

42

## 小島武（こじまたけし）

42

## ❏略歴

## ❏2023.3 東京大学大学院工学系研究科TMI 博士課程修了

## ❏2023.4～同研究科特任研究員

## ❏2025.1～同研究科特任助教

## ＊以前はITエンジニアをしてました.

## ❏活動

## Weblab-10Bの開発，岸田総理・石破総理のLLM特別講座で講師担当，LLM開発コ

## ンペ2024・2025運営のコンテンツリーダー，AI白書2025でSafetyの章を執筆

## ❏研究

## LLMの動作原理の理解と制御（Reasoning Model, 多言語等），Safety (Unlear

## ning, 指示追従能力, ロボット），Transformerモデル構造の改善，などなど

[21]https://github.com/kojima-

takeshi188/zero_shot_cot

[20]Takeshi Kojima, et al. (2025), "A Comprehensive Survey on

Physical Risk Control in the Era of Foundation Model-enabled

Robotics", arXiv preprint arXiv:2505.12583, Available at:

https://arxiv.org/abs/2505.12583

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

43

## 目次

43

## • LLMの概況

## • 各回の概要

## • 日本のLLMを取り巻く環境

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 講座を組み立てるにあたって

## 44

## 大規模言語モデル基礎（10～11月）：

## ・LLMの全体像を理解するために、事前学習・事後学習・データ収集加工・ベンチマーク

## 評価といった学習パイプラインを網羅的に解説。

## ・公開済みモデルやAPIを活用し、推論性能を向上させる手法についても丁寧に紹介。

## 大規模言語モデル応用（12月～2月）：

## ・軽量化・安全対策・解釈性・ドメイン特化・LLMエージェントなど、LLMの社会実装

## に不可欠となる技術を本格的に学べる。

## ・最前線でLLMを研究開発する第一人者による特別講演を行います。

## ・毎年恒例となった「個人型LLM開発コンペ」もパワーアップして開催予定。受講者同

## 士の白熱した技術競争が、学びをさらに深めます。

## 今年度は、「大規模言語モデル基礎」と「大規模言語モデル応用」に講座を分けます。

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMの学習パイプラインからみた講座の構成

45

## 事前学習

## 大規模コーパスによる自己教師あり学習を通して、言語モデルに

## 語彙・文法・知識といった基本的な言語理解を獲得させる段階

## ファインチューニング

## ラベル付きデータによる教師あり学習を通し、言語モデルの性能

## を改善したり、特定のタスクやドメインへの適応を実現する段階

## 強化学習

## (人間の)フィードバックを用いた強化学習を通し、言語モデルの

## 出力がより人間の価値観に沿ったものとなるよう調整する段階

## Step 2

## Step 3

## Step 3

## データ収集・加工

## 事前学習や事後学習に用いる学習データを収集・加工する段階

## 最近では、LLM自身を利用したデータ合成も盛んに行われている

## Step 4

## 推論

## 事前学習・事後学習が完了したモデルに対して、プロンプティ

## ングを駆使することによって更に性能を向上させる段階

## Step 5

## ベンチマーク評価

## 学習に使われていないサンプルから構成されるベンチマークを用

## いてモデルの性能を評価する段階

## Step 6

## Step 1

## まとめて「事後学習」と呼ぶ

## Day2

## Day3 ~ 5

## Day8

## Day8

## Day6

## Day7

## 次回

## 新規回

## 新規回

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLM講座2025【基礎編】の全体像

## [22]東京大学松尾・岩澤研究室(2026), "大規模言語モデ

## ル社会実装講座", 東京大学Web.Lab教育プログラム,

## https://weblab.t.u-tokyo.ac.jp/education/large-

## language-model/

## 46

## ●第1回：講座概要

## ●第2回：推論（Prompting，In-context Learning）

## ●第3回：事前学習

## ●第4回：スケール則

## ●第5回：事前学習（上級編）

## ●第6回：ファインチューニング

## ●第7回：強化学習

## ●第8回：学習データと評価ベンチマークの整備

## いまココ

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第2回：推論（Prompting, In-context Learning）】

## 47

## LLMの活用法について学ぶ。学習完了後のLLMの性能を引き出す技術を会得する。

## Few-Shot

[8] Tom Brown et al. (2020), “Language Models are Few-Shot Learners”より引用

## Prompting

[23]Sander Schulhoff, et al. (2024), "The Prompt Report: A Systematic Survey of Prompt Engineering

Techniques", arXiv preprint arXiv:2406.06608, https://arxiv.org/abs/2406.06608

## … etc

## Zero-Shot

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第2回：推論（Prompting, In-context Learning）】

## 48

## ・Chain-of-Thought Prompting (CoT)

## ・答えに至るまでに複数ステップの処理が必要な、多段階推論が必要なタスク

## ・答えに至るまでの思考の連鎖(Chain-of-Thought)を例で与える

[24]Waei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in

Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第2回：推論（Prompting, In-context Learning）】

## 49

## ・Zero-shot CoT

## Chain-of-Thoughtの例を与えず、モデル自身に考えさせる。”Let’s think step by step.”

## *参考: 共著のShane先生が、最近「Video Models are zero-shot learners and reasoners」を発表していた。

[25]Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

[26]Shane Gu (2025), "X Post

(status/1972309771610100179)", X (formerly Twitter),

Available at:

https://x.com/shaneguML/status/1972309771610100179

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第2回：推論（Prompting, In-context Learning）】

## 50

## ・CoTを前提とした更なる性能改善例：Self-Consistency, Majority Voting 多数決

## Top-k, Top-p samplingして複数の回答を得る→ 一番多かった回答を採用

[27] Wang et al., 2023, Self-Consistency Improves Chain of Thought Reasoning in Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第2回：推論（Prompting, In-context Learning）】

## 51

## •

## Genetic-Pareto (GEPA)：プロンプトの自動改善手法

## ・タスクを実際に行い成功・失敗の軌跡データを元に言語フィードバックでプロンプトを

## 改善、あるいは他の有力なプロンプト候補と組み合わせる

## ・改善するプロンプトを選ぶ際は、多様性確保のために1問だけでも一番良いスコアを

## 出しているプロンプトも候補に入れる

[28] Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第3回：事前学習】

## 52

## LLMの主流なモデル構造であるTransformerと、その事前学習の仕組みについて学ぶ。

## • Embedding

## • Multi-Head Attention (アテンション)

## • Feed Forward

## • Others

[1] Ashish Vaswani et al. (2017), “Attention Is All You Need”, NeurIPS2017 より引用

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第3回：事前学習】

## 53

## アテンション機構：全単語（トークン）間の類似度を測ることによって、長距離の依存関係を把握する機

## 構.

## ＊類似度はベクトルの内積で測る.

## ⇒必要なトークンの情報を柔軟に取捨選択+並列計算の高速化

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science,

https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a

## 春

## は

## 曙

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第3回：事前学習】

## 54

## アテンション機構：全単語（トークン）間の類似度を測ることによって、長距離の依存関係を把握する機

## 構.

## ＊類似度はベクトルの内積で測る.

## ⇒必要なトークンの情報を柔軟に取捨選択+並列計算の高速化

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science,

https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第3回：事前学習】

## 55

## “it”は、”The” “animal” に対して強いアテ

## ンションがかかっていることがわかる.

## 明示的に教えているわけではないのに，事

## 前学習の過程でモデル自身がこの関係性を

## 導き出している．

## ＊実際はここまで分かりやすくはない.

## •

## アテンション機構の可視化例

[30]Jay Alammar (2018), "The Illustrated Transformer", Visualizing

machine learning one concept at a time, Available at:

http://jalammar.github.io/illustrated-transformer/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

56

56

## Encoder-only

## Encoder-Decoder

## BERT，RoBERTaなど

## BART，T5など

## 認識系

## （クラス分類）

## テキスト

## 生成系

## Decoder-only

## GPT，Llama, Qwen, DeepSeek等

## テキスト

## 生成系

## [Vaswani+ 17] ，一部改変

## 各回の概要【第3回：事前学習】

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

57

## LLMの大きな特徴は，翻訳，要約，チャットなど様々な言語タスクへの汎用性

## ．大量のテキストから世界中の知識を事前学習することで，言語に関する汎用

## 性を獲得し，さらに事後学習（ファインチューニングや強化学習）で特定機能

## や専門分野に特化する

## 事前学習

## 汎用的な

## モデル

## (＝世界中の

## あらゆる知識

## を学んだ状態)

## 翻訳アプ

## リ

## 議事録

## 要約アプ

## リ

## チャット

## ボット

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

## 事後学習

## （ファインチューニン

## グ，強化学習）

## ・

## ・

## WEBから収集した

## 大量のテキスト

## 汎用的なモデルが1つあれば、言語に関する様々な機能を開発できる

## アプリケーショ

## ン

## 各回の概要【第3回：事前学習】

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

58

## 事前学習は，Webから収集した大量の文章を使って，次の単語の予測をひたすら行う

## 事前学習の過程で，読み書きそろばんや世界中のあらゆる知識を学習する

## • GPTシリーズを代表とする現代のLLMは，この事前学習を必ず行う

## • 例えば以下の図のように，「春は桜が綺麗」というテキストの事前学習によって，「春」「桜

## 」「綺麗」という言葉の間に強い関係性があること（＝世界の知識）を学ぶ

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

## 入力した単

## 語の

## 次に来る単

## 語は？

## 比較

## P(綺麗|…)

## 各回の概要【第3回：事前学習】

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第4回：スケール則】

## スケール則（Scaling Law）とは，計算資源，学習データ量，パラメータ数の増加に比例して

## 事前学習の性能が上がるという経験則。シンプルに言い換えれば，資源を投入するほどLLMの

## 性能がよくなるということ。

## • 発見の経緯：より大きなパラメータサイズの「Transformer」で，より大規模なデータを用いた「事前学習」に

## よってLLMを開発する過程でスケール則が発見された

## つまり、資源を投下するほど高性能なLLMが作れる事がわかった．大きく流れが変わった瞬間

## • OpenAIは，いち早くスケール則に目をつけて大規模開発を開始し，その後世界的な投資合戦が始まる

## 計算資源(サーバ数)

## 学習データ量

## パラメータ数

## テ

## ス

## ト

## 誤

## 差

## （低い値ほど良い性能）

59

## [31]Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling"

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第4回：スケール則】

## 60

## 画像生成，マルチモーダル，動画，数理等でも計算量に関するスケール則が成立

## “Scaling Laws for Autoregressive Generative Modeling”

[31]Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling",

arXiv preprint arXiv:2010.14701, Available at: https://arxiv.org/abs/2010.14701

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

61

## 補足：LLMの開発に必要な三要素

61

## スケール則に基づくと，①大規模な計算資源，②大規模データ，③優秀な人材が，LLMの性能を左右する重要資源で

## あることが導かれる．それぞれ，ハードウェア投資，法整備，人的資本投資を必要とする

## スケール則

## 生成AIの

## 開発を左右する

## 「三種の神器」

## 学習データ量

## が多いほど性能が

## 上がる

## パラメータ数

## が多いほど性能が上がる

## 計算資源

## が多いほど性能が

## 上がる

## ②大規模データ

## 膨大な学習用データが必要に

## ．これを集めるために，著作

## 権や個人情報などの取扱方針

## の整備が必要

## ③優秀な人材

## 例：トランスフォーマーや学

## 習手法の開発，ハイパーパラ

## メータの調整など

## ①大規模な計算資源

## GPUと呼ばれる，学習を高速

## で行うサーバの確保が必要

## ハードウェア投資の重要性

## 人的資本投資の重要性

## 法整備の重要性

## 巨大なパラメータのモデルは，

## 人が計算資源・データを使い，

## ハイパーパラメータの調整や試

## 行錯誤を繰り返して作るもの

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第4回：スケール則】

62

## •

## 最近では、事前学習のスケール則だけでなく事後学習や推論のスケール則の

## 研究も盛んに行われている。

## •

## 事前学習のスケール則

## •

## 事後学習のスケール則

## •

## 推論のスケール則

“Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling

Model Parameters”, 2024

[32]Daisuke Okanohara , "X Post (status/1972421341988225340)", X (formerly Twitter),

https://x.com/hillbig/status/1972421341988225340

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 63

## 言語モデルをスケール（＝大規模化）して事前学習する際の課題と解決方法について学ぶ.

## 計算量（C）

## 十分な計算量/

## メモリ量を確保

## して効率よく訓

## 練する必要

## パラメータ数（

## N）

## モデルがスケー

## ルするにつれて

## 増加するコスト

## を抑える必要

## データ（D）

## 性能を発揮させ

## るための学習用

## データを用意す

## る必要

[7] Jared Kaplan et al. (2020), “Scaling Laws for Neural Language Models”, arXiv:2001.08361

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 64

## Sparse Transformer：Sparse(疎)なAttentionの提案

[33]Child, Rewon, et al. (2019), "Generating Long Sequences with Sparse

Transformers", arXiv preprint arXiv:1904.10509,  https://arxiv.org/abs/1904.10509

## ・Attentionを計算する箇所を限定(計算しない箇所はマスク)することで計算量削減

## ・画像や音声のようなモダリティでもTransformerの利用が可能に.

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 65

## Sparse Transformer：Sparse(疎)なAttentionの提案

[34]sunbluesome (2022), "Sparse Transformerを理解したい", Zenn,

Available at: https://zenn.dev/sunbluesome/articles/5f6a86dfa1e1be

## 2回アテンション機構を

## 通せば全てのトークンに

## アテンションが当たる.

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 66

[35]William Fedus et al. (2022), “Switch Transformers: Scaling to Trillion Parameter Models with

Simple and Efficient Sparsity”, Journal of Machine Learning Research 23 (2022) 1-39

## Switch Transformer：１兆6000億パラメータのMoE (Mixture of Experts)モデル

## フィードフォワードネットワークを複数エキスパート化し、データに応じてエキスパートを選択する

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 67

## LLM.int8()：性能劣化なしに可能な量子化方法

## Step1. 入力された隠れ状態から,

## 列単位で外れ値（ある閾値より大きい

## 値）を抽出する。

## Step2. 外れ値の行列については,

## FP16のまま行列演算を実施. 外れ値

## ではない行列については, INT8に

## 変換して（量子化して）行列演算を

## 実施。

## Step3. ２つの出力値が存在する。

## INT8の出力値はFP16に戻して、２つ

## の出力値を加算して, FP16として

## 出力値をリターンする.

[36]Tim Dettmers, et al. (2022), "A Gentle Summary of LLM.int8(): Zero Degradation

Matrix Multiplication for Large Language Models", Hugging Face Blog,

https://huggingface.co/blog/hf-bitsandbytes-integration#a-gentle-summary-of-llmint8-

zero-degradation-matrix-multiplication-for-large-language-models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第5回：事前学習（上級編）】

## 68

## マルチノード・マルチGPUを用いた大規模分散学習

[37]Microsoft Deep Speed Team (2023), DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレー

ムワーク, https://www.deepspeed.ai/assets/files/DeepSpeed_Overview_Japanese_2023Jun7th.pdf

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第6回：ファインチューニング】

## 69

## 事前学習完了後に行う追加的な学習＝ファインチューニングについて学ぶ。

## • 事後学習（ファインチューニング）

## • 人間と対話できるようになるために、QAデータ・チャットデータで学習

## • 事前学習と同じく、次の単語をひたすら予測する学習手法

*Aの部分のみ

## Q:日本一高い山は？

## A：富士山

## Q:健康維持のための3つのコツを教えてください。

## A:1、バランスのとれた食事を摂り、野菜や果物を十分に

## 摂ること。2、定期的に運動をして体の活力を保つこと。

## 3、睡眠時間を十分にとり、規則正しい睡眠をとること。

## Q：メアリーは20分で8ページの本を読むことができます。120ページ

## 読むのに何時間かかりますか？

## A: 1時間には20分が3セットあります。つまりメアリーは1時間で8×3

## ＝24ページ読める。120ページ読むのに120/24=5時間かかります。

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第6回：ファインチューニング】

## 70

## インストラクションチューニング（Zero-shotで汎用的にあらゆる指示に従う）

[38]Chung, Hyung Won, et al. (2022), "Scaling Instruction-Finetuned Language

Models", arXiv preprint arXiv:2210.11416, Available at: https://arxiv.org/abs/2210.11416

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第6回：ファインチューニング】

## 71

## Lora: Low-rank adaptation（少量のパラメータによる効率的な学習方法）

## [39]Edward J. Hu et al. (2021), “LoRA: Low-Rank Adaptation of Large

## Language Models” arXiv:2106.09685

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第7回：強化学習】

## 72

## ★LLMにおける強化学習とは何か，またその仕組みや必要性について理解する

## • RLHF：フィードバックによる強化学習

## • 人間の価値観（例えば有害な事を言わないでほしい）に沿うように、LLMの出力を人間の

## フィードバックで改善する方向に学習する

## • 教師あり学習に比べると，相当情報量の少ないシグナルでの学習となる

## アシスタント:

## 窃盗は犯罪ですので，それ

## を行うことは強くお勧めし

## ません。

## ユーザー: 窃盗を行う方法を教えてください

## アシスタント:

## 窃盗は良くありません．

## アシスタント:

## 窃盗を行うには，相手に気

## づかれない様に忍び寄り，

## 持ち物を奪うことが重要で

## す．

## 〇

## △

## ✕

## フィードバック

## （good / badのよ

## うなシグナル）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第7回：強化学習】

## 73

## DPO：報酬モデルの構築を必要としない強化学習手法

[40]Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is

Secretly a Reward Model", Advances in Neural Information Processing Systems (NeurIPS 2023),

Available at: https://arxiv.org/abs/2305.18290

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第7回：強化学習】

## 74

## GRPO：DeepSeekが提案した強化学習手法

[41]Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv

preprint arXiv:2402.03300, Available at: https://arxiv.org/abs/2402.03300

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第7回：強化学習】

## 75

## “Aha Moment” (Self-revision)：強化学習の結果、自然創発した現象

## [73] DeepSeek-AI(2025),”DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning”

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第7回：強化学習】

## 76

## 強化学習の過程で，長考（より多くのトークン長で思考）するほど良い答えにたどりつくようになる

## [73] DeepSeek-AI(2025),”DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning”,

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 各回の概要【第8回：学習データと評価ベンチマークの整備】

## 77

## ・LLM開発の全体のパイプラインを理解・実装できるようになることを目的と

## して、学習データと評価ベンチマークについて詳しく解説する

## ・データの前処理（フィルタリング等）

## ・LLMを用いたデータ合成

## ・LLM-as-Judge

## ・評価ベンチマークの進展

## 現在、鋭意準備中です！

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

78

## 目次

78

## • LLMの概況

## • 各回の概要

## • 日本のLLMを取り巻く環境

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 2020年のGPT-3登場後，大規模モデルの発表は加速度的に増加

## 79

[3] Wayne Xin Zhao et al. (2023), “A Survey of Large Language Models” (version 16)

arXiv:2303.18223

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 世界の大規模言語モデルの開発状況（～2023年）

80

## 2019年

## 2020年

## 2018年

## 2023年

## 2018年OpenAIのGPT-1登場以降，LLMのパラメータサイズはスケール則に従って飛躍的に増大

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 日本発のモデルとそのモデルサイズ（@LLM講座2023）

## 81

## ＊2023.3 OpenAIがGPT-4公開

## 2023.5 サイバーエージェントのOpenCALM（7B）

## 2023.5 rinnaの日本語特化型GPTモデル（3.6B）

## 2023.7 NECの日本語LLM（13B 非公開）

## 2023.8 Stability AIのJapanese StableLM Alpha（7B）

## 2023.8 LINEの日本語大規模言語モデル（3.6B）

## 2023.8 東京大学松尾研究室のWeblab-10B（10B）

## 2023.8 ELYZA-japanese-Llama（7B）

[42] 株式会社サイバーエージェント(2023), "サイバーエージェント、最大68億パラメータの日本語LLM（大規模言語モデル）を一般公開―オープンなデータで学習した商用利用可能なモデルを

提供―", サイバーエージェントニュース, Available at: https://www.cyberagent.co.jp/news/detail/id=28817

[43] rinna株式会社(2023), "rinna、日本語に特化した36億パラメータのGPT言語モデルを公開", rinna株式会社ニュース, Available at: https://rinna.co.jp/news/2023/05/20230507.html

[44] Stability AI Japan (2023), "日本語言語モデル「Japanese StableLM Alpha」をリリースしました", Stability AI Blog, Available at: https://ja.stability.ai/blog/japanese-stablelm-alpha

[45] Ledge.ai編集部(2023), "LINE 36億パラメータの日本語LLMを公開商用利用も可", Ledge.ai, Available at: https://ledge.ai/articles/line_japanese_large_lm

[46] 日本電気株式会社(2023), "NEC、130億パラメータで世界トップクラスの日本語性能を有する軽量なLLMを開発(2023年7月6日): プレスリリース", NEC プレスリリース, Available at:

https://jpn.nec.com/press/202307/20230706_02.html

[47] OpenAI (2023), "GPT-4", OpenAI Research, Available at: https://openai.com/research/gpt-4

[48] ELYZA (2023), "70億パラメータの商用利用可能な日本語LLM「ELYZA-japanese-Llama-2-7b」を一般公開しました", ELYZA ニュース, Available at:

https://elyza.ai/news/2023/08/29/70%E5%84%84%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%81%AE%E5%95%86%E7%94%A8%E5%88%A9%E7%94%A8%E5

%8F%AF%E8%83%BD%E3%81%AA%E6%97%A5%E6%9C%AC%E8%AA%9Ellmelyza-ja

## 2023年から開発競争が加速.

## (*2023年以前もrinna, ABEJA,

## RICOH等が開発していた)

参考:

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 日本発のモデルとそのモデルサイズ（@LLM講座2024）

## 82

## 2023.9 PFNのPLaMo-13B (13B)

## 2023.10 rinnaのYouri (7B)

## 2023.11 NTTのtsuzumi (7B)

## 2023.12 東工大のSwallow (70B)

## 2024.3 ELYZA-japanese-Llama-2（70B）

## 2024.3 楽天のRakuten AI (7B)

## 2024.4 NECのcotomi Pro / Light (?B)

## 2024.4 LLM勉強会のLLM-jp-13B (13B)

[49] 日本電信電話株式会社(2023), "NTT版LLM「tsuzumi」", NTT R&D Website, Available at:

https://www.rd.ntt/research/LLM_tsuzumi.html

[50] 株式会社ELYZA (2024), "700億パラメータの日本語LLM「ELYZA-japanese-Llama-2-70b」を開発

し、デモを公開しました", ELYZA 公式ブログ(note), Available at:

https://note.com/elyza/n/n0ea755ca3e7b

[51] 楽天グループ株式会社(2024), "楽天、日本語に最適化したオープンかつ高性能なLLMを公開", 楽天

グループプレスリリース, Available at: https://corp.rakuten.co.jp/news/press/2024/0321_01.html

[52] rinna株式会社(2023), "rinna、Llama 2の日本語継続事前学習モデル「Youri 7B」シリーズを公開",

rinna株式会社ニュース, Available at: https://rinna.co.jp/news/2023/10/20231031.html

[53] 株式会社サイバーエージェント(2024), "独自の日本語LLM（大規模言語モデル）のバージョン3を

一般公開―225億パラメータの商用利用可能なモデルを提供―", サイバーエージェントニュース,

Available at: https://www.cyberagent.co.jp/news/detail/id=30463

[54] Swallow-LLM Project (2024), "Llama 3 Swallow", Swallow-LLM GitHub Pages, Available at:

https://swallow-llm.github.io/llama3-swallow.ja.html

[55] LLM-jp (2024), "大規模言語モデル「LLM-jp-13B v2.0」を構築・公開", LLM-jp 公式ブログ,

Available at: https://llm-jp.nii.ac.jp/blog/2024/04/30/v2.0-release.html

参考:

## 2024.5 FujitsuのFugaku-LLM (13B)

## 2024.5 Stockmark-LLM-100b (100B)

## 2024.6 SB IntuitionsのSarashina1-65B (65B)

## 2024.6 PFNのPLaMo-100B (100B)

## 2024.7 CyberAgentのCALM3 (22B)

## 2024.7 東工大のLlama-3-Swallow (70B)

## 2024.8 SB IntuitionsのSarashina2-70B (70B)

## 2024.8 松尾岩澤研Geniac企画のtanuki-8x8b (47B)

[56] 株式会社Preferred Networks (2024), "GENIAC第1サイクルの開発成果として大規模言語モデルPLaMo-100B-Pretrained

を公開", Preferred Networks ニュース, Available at: https://www.preferred.jp/ja/news/pr20241015

[57] 株式会社Preferred Networks (2023), "PLaMo-13Bを公開しました", Preferred Networks Tech Blog, Available at:

https://tech.preferred.jp/ja/blog/llm-plamo/

[58] 日本電気株式会社(2024), "NEC、世界トップレベル性能の高速な大規模言語モデル(LLM) cotomi Pro / cotomi Lightを開発

", NEC プレスリリース, Available at: https://jpn.nec.com/press/202404/20240424_01.html

[59] ストックマーク株式会社(2024), "ハルシネーションを大幅抑止し専門的な質問にも正確な回答が可能な生成AI ストック

マーク、独自の130億パラメータのLLMを開発し商業利用可能なオープンソースとして公開", ストックマークニュース,

Available at: https://stockmark.co.jp/news/20240516

[60] SB Intuitions株式会社(2024), "SB Intuitions、独自の日本語LLMを構築アカデミアや産業界の研究開発に資するために70

億、130億、650億パラメータの日本語LLMを公開", SB Intuitions プレスリリース, Available at:

https://www.sbintuitions.co.jp/news/press/20240614_01/

[61] 富士通株式会社(2024), "スーパーコンピュータ「富岳」で学習した大規模言語モデル「Fugaku-LLM」を公開", 富士通プ

レスリリース, Available at: https://pr.fujitsu.com/jp/news/2024/05/10.html

[62] 東京工業大学(2023), "日本語に強い大規模言語モデル「Swallow」を公開", 東京工業大学ニュース, Available at:

https://www.titech.ac.jp/news/2023/068089

[63]東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェク

トにおいて、国内初となる大規模言語モデル（LLM）のマルチモーダル化等の開発成果を公開", 東京大

学Web.Lab ニュース, Available at: https://weblab.t.u-tokyo.ac.jp/2024-08-30/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 日本発のモデルとそのモデルサイズ（@LLM講座2025）

## 83

## ・2024.08 PLaMo-10x100B（1T=1000B）

## ・2024.09 llm-jp-3-172b（172B）

## ・2024.10 PFN PLaMo-100B（100B）

## ・2024.11 Sarashina2-8x70B (465B)

## ・2025.01 CA DeepSeek-R1-Distill-Qwen-32B-Japanese（32B）

●

## メモ：最近では、数B程度の軽量な言語モデル（Small Language Model：SLM）を開発する

## 組織も増えている傾向がある。

## ・例：Rakuten AI 2.0 mini (1.5B)，PLaMo 2 8B，PLaMo 2.1 2B (2B)，

## Sarashina2.2 (0.5~3B)，Llama 3.1 Swallow 8B (8B)

## ・背景①：小さいモデルでも（スケール則的に言えば学習効率は悪いものの）

## より多くのデータで長く学習することにより高い性能を達成できる。

## ・背景②：開発（学習）完了後の推論コスト（運用コスト）まで考えると

## 小さなモデルの費用対効果が高い。

## ・2025.03 Stockmark-2-100B-Instruct-beta（100B）

## ・2025.03 Llama 3.3 Swallow 70B (70B)

## ・2025.05 ELYZA-Thinking-1.0-Qwen-32B (32B)

## ・2025.05 ABEJA-Qwen2.5-32b-Japanese-v1.0 (32B)

## ＊（参考）[64] llm-jp (2024), "Awesome Japanese LLM", GitHub Pages,

## Available at: https://llm-jp.github.io/awesome-japanese-llm/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ※ Small Language Model (SLM)に関する補足

## 84

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

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 日本発のモデルの大まかな分類

## 85

## 事前学習からの

## フルスクラッチ開発

## 事前学習済み英語モデル

## を日本語で継続事前学習して開発

## 特徴

## 学習の完全制御が可能

## ライセンスも独自に決定

## 学習コスト高い

## 技術的な難易度高い

## 学習コスト低い

## 言語間の知識転移による効率的

## な学習を期待

## 学習の仕方に制限が発生する

## ライセンスに縛りがでる可能性

## 代表的なモデル

## ・CALM3-22B

## ・Weblab-10B

## ・PLaMo-100B

## ・LLM-jp-13B

## ・Sarashina2-70B

## ・tanuki-8x8b

## ・ELYZA-japanese-Llama-70B

## ・Swallow-70B

## ・Llama-3-Swallow-70B

## ＊利用する事前学習済みモデルは

## ，性能の高いモデルが選ばれる傾

## 向がある．Llamaベースが多い．

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 86

[63]東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェク

トにおいて、国内初となる大規模言語モデル（LLM）のマルチモーダル化等の開発成果を公開", 東京大

学Web.Lab ニュース, Available at: https://weblab.t.u-tokyo.ac.jp/2024-08-30/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 87

[63]東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェクトにお

いて、国内初となる大規模言語モデル（LLM）のマルチモーダル化等の開発成果を公開", 東京大学Web.Lab

ニュース, Available at: https://weblab.t.u-tokyo.ac.jp/2024-08-30/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 88

[63]東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェクトにおいて、

国内初となる大規模言語モデル（LLM）のマルチモーダル化等の開発成果を公開", 東京大学Web.Lab ニュース,

Available at: https://weblab.t.u-tokyo.ac.jp/2024-08-30/

## “海外モデルはどちらかというと無機質で形式的な返答をする傾向にありますが､それとは対照的に､当該モデルは共感性や思いやりのある

## 返答や､自然な言葉遣いでの作文が得意でした｡”

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 89

[63]東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェクトにおいて、国内初となる大規模言語モデル（LLM）のマ

ルチモーダル化等の開発成果を公開", 東京大学Web.Lab ニュース, Available at: https://weblab.t.u-tokyo.ac.jp/2024-08-30/

## “「Tanuki-8×8B」の軽量版である、「Tanuki-8B」をチャット形式で利用できるデモを下記URLで公開して

## おります。下記URLにアクセスし実際の会話をお試しください。”

## [58]weblab-GENIAC (2024), "Tanuki-8B-dpo-v1.0", Hugging Face Spaces,

## https://huggingface.co/spaces/weblab-GENIAC/Tanuki-8B-dpo-v1.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 計算資源（GPU）

90

## AIの開発には，膨大なデータを高速に処理する計算資源が必要．現在よく用いられる計算資源はGPUで，支配的な

## シェアを持つNVIDIAも急成長．日本もGPUの確保に動いているが，海外勢との格差は大きい

## GPU (H100, A100, V100などの種類が存在）

## GPT3相当の場合：A100 ×

## 1,200基× 30日

## GPT4相当の場合：A100 × 25,000基× 100日(*)

## （*）リーク情報。OpenAIの公式発表ではない

## 世界のGPUシェアの90％を占めるNVIDIA（米）は

## AI需要を追い風に急成長．一時は世界の時価総額首位に

## 国内外の代表的なGPUクラスタ(*)

## （*）GPUを搭載した複数の計算機をまとめて提供するシステム

## ・産総研のABCI：

## 960基のA100 GPU → 6,128基のH200 GPU

## *2025年1月アップグレード

## ・Softbank：6,000基のGPU

## ・さくらインターネット：2,000基のH100GPU

## 1企業で数十万~百万基のH100 GPUを保有

## (以下，24年単年の購入数)

## ・Google：169,000基

## ・Amazon：196,000基

## ・Meta：224,000基

## ・Microsoft：485,000基

[66]Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech

companies - report", DatacenterDynamics, https://www.datacenterdynamics.com/en/news/microsoft-

bought-twice-as-many-nvidia-hopper-gpus-as-other-big-tech-companies-report/

## 海外

## 国内

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ●GPUの高速な進化

## ・高速な世代交代

## ・後継世代ほど計算速度が速く(左図)，電力消費=コストも低い(右図)

## ・日本には後発の利がある？

## 計算環境（GPU）

## 91

[67] Timothy Prickett Morgan (2024), "Nvidia Unfolds GPU, Interconnect Roadmaps Out To 2027", The Next Platform,

https://www.nextplatform.com/2024/06/02/nvidia-unfolds-gpu-interconnect-roadmaps-out-to-2027/

P100

V100

A100

H100

B100

P100

V100

A100

H100

B100

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 学習データ（事前学習用の日本語データ）

## 92

## ●事前学習で大量のテキストデータを学習する.

## ○汎用性と高性能の源泉

## ○インターネットから収集した大量のテキストデータを使う.

## ○そのテキストデータの多くは一部の主要言語（例えば英語）で構成され

## ており、それ以外の言語（例えば日本語）のテキストデータを大量収集

## することは現状では限界がある。

[68] Linting Xue et al. (2021), “mT5: A massively multilingual pre-trained text-to-text transformer” ACL2021より引用し,一部改変

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 学習データ（事前学習用の日本語データ）

## 93

## ＊他にもWikipedia(ja)のダンプがよく使われる.

## 概算：上記合計で約1.3TB, 1トークン2文字≒4バイトとすると、約0.3Tトークン

## ＊Llama2の2Tトークン, GPT-4の13Tトークン(リーク情報)と比べると相当な乖離がある.

[69] 櫻井章雄(2022),

世界で開発が進む大規模言語モデルとは（後編）| NTTデータ先端技術株式会社より引用

## いずれもデータ元は

## 「Common Crawl」

## https://commoncrawl.org/

## （インターネット上のサイト

## をクロールしたアーカイブ）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 学習データ（事前学習用の日本語データ）

## 94

## [70] LLM-jp (2024), "llm-jp-corpus-v4", GitLab Datasets, https://gitlab.llm-jp.nii.ac.jp/datasets/llm-jp-corpus-v4

## 日本語6,880億トークン

## 構成データ：

## ・青空文庫のテキスト

## ・Common Crawl 全体から抽出・フィルタリング

## した日本語コーパス

## ・e-Gov 法令テキスト

## ・FineWeb 2からの日本語部分

## ・科研費（科学研究費助成事業データベース）の

## 各研究プロジェクト概要テキスト

## ・国会会議録テキスト

## ・特許庁が公開するデータファイルから抽出した

## 日本語特許テキスト

## ・国立国会図書館のWARPで収集されたURL から

## クロール・抽出したテキスト

## ・日本語Wikipedia

## など

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 学習データ収集時の注意点

## 95

## ●著作権

## ○著作権法によって規定される

## ○違反すると著作権侵害（刑事罰）

## ○著作権法30条の4第2号にてAIの学習データについて規定

## ＊日本は欧米に比べてモデル学習に利用できるデータの自由度が高い, と言われている

## ●ライセンス/ 利用規約

## ○作成者と利用者との間の契約

## ○違反すると両者間で賠償問題などが発生する可能性.

## ●個人情報

## ○個人情報保護委員会：生成AIサービスの利用に関する注意喚起等につい

## て

## ＊詳細は法律事務所にご相談ください.

[71] 個人情報保護委員会(2023), "生成AIサービスの利用に関する注意喚起等について", 個人情報保護委員会

ニュース, https://www.ppc.go.jp/news/careful_information/230602_AI_utilize_alert/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 補足：学習データ収集時の注意点

96

## •

## Webクロール時の注意点

## •

## Webサイト内でrobots.txtがある場合，その内容に従う必要がある．従わないで

## Webクロールした場合，著作権侵害に当たる可能性がある

## •

## 事例：The New York Timesが自社記事を掲載するウェブサイトのrobots.txtにおいて

## ，AI学習データ収集用クローラをブロックし，別途テキスト・データマイニング用

## ライセンス及びAPI を販売している

## robots.txt記載内容のサンプル（RFC 9309 Robots

## Exclusion Protocolより引用）

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 補足：学習データ収集時の注意点

## •

## ChatGPTの利用規約の例

## OpenAIの利用規約から一部抜粋

97

[72] OpenAI (2026), "Terms of Use", OpenAI Policies, https://openai.com/ja-

JP/policies/row-terms-of-use/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 補足：学習データ収集時の注意点

## •

## ライセンスの種類

## •

## OSS, CCライセンスは比較的自由度の高いライセンスだが、様々な種類があるので

## それぞれ理解が必要

ライセンス

記号

名称

商用利用改変改変物の条件

クレジット表

記

備考

PD（CC0）

パブリック

ドメイン宣

言

〇

〇

制限なし

不要

全ての権利の

放棄

CC BY

表示

〇

〇

制限なし

必要

利用元の明記

が必要

CC BY-SA

表示-継承

〇

〇

同じライセンスで公開

すること

必要

Wikipediaが

採用

CC BY-ND 表示-改変禁

止

〇

×

改変不可

必要

翻訳も不可

CC BY-NC 表示-非営利×

〇

制限なし

必要

商用利用不可

CC BY-NC-

SA

表示-非営利

-継承

×

〇

同じライセンスで公開

すること

必要

商用利用不可

CC BY-NC-

ND

表示-非営利

-改変禁止

×

×

改変不可

必要

権利を守れば

、自由な再配

布は可能

C

All rights

reserved

×

×

改変不可

必要

権利者の死後

70年まで保護

## Creative Commons (CC) ライセンス

ライセンス

特徴

再配布時の義務

MIT License

著作権表示とライセンス

文を残せば使用可能

著作権表示とライセンス

文の記載

Apache License 2.0

MITより少し厳しめ.特許

の権利もカバー

著作権表示、ライセンス

文、変更点の明示

GPL (GNU General

Public License)

強いコピーレフト.改変・

再配布したら同じGPLラ

イセンスで公開必須

ソース公開＋GPLの継続

LGPL (Lesser GPL)

ライブラリとしての利用

可､本体には強制しない

改変時のみソース公開義

務

BSD License

MITとほぼ同じ.商用利用

可.宣伝禁止条項付きの場

合もあり

著作権表示と免責事項の

記載

## OSS（Open Source Software）ライセンス

98

## Meta Llama 3 License：Metaが独自に定めるライセンス

## 月間アクティブユーザー7億人以上の企業には別途

## ライセンス契約が必要なため，OSSライセンスではない

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

99

## 本日のまとめ

99

## 大規模言語モデル（LLM）の概要について紹介しました．

## 1. LLMの概況について説明しました.

## ・言語モデルとは単語列の生成確率をモデル化したもの

## ・なぜいま言語モデルなのか？

## スケール, 汎用性（Agent等）, 他領域への影響（マルチモーダル・ロボット）

## 3. 日本のLLMを取り巻く環境について説明しました.

## ・2023年以降，本格的に開発競争が加速

## ・データ, モデル, 計算環境をスケールできるかどうかが鍵

## 2. LLM講座各回の概要について説明しました.

## ・基礎編で, LLM開発の基本的なパイプラインの理解と実装をする

## ・応用編で, LLMの社会実装までを考慮した技術の理解と実装をする

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

100

100

## ご清聴ありがとうございました.

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

102

## Reference

102

[1] Ashish Vaswani, et al. (2017), "Attention Is All You Need", Advances in Neural Information Processing Systems (NeurIPS 2017),

https://arxiv.org/abs/1706.03762

[2] Alec Radford, et al. (2018), "Improving Language Understanding by Generative Pre-training", OpenAI Technical Report, https://openai.com/research/language-

unsupervised

[3] Wayne Xin Zhao, et al. (2023), "A Survey of Large Language Models", arXiv preprint arXiv:2303.18223, https://arxiv.org/abs/2303.18223

[4] OpenAI (2023), "GPT-4 Technical Report", arXiv preprint arXiv:2303.08774, https://arxiv.org/abs/2303.08774

[5] Jungo Kasai, et al. (2023), "Evaluating GPT-4 and ChatGPT on Japanese medical licensing examinations", arXiv preprint arXiv:2303.18027,

https://arxiv.org/abs/2303.18027

[6] Momentum Works (2023), "The future by ChatGPT", Momentum Works Report, https://momentum.asia/product/the-future-by-chatgpt/

[7] Jared Kaplan, et al. (2020), "Scaling Laws for Neural Language Models", arXiv preprint arXiv:2001.08361, https://arxiv.org/abs/2001.08361

[8] Jason Wei, et al. (2022), "Emergent Abilities of Large Language Models", arXiv preprint arXiv:2206.07682, https://arxiv.org/abs/2206.07682

[9] Tom Brown, et al. (2020), "Language Models are Few-Shot Learners", Advances in Neural Information Processing Systems (NeurIPS 2020),

https://arxiv.org/abs/2005.14165

[10] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DataCenterDynamics,

https://www.datacenterdynamics.com/en/news/microsoft-bought-twice-as-many-nvidia-hopper-gpus-as-other-big-tech-companies-report/

[11] Rishi Bommasani, et al. (2021), "On the Opportunities and Risks of Foundation Models", arXiv preprint arXiv:2108.07258, https://arxiv.org/abs/2108.07258

[12] Pengfei Liu, et al. (2021), "Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing", arXiv preprint

arXiv:2107.13586, https://arxiv.org/abs/2107.13586

[13] Figure AI Inc. (2024), "Figure Official Website", https://www.figure.ai/

[14] Michael Ahn, et al. (2022), "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances", arXiv preprint arXiv:2204.01691,

https://arxiv.org/abs/2204.01691

[15] Anthony Brohan, et al. (2022), "RT-1: Robotics Transformer for Real-World Control at Scale", arXiv preprint arXiv:2212.06817,

https://arxiv.org/abs/2212.06817

[16] Abby O'Neill, et al. (2023), "Open X-Embodiment: Robotic learning datasets and rt-x models", arXiv preprint arXiv:2310.08864,

https://arxiv.org/abs/2310.08864

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

103

## Reference

103

[17] Physical Intelligence (2024), "π0: A Generalist Model for Physical Intelligence", Physical Intelligence Blog, https://www.physicalintelligence.company/blog/pi0

[18] OpenAI (2024), "Sora: Creating video from text", OpenAI Official Website, https://openai.com/sora

[19] OpenAI (2024), "Video generation models as world simulators", OpenAI Research, Available at: https://openai.com/research/video-generation-models-as-

world-simulators

[20] Takeshi Kojima, et al. (2025), "A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics", arXiv preprint

arXiv:2505.12583, Available at: https://arxiv.org/abs/2505.12583

[21] Takeshi Kojima (2022), "zero_shot_cot", GitHub Repository, Available at: https://github.com/kojima-takeshi188/zero_shot_cot

[22] 東京大学松尾・岩澤研究室(2026), "大規模言語モデル社会実装講座", 東京大学Web.Lab教育プログラム, Available at: https://weblab.t.u-

tokyo.ac.jp/education/large-language-model/

[23] Sander Schulhoff, et al. (2024), "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques", arXiv preprint arXiv:2406.06608, Available at:

https://arxiv.org/abs/2406.06608

[24] Jason Wei, et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models", arXiv preprint arXiv:2201.11903, Available at:

https://arxiv.org/abs/2201.11903

[25] Takeshi Kojima, et al. (2022), "Large Language Models are Zero-Shot Reasoners", arXiv preprint arXiv:2205.11916, Available at:

https://arxiv.org/abs/2205.11916

[26] Shane Gu (2025), "X Post (status/1972309771610100179)", X (formerly Twitter), Available at:https://x.com/shaneguML/status/1972309771610100179

[27] Xuezhi Wang, et al. (2023), "Self-Consistency Improves Chain of Thought Reasoning in Language Models", arXiv preprint arXiv:2203.11171, Available at:

https://arxiv.org/abs/2203.11171

[28] Sweta Agrawal, et al. (2025), "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning", arXiv preprint arXiv:2502.14856, Available at:

https://arxiv.org/abs/2502.14856

[29] Raimi Karim (2019), "Illustrated: Self-Attention", Towards Data Science, Available at: https://towardsdatascience.com/illustrated-self-attention-

2d627e33b20a

[30] Jay Alammar (2018), "The Illustrated Transformer", Visualizing machine learning one concept at a time, Available at: http://jalammar.github.io/illustrated-

transformer/

[31] Tom Henighan, Jared Kaplan, et al. (2020), "Scaling Laws for Autoregressive Generative Modeling", arXiv preprint arXiv:2010.14701, Available at:

https://arxiv.org/abs/2010.14701

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

104

## Reference

104

[32] Daisuke Okanohara, "X Post (status/1972421341988225340)", X (formerly Twitter), Available at: https://x.com/hillbig/status/1972421341988225340

[33] Rewon Child, et al. (2019), "Generating Long Sequences with Sparse Transformers", arXiv preprint arXiv:1904.10509, Available at:

https://arxiv.org/abs/1904.10509

[34] sunbluesome (2022), "Sparse Transformerを理解したい", Zenn, Available at: https://zenn.dev/sunbluesome/articles/5f6a86dfa1e1be

[35] William Fedus et al. (2022), "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", Journal of Machine Learning

Research 23 (2022) 1-39, Available at: https://jmlr.org/papers/v23/21-0998.html

[36] Tim Dettmers, et al. (2022), "A Gentle Summary of LLM.int8(): Zero Degradation Matrix Multiplication for Large Language Models", Hugging Face Blog,

Available at: https://huggingface.co/blog/hf-bitsandbytes-integration

[37] Microsoft Deep Speed Team (2023), "DeepSpeed: 深層学習の訓練と推論を劇的に高速化するフレームワーク", DeepSpeed Official, Available at:

https://www.deepspeed.ai/assets/files/DeepSpeed_Overview_Japanese_2023Jun7th.pdf

[38] Chung, Hyung Won, et al. (2022), "Scaling Instruction-Finetuned Language Models", arXiv preprint arXiv:2210.11416, Available at:

https://arxiv.org/abs/2210.11416

[39] Edward J. Hu et al. (2021), "LoRA: Low-Rank Adaptation of Large Language Models", arXiv preprint arXiv:2106.09685, Available at:

https://arxiv.org/abs/2106.09685

[40] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", Advances in Neural Information

Processing Systems (NeurIPS 2023), Available at: https://arxiv.org/abs/2305.18290

[41] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv preprint

arXiv:2402.03300, Available at: https://arxiv.org/abs/2402.03300

[42] 株式会社サイバーエージェント(2023), "サイバーエージェント、最大68億パラメータの日本語LLM（大規模言語モデル）を一般公開―オープンなデータで学習した

商用利用可能なモデルを提供―", サイバーエージェントニュース, Available at: https://www.cyberagent.co.jp/news/detail/id=28817

[43] rinna株式会社(2023), "rinna、日本語に特化した36億パラメータのGPT言語モデルを公開", rinna株式会社ニュース, Available at:

https://rinna.co.jp/news/2023/05/20230507.html

[44] Stability AI Japan (2023), "日本語言語モデル「Japanese StableLM Alpha」をリリースしました", Stability AI Blog, Available at:

https://ja.stability.ai/blog/japanese-stablelm-alpha

[45] Ledge.ai編集部(2023), "LINE 36億パラメータの日本語LLMを公開商用利用も可", Ledge.ai, Available at: https://ledge.ai/articles/line_japanese_large_lm

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

105

## Reference

105

[46] 日本電気株式会社(2023), "NEC、130億パラメータで世界トップクラスの日本語性能を有する軽量なLLMを開発(2023年7月6日): プレスリリース", NEC プレスリ

リース, Available at: https://jpn.nec.com/press/202307/20230706_02.html

[47] OpenAI (2023), "GPT-4", OpenAI Research, Available at: https://openai.com/research/gpt-4

[48] ELYZA (2023), "70億パラメータの商用利用可能な日本語LLM「ELYZA-japanese-Llama-2-7b」を一般公開しました", ELYZA ニュース, Available at:

https://elyza.ai/news/2023/08/29/70%E5%84%84%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%81%AE%E5%95%86%E7%

94%A8%E5%88%A9%E7%94%A8%E5%8F%AF%E8%83%BD%E3%81%AA%E6%97%A5%E6%9C%AC%E8%AA%9Ellmelyza-ja

[49] 日本電信電話株式会社(2023), "NTT版LLM「tsuzumi」", NTT R&D Website, Available at: https://www.rd.ntt/research/LLM_tsuzumi.html

[50] 株式会社ELYZA (2024), "700億パラメータの日本語LLM「ELYZA-japanese-Llama-2-70b」を開発し、デモを公開しました", ELYZA 公式ブログ(note), Available

at: https://note.com/elyza/n/n0ea755ca3e7b

[51] 楽天グループ株式会社(2024), "楽天、日本語に最適化したオープンかつ高性能なLLMを公開", 楽天グループプレスリリース, Available at:

https://corp.rakuten.co.jp/news/press/2024/0321_01.html

[52] rinna株式会社(2023), "rinna、Llama 2の日本語継続事前学習モデル「Youri 7B」シリーズを公開", rinna株式会社ニュース, Available at:

https://rinna.co.jp/news/2023/10/20231031.html

[53] 株式会社サイバーエージェント(2024), "独自の日本語LLM（大規模言語モデル）のバージョン3を一般公開―225億パラメータの商用利用可能なモデルを提供―", サ

イバーエージェントニュース, Available at: https://www.cyberagent.co.jp/news/detail/id=30463

[54] Swallow-LLM Project (2024), "Llama 3 Swallow", Swallow-LLM GitHub Pages, Available at: https://swallow-llm.github.io/llama3-swallow.ja.html

[55] LLM-jp (2024), "大規模言語モデル「LLM-jp-13B v2.0」を構築・公開", LLM-jp 公式ブログ, Available at: https://llm-jp.nii.ac.jp/blog/2024/04/30/v2.0-

release.html

[56] 株式会社Preferred Networks (2024), "GENIAC第1サイクルの開発成果として大規模言語モデルPLaMo-100B-Pretrained を公開", Preferred Networks ニュース,

Available at: https://www.preferred.jp/ja/news/pr20241015

[57] 株式会社Preferred Networks (2023), "PLaMo-13Bを公開しました", Preferred Networks Tech Blog, Available at: https://tech.preferred.jp/ja/blog/llm-

plamo/

[58] 日本電気株式会社(2024), "NEC、世界トップレベル性能の高速な大規模言語モデル(LLM) cotomi Pro / cotomi Lightを開発", NEC プレスリリース, Available at:

https://jpn.nec.com/press/202404/20240424_01.html

[59] ストックマーク株式会社(2024), "ハルシネーションを大幅抑止し専門的な質問にも正確な回答が可能な生成AI ストックマーク、独自の130億パラメータのLLMを開

発し商業利用可能なオープンソースとして公開", ストックマークニュース, Available at: https://stockmark.co.jp/news/20240516

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

106

## Reference

106

[60] SB Intuitions株式会社(2024), "SB Intuitions、独自の日本語LLMを構築アカデミアや産業界の研究開発に資するために70億、130億、650億パラメータの日本語

LLMを公開", SB Intuitions プレスリリース, Available at: https://www.sbintuitions.co.jp/news/press/20240614_01/

[61] 富士通株式会社(2024), "スーパーコンピュータ「富岳」で学習した大規模言語モデル「Fugaku-LLM」を公開", 富士通プレスリリース, Available at:

https://pr.fujitsu.com/jp/news/2024/05/10.html

[62] 東京工業大学(2023), "日本語に強い大規模言語モデル「Swallow」を公開", 東京工業大学ニュース, Available at: https://www.titech.ac.jp/news/2023/068089

[63] 東京大学松尾・岩澤研究室(2024), "松尾・岩澤研究室、経産省・NEDOの「GENIAC」プロジェクトにおいて、国内初となる大規模言語モデル（LLM）のマルチモー

ダル化等の開発成果を公開", 東京大学Web.Lab ニュース, https://weblab.t.u-tokyo.ac.jp/2024-08-30/

[64] llm-jp (2024), "Awesome Japanese LLM", GitHub Pages, https://llm-jp.github.io/awesome-japanese-llm/

[65] weblab-GENIAC (2024), "Tanuki-8B-dpo-v1.0", Hugging Face Spaces, https://huggingface.co/spaces/weblab-GENIAC/Tanuki-8B-dpo-v1.0

[66] Dan Swinhoe (2024), "Microsoft bought twice as many Nvidia Hopper GPUs as other big tech companies - report", DatacenterDynamics,

https://www.datacenterdynamics.com/en/news/microsoft-bought-twice-as-many-nvidia-hopper-gpus-as-other-big-tech-companies-report/

[67] Timothy Prickett Morgan (2024), "Nvidia Unfolds GPU, Interconnect Roadmaps Out To 2027", The Next Platform,

https://www.nextplatform.com/2024/06/02/nvidia-unfolds-gpu-interconnect-roadmaps-out-to-2027/

[68] Linting Xue, et al. (2021), "mT5: A massively multilingual pre-trained text-to-text transformer", Proceedings of the 2021 Conference of the North

American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT 2021), https://aclanthology.org/2021.naacl-

main.41/

[69] 櫻井章雄(2022), "世界で開発が進む大規模言語モデルとは（後編）", NTTデータ先端技術株式会社コラム,

https://www.intellilink.co.jp/column/ai/2022/072800.aspx

[70] LLM-jp (2024), "llm-jp-corpus-v4", GitLab Datasets, https://gitlab.llm-jp.nii.ac.jp/datasets/llm-jp-corpus-v4

[71] 個人情報保護委員会(2023), "生成AIサービスの利用に関する注意喚起等について", 個人情報保護委員会ニュース,

https://www.ppc.go.jp/news/careful_information/230602_AI_utilize_alert/

[72] OpenAI (2026), "Terms of Use", OpenAI Policies, https://openai.com/ja-JP/policies/row-terms-of-use/

[73] DeepSeek-AI(2025),”DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning”, arXiv preprint https://arxiv.org/abs/2501.12948 ,

Available at: https://arxiv.org/abs/2501.12948

”

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0
