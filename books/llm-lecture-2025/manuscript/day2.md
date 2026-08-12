# Day 2

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

## 推論（Prompting，In-context Learning）

## 原田憲旺

許諾なく撮影や第三者

への開示を禁止します

## 大規模言語モデル講座2025

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

3

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 原田憲旺（はらだけんおう）@KH_ls_ippon

3

## 松尾・岩澤研博士課程3年

## LLM講座立ち上げ時に講座の資料作成・コンペ作成担当

## GENIACで評価担当

## AI白書2025 生成AIエディション執筆協力

## DeepLearning.ai の生成AI講義の翻訳

## 岸田総理・石破総理生成AI講義TA・講師

## ■研究テーマ

## -

## 大規模言語モデルの評価、大規模言語モデルによる評価

## -

## 大規模言語モデルの指示追従能力について

## -

## Web Agentを活用したUI/UX評価

## -

## 教育場面における大規模言語モデル応用

## ■担当講座

## -

## 基礎編第2回講義・演習

## 自然言語処理学会2024の発表風景

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

4

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## ChatGPTの利用拡大(1週あたり7億人が利用、180億メッセージ)

## •

## 仕事用途は27％、利用者の半分ほどが26歳以下、男女比は1:1に

## •

## 全利用用途の80%はPractical Guidance, Seeking Information, Writing

[1]Chatterji et al., 2025, How People Use ChatGPT

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

5

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 原田のLLM使用例

## •

## 研究者の対談やインタビューPodcastを翻訳・要約(Writing)

## •

## 1時間あるPodcastでもGeminiで、知りたいところだけを聞きに行ける

## •

## 音声・動画も対応するマルチモーダル

## •

## 研究分野の初手サーベイ(Information Seeking)

## •

## 数十件論文を調査するDeep Research (Gemini, ChatGPT)

## •

## 同じ質問を複数サービスに投げながらキャッチアップ

## •

## 海外講義資料の説明補足(Writing)

## •

## 投影資料だけ公開している場合でも追加検索や文脈追加で内容を追える

## •

## 要点箇条書き→ 文章(Writing)

## •

## コーディング補助やデータ整形(Writing/Practical Guidance)

## •

## 自作ワークフロー: https://github.com/kenoharada/labudy

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

6

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルへの指示の仕方・モデルの回答の選び方を工夫してモデルを活用する

6

## LLM

## Generative AI

## 上の単語を日本語に翻訳して

## Generative AI

## について5歳児でも

## 分かるように説明して

## 生成AI

## 「生成AI（せいせいAI）」

## っていうのは、コンピュー

## ターが絵やお話を自分で作

## れる仕組みのことだよ。例

## えば、君が「お花の絵を描

## いて」と言ったら、そのコ

## ンピューターがとっても綺

## 麗なお花の絵を描いてくれ

## るんだ。

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

7

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 目次

## •

## Decodingの基礎(greedy decoding, top-p sampling)

## •

## Promptingの基礎(Few-shot, CoT)

## •

## Meta-generation (Best-of-N, Self-refine, LLM-as-a-Judge)

## •

## 発展的なプロンプト例

## •

## LLMを使いこなしたサービス例

## •

## モデルの選択

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Decoding(デコーディング)の基礎

## Decode: 復号・解読

## Decoding algorithms: Token-level generation algorithms (Welleck et al., 2024)

## Decoding as a choice of Algorithm + Scoring Function (Amini et al., 2023)

## モデルの出力から”望む”出力を得るための様々な手法

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

9

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 言語モデル(Language Model) とは

## •

## ある単語の系列（≒文章）がどれくらい発生しやすいかをモデル化したもの

## •

## 単語の系列（𝑥1, 𝑥2, ⋯, 𝑥𝐿）に、その生成確率𝑝(𝑥1, 𝑥2, ⋯, 𝑥𝐿)を

## 割り当てる確率モデル𝑝のこと

## 𝑝(日本, の, 首都, は, 東京) = 0.02

## 𝑝(日本, の, 首都, は, パリ) = 0.00001

## 𝑝(東京, の, 首都, は, 日本) = 0.0005

## “良い”言語モデルへの期待:

## 文法的・常識的観点で誤りのある文章には低い確率を割り当てる

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

10

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 自己回帰言語モデル(Autoregressive Language Models)

## •

## 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿を条件分布の積として表現する

## 𝑝𝑥1, 𝑥2, ⋯, 𝑥𝐿= 𝑝𝑥1 𝑝𝑥2 𝑥1 ⋯𝑝(𝑥𝐿|𝑥1, 𝑥2, ⋯, 𝑥𝐿−1)

## 𝑝(日本, の, 首都) = 𝑝日本𝑝(の|日本) 𝑝(首都|日本, の)

## •

## このように確率の連鎖律で分解したモデルを特に自己回帰言語モデルと呼ぶ

## •

## 条件付き確率がわかると，生成することもできる

## 𝑝東京日本, の, 首都, は) = 0.2

## 𝑝パリ日本, の, 首都, は) = 0.001

## 𝑝カイロ日本, の, 首都, は) = 0.0005

## 日本の首都は→ 東京

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

11

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 言語モデルの活用: 条件付き確率をもとにタスクを解く

## タスク

## 翻訳

## 質問応答

## 要約

## モデルへの入力

## 英語の文章

## 質問

## 文書

## モデルの出力

## 日本語の文章

## 回答

## 短い記述

## 𝑝𝑥𝑖+1:𝐿𝑥1, 𝑥2, ⋯, 𝑥𝑖=

## ෑ

## 𝑗=𝑖+1

## 𝐿

## 𝑝𝑥𝑗𝑥1:𝑖, 𝑥𝑖+1:𝑗−1)

## どのようにモデルから出力を得るか？→ Decoding

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

12

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 言語モデルを使用する際の設定

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

13

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Decoding: 言語モデルの出力から”望む”出力を得るための様々な手法

## •

## Greedy decoding

## •

## 毎ステップで一番確率の高いものを選ぶ

## •

## Beam search

## •

## いくつか候補を残しておき、複数ステップ単位でスコアの高いものを選ぶ

## •

## Ancestral sampling

## •

## 全候補から確率に基づいてサンプリング

## •

## Top-k sampling

## •

## 上位k個のものからサンプリング

## •

## Top-p sampling (nucleus sampling)

## •

## 上位から合計してp*100 %になるような候補の中からサンプリング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

14

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Greedy decoding

## •

## 毎ステップで一番確率の高いものを選ぶ

## •

## 必ずしも文章全体として確率が一番高くなるわけではない

## •

## 繰り返しがよく見られた

[2] How to generate text: using different decoding

methods for language generation with Transformers,

https://huggingface.co/blog/how-to-generate

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

15

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Beam search

## •

## いくつか候補を残しておき、複数ステップ単位でスコアの高いものを選ぶ

## •

## 指定のビーム数(num_beams)候補を残して次の深さを探索

## •

## 計算量多い

## •

## 出力が面白くない(当たり障りがない)

## •

## 出力が短くなる

[2] How to generate text: using different decoding methods for

language generation with Transformers,

https://huggingface.co/blog/how-to-generate

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

16

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Top-k sampling

## •

## Top-k:上位k個のものからサンプリング

## •

## Long-tail問題、有望な選択肢の除外

[2] How to generate text: using different decoding methods for language

generation with Transformers, https://huggingface.co/blog/how-to-generate

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

17

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Top-p sampling / nucleus sampling (Holtzman et al., 2020)

## •

## Top-p: 上位から合計してp*100 %になるような候補の中からサンプリング

## •

## Top-kよりは柔軟性がある

[2] How to generate text: using different decoding methods for language

generation with Transformers, https://huggingface.co/blog/how-to-generate

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

18

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Samplingを左右するTemperature

## •

## 分布の尖り方を調整するパラメータ、下記の式のTにあたる値

## •

## Tの値を0に近づけるほど尖り、大きくするほどランダム性が高まる

## 𝑒𝑧𝑤/𝑇

## σ𝑗=1

## 𝑉

## 𝑒𝑧𝑗/𝑇

[3]Cohere (2024), "Parameters for Controlling Outputs", Cohere LLMU,

Available at: https://cohere.com/llmu/parameters-for-controlling-outputs ,

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

19

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 補足: temperatureを0にしても決定的にならないこともある

## 浮動小数点の計算は順序によって変わりうる

## 同時にリクエストを処理している際(バッチ処理)に、処理の分割の仕方が変わる

## →計算の順序が異なる→ 決定的にならない

## GPUでの処理を修正すれば決定的にできる

[4]Thinking Machines (2024), "Defeating Nondeterminism in LLM Inference",

Thinking Machines Blog, Available at: https://thinkingmachines.ai/blog/defeating-

nondeterminism-in-llm-inference/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

20

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## どのDecoding手法を用いれば良いか？

## •

## Taskの性質に基づいた検討→多様性が必要かどうか？

## •

## 物語生成・アイディア出し→ sampling手法

## •

## 知識を問う系・翻訳→ Greedy decoding, Beam Search

## •

## Greedy decodingの生成, temperature・Top-pを変えて複数生成し見比べてみる

## •

## A Thorough Examination of Decoding Methods in the Era of LLMs

## •

## The Curious Case of Neural Text Degeneration

## •

## Is GPT-3 Text Indistinguishable from Human Text? Scarecrow: A Framework for

## Scrutinizing Machine Text

## •

## Trading Off Diversity and Quality in Natural Language Generation

## •

## It’s MBR All the Way Down: Modern Generation Techniques Through the Lens of

## Minimum Bayes Risk

## •

## 系列の評価: 確率が高いものが本当に欲しい出力か？

## •

## → Reward model/LLMs-as-Judgeを活用しBest-of-N (後述)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

21

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Decodingの基礎のまとめ

## •

## 条件付き確率で次の単語の候補が決まる

## •

## モデルは過去の文脈を踏まえ、次の単語のもっともらしさを出力

## •

## 過去の文脈を踏まえるための工夫、言語モデルの学習の工夫→ 第３回

## •

## 候補からどのように次の単語を選択するか

## •

## Greedy decoding, Top-p samplingなどのDecoding手法

## •

## タスクによって適した手法が異なる

## •

## モデルへの入力（過去の文脈）を工夫することでモデルにタスクを解かせる

## •

## → プロンプティング

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

22

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料

## •

## Generating Text from Language Models,

## https://rycolab.io/classes/acl-2023-tutorial/

## •

## Stanford CS324 Introduction, https://stanford-

## cs324.github.io/winter2022/lectures/introduction/

## •

## CMU Advenced NLP Inference I Decoding and Generation Algorithms,

## https://cmu-l3.github.io/anlp-spring2025/static_files/anlp-s2025-07-

## decoding.pdf

## •

## From Decoding to Meta-Generation:Inference-time Algorithms for

## Large Language Models, https://arxiv.org/abs/2406.16838

## •

## Generation strategies,

## https://huggingface.co/docs/transformers/v4.56.0/en/generation_str

## ategies

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Prompting(プロンプティング)の基礎

## コマンドプロンプト(command prompt)

## 人間の入力を促す表示

## C:¥>

## ~$

## 近年のprompt

## AIの出力を促す文字列

## 質問: 日本の首都は？

## 回答:

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

24

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-3の登場(Brown et al., 2020)

## “Here we show that scaling up language models greatly improves task-

## agnostic, few-shot performance, sometimes even reaching

## competitiveness with prior state-of-the-art finetuning approaches.

## Specifically, we train GPT-3, an autoregressive language model with

## 175 billion parameters, 10x more than any previous non-sparse

## language model, and test its performance in the few-shot setting. For

## all tasks, GPT-3 is applied without any gradient updates or fine-tuning,

## with tasks and few-shot demonstrations specified purely via text

## interaction with the model.”

## これまで: タスク専用のモデルを大量のデータを元に重みを更新し学習

## GPT-3: 重みの再学習なしで、タスクの情報といくつかの例を含むpromptを変

## えるだけで様々なタスクで高性能

[5]Brown et al., 2020, Language Models are Few-Shot Learners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

25

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Before prompt (Before GPT-3)

## タスクごとにモデルを学習

## （NN以外）

## タスクごとにモデルを学習

## （NN）

## モデルを共有して学習

## （Fine-Tuning）

## モデルを固定して指示を変更

## （Prompting）

## 従来

## 現代

[6]Liu et al., 2021, Pre-train, Prompt, and Predict: A Systematic Survey of

Prompting Methods in Natural Language Processing

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

26

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## GPT-2での予兆(Radford et al., 2019)

## •

## 質問文の後に”A: “って入れたらある程度答えられた

## •

## 要約タスクで”TL;DR:” と入れたら要約を生成した

## •

## “Too Long, Didn‘t Read” (TL;DR) 要約を指すスラング

## •

## “english sentence = french sentence, english sentence =“で翻訳できた

[7]Radford et al., 2019, Language Models are Unsupervised Multitask Learners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

27

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## In-context learning (ICL, 文脈内学習) で重みの更新なく高性能

## •

## 重みを固定した言語モデルが、プロンプトでの条件付けによってタスクを実

## 行すること

## •

## 1つのモデルが重みパラメータの再学習なしで、プロンプト文の変更のみで

## 様々なタスクを高性能に行えることが当時の衝撃

[5]Brown et al., 2020, Language Models are Few-Shot Learners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

28

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## プロンプティング(prompting) とは？

## •

## 特定の機能の発生を促進(prompt)するような言語モデルに入力する

## コンテキスト文

## •

## Zero-shot: タスクの説明文・指示文のみ

## •

## Few-shot: 解かせたいTaskのデモンストレーション例をいくつか用意

## •

## 例が1つだけの場合はone-shot

## •

## ※ LLM以前のFew-shot learningとは意味合いが異なることに注意

[5]Brown et al., 2020, Language Models are Few-Shot Learners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

29

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## デモンストレーション数を増やすと性能が向上

## •

## 特にモデルが大規模な場合Few-Shotのデモンストレーションの追加で性能

## が大幅に上がることが多い

[5]Brown et al., 2020, Language Models are Few-Shot Learners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

30

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## デモンストレーション数を増やすと性能が向上

## •

## 100万トークンの入力を受け付けるlong contextモデルの活用

## •

## GPT-3は2048トークンしか受け付けなかった

## •

## コンテキスト長が増えると計算量が増える、更に性能向上を目指したい

## •

## → Fine-tuning、モデルがデカイので効率的に→ 第６回講義

[8]Agarwal et al., 2024, Many-Shot In-Context Learning

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

31

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## より難しいタスクをモデルに解かせるために

## •

## 答えに至るまでに複数ステップの処理が必要な、多段階推論が必要なタスク

[9]Wei et al., 2022, Chain-of-Thought Prompting Elicits

Reasoning in Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

32

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chain-of-Thought Prompting (Few-shot CoT)

## •

## 答えに至るまでに複数ステップの処理が必要な、多段階推論が必要なタスク

## •

## 答えに至るまでの思考の連鎖(Chain-of-Thought)を例で与える

[9]Wei et al., 2022, Chain-of-Thought Prompting Elicits

Reasoning in Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

33

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Chain-of-Thought Prompting (Few-shot CoT)

## •

## さまざまな数学のデータセットで

## 検証した結果

## •

## 特にモデルサイズが大きいときに

## 性能の改善が大きい

[9]Wei et al., 2022, Chain-of-Thought Prompting Elicits

Reasoning in Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

34

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## “Let’s think step by step” (Zero-shot CoT)

## •

## Chain-of-Thoughtの例を与えず、モデル自身に考えさせる

## •

## 「パイプラインとか人間が設計せずに、モデル自身に考えさせた方が良いのでは？」

## •

## → “Let’s think step by step”というフレーズが降りてきたby 小島さん

[10]Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

35

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## “Let’s think step by step” (Zero-shot CoT)の推論能力

## シングルステップの推論で解けるタスク

## （CoTがいらない）

## 常識推論（考えすぎて失敗するケースが多い）

## ※ 特にありえる解を複数選択してしまう

## 多段階推論が必要なタスク

## 2022年論文で作られたタスク

## （利用したモデルは2021までのデータで学習）

[10]Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

36

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## CoT(思考の連鎖)/Intermediate token(中間トークン)の効果

## CoT・中間トークンにより表現力が向上

## → 逐次的な処理を必要とするタスクの性能が向上

[11]Li et al., 2024, Chain of Thought Empowers Transformers to Solve Inherently Serial Problems

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

37

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## プロンプトの違いによる性能差

## 精度低

## 精度高

[12]Gonen et al., 2023, Demystifying Prompts in

Language Models via Perplexity Estimation

[13]Sclar et al., 2024, Quantifying Language Models' Sensitivity

to Spurious Features in Prompt Design or: How I learned to start

worrying about prompt formatting

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

38

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## プロンプトの違いによる性能差

## マニュアルで設定

[10]Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

39

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Prompt engineering (プロンプトエンジニアリング)

## 望む出力が得られるようにpromptを試行錯誤

## •

## 人手で試行錯誤

## •

## Few-shot prompting, CoT prompting

## •

## LLM開発元のガイドラインを参考に

## (例: https://platform.openai.com/docs/guides/prompt-engineering )

## •

## 自動で調整

## •

## 特殊なトークンを学習: Prefix tuning / Prompt tuning (ファインチューニング講義回)

## •

## Prompt文そのものを修正

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

40

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Automatic Prompt Engineer

## •

## 入出力のペアを使用し、指示文をLLM自身に複数予測させる

## •

## 指示文の候補を用いてタスク性能あるいは答えの尤度を計測

## スコアの高いものを選択

## •

## 指示文のバリエーションを出すために指示文の書き換えをLLMにさせる

[14]Zhou et al., 2023, Large Language Models are Human-Level Prompt

Engineers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

41

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Demonstrate-Search-Predict

## •

## 質問の分解の仕方・Follow-up質問等の中間過程を、LLMの試行錯誤で作成

## •

## 中間過程が合っているか否かは、その過程を経て得たLLMの出力と

## デモンストレーション例の出力が合致したかを基に判断

[15]Khattab et al., 2022, Large Language Models are Human-Level Prompt

Engineers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

42

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Optimization by PROmpting (OPRO)

## •

## 過去のプロンプトとそのスコアの変遷とともに、よりスコアが高くなるよう

## なプロンプトをLLMに作らせる

## •

## 1度の生成で8個ほど候補を作成し、スコアが良いものを選択

[16]Yang et al., 2024, Large Language Models as Optimizers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

43

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Genetic-Pareto (GEPA)

## •

## タスクを実際に行い成功・失敗の軌跡データを元に言語フィードバック作成

## しプロンプトを改善、あるいは他の有力なプロンプト候補と組み合わせる

## •

## 改善するプロンプトを選ぶ際は、多様性確保のために1問だけでも一番良い

## スコアを出しているプロンプトも候補に入れる

[17]Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can

Outperform Reinforcement Learning

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

44

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Genetic-Pareto (GEPA)

[17]Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can

Outperform Reinforcement Learning

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

45

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## プロンプティングの基礎まとめ

## •

## モデルへの入力文を、特定の機能の発生を促進(prompt)するよう工夫する

## ことで、様々なタスクで重みの再学習なしで高性能

## •

## デモンストレーション例を含めるFew-shot prompting、逐次的な処理・思

## 考過程を促すChain-of-Thought promptingが有効

## •

## 言い回しやフォーマットの違いで性能が大きく変わるので、prompt

## engineeringと呼ばれる試行錯誤が必要

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

46

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展: Meta-generation algorithms (Welleck et al, 2024)

## 複数回モデルを推論させた後に出力を得る

[18]Welleck et al., 2024, From Decoding to Meta-Generation: Inference-

time Algorithms for Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

47

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Self-Consistency, Majority Voting 多数決

## Top-k, Top-p samplingして複数の回答を得る→ 一番多かった回答を採用

[19]Wang et al., 2023, Self-Consistency Improves Chain of Thought

Reasoning in Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

48

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Best-of-N

## 複数の回答を得た後に、スコア化を行い一番高いスコアのものを選択

[20]Snell et al., 2024, Scaling LLM Test-Time Compute Optimally can be

More Effective than Scaling Model Parameters

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

49

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## どのようにスコアづけする？

## •

## 専用の分類器を学習する

## •

## Reward model, Process Reward Model (詳しくは第7回強化学習)

## •

## LLMがスコアを出すようにプロンプティングする

## •

## LLM-as-a-Judge (Zheng et al., 2023)

## •

## 細かい評価観点をプロンプトに入れる(Cook et al., 2024)

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

50

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLM-as-a-Judge: プロンプティングによりLLMに文を評価させる

## 長い文章を高く評価しがちというバイアスはあるものの

## 人間の評価とある程度一致

[21]Zheng et al., 2023, Judging LLM-as-a-Judge with MT-Bench and

Chatbot Arena

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

51

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## SELF-REFINE

## •

## 回答生成→回答へのフィードバック→回答の修正のループを回す

## •

## 生成・フィードバック・修正は同じモデル、プロンプティングを変更

[22]Madaan et al., 2023, Self-Refine: Iterative Refinement with Self-

Feedback

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

52

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: Claudeで実際に使用されているプロンプト

## 2500 wordsに及ぶ、属性に関する情報(retrieveして使う、名前やプロダクト

## 情報)、あるジャンルに対する返答姿勢の指定、フォーマットについての指定、

## knowledge cut-offの情報、アメリカの大統領選挙結果の情報

[23]Anthropic Release notes, System prompts

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

53

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: 敵対的プロンプト(Adversarial Prompt)

## ジェイルブレイク（DAN）

## •

## プロンプトの工夫による攻撃

## •

## 例：ジェイルブレイク

## （ペルソナを与えると本来答えないことも答え

## てくれる．”Do Anything Now” ．）

## •

## 加えると攻撃性が上がるトークンの存在なども

## 知られている

[24]Adversarial Prompting in LLMs

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

54

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: 生成AIを使うユーザーへのカウンター

## •

## 授業資料とは全く異なる趣旨のレポートを作成するように透明色の文字

## •

## 論文の査読結果が肯定的になるように

[25]島田拓(2025), "AIに課題を書かせると資料にない内容を出力――慶應大のAI対

策が話題に狙いを聞いた", ITmedia AI+, 公開日: 2025/05/01, Available at:

https://www.itmedia.co.jp/aiplus/articles/2504/30/news214.html

[26]日本経済新聞(2025), "論文内に秘密の命令文、AIに「高評価せよ」日韓米な

ど有力14大学で", 日本経済新聞, 公開日: 2025/06/29, Available at:

https://www.nikkei.com/article/DGXZQOUC13BCW0T10C25A6000000/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

55

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: DeepResearchをプロンプティングで実現

## 検索クエリの作成・検索が十分かの振り返り・回答生成をプロンプティング

[27] Gemini Fullstack LangGraph Quickstart

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

56

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: 論文からポスター生成

## 図の切り抜き処理・パワポを扱うライブラリと上手く組み合わせる

## 検索エンジンやコードの利用などについては応用講座第2回

[28]Pang et al., 2025, Paper2Poster: Towards Multimodal Poster Automation

from Scientific Papers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

57

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: 合成データ(Synthetic data)

## LLMの学習に使用するデータを人工的に(特にLLMを使用して)作る

## •

## Controllableな実験のために: TinyStories, Physics of LM

## •

## より複雑なデータセットを作るために: WizardLM, Alpaca

## •

## 大きくて優秀なモデルの能力を小さいモデルに: s1K, NaturalThoughts

## •

## 品質の高い事前学習データ: Textbooks Are All You Need

[29]Taori et al., 2023, Alpaca: A Strong,

Replicable Instruction-Following Model

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

58

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 発展的なプロンプト例: シミュレーション(Simulation)

## LLMに特定の人格・特徴を付与して人間の模擬

[30]Park et al., 2024, Generative Agent Simulations of 1,000 People

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

59

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(GPT-2, GPT-3開発裏話)

## •

## Ilya Sutskever - GPT-2,

## https://www.youtube.com/watch?v=T0I88NhR_9M

## •

## L11 Language Models -- guest instructor: Alec Radford (OpenAI) ---

## Deep Unsupervised Learning SP20,

## https://www.youtube.com/watch?v=BnpB3GrpsfM

## •

## An Observation on Generalization,

## https://www.youtube.com/watch?v=AKMuA_TVz3A

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

60

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(Promptingについて)

## •

## Stanford CS224U In-context learning,

## https://web.stanford.edu/class/cs224u/slides/cs224u-

## incontextlearning-2023-handout.pdf

## •

## Weng, Lilian. (Mar 2023). Prompt Engineering. Lil’Log.

## https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/.

## •

## Prompt Engineering Guide, https://www.promptingguide.ai/

## •

## Stanford CS224N Lecture 11: Efficient Adaptation,

## https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-

## lecture11-adapatation.pdf

## •

## CMU CS11-711 Advanced NLP Prompting and In-Context Learning,

## https://cmu-l3.github.io/anlp-spring2025/static_files/anlp-s2025-08-

## prompting.pdf

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

61

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(文脈内学習の謎・仕組み)

## •

## 大規模言語モデル応用第5回LLMの分析・解釈可能性

## •

## In-context Learning and Induction Heads, https://transformer-

## circuits.pub/2022/in-context-learning-and-induction-

## heads/index.html

## •

## Dai et al., 2023, Why Can GPT Learn In-Context? Language Models

## Secretly Perform Gradient Descent as Meta-Optimizers

## •

## Min et al., 2022, Rethinking the Role of Demonstrations: What Makes

## In-Context Learning Work?

## •

## Razeghi et al., 2022, Impact of Pretraining Term Frequencies on Few-

## Shot Numerical Reasoning

## •

## Wei et al., 2023, Larger language models do in-context learning

## differently

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

62

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(Chain-of-Thought)

## •

## Stanford CS 25 LLM Reasoning, https://dennyzhou.github.io/LLM-

## Reasoning-Stanford-CS-25.pdf

## •

## Wang et al., 2024, Chain-of-Thought Reasoning Without Prompting

## •

## Yao et al., 2023, Tree of Thoughts: Deliberate Problem Solving with

## Large Language Models

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

63

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(Meta-generation)

## •

## Beyond Decoding: Meta-Generation Algorithms for Large Language

## Models, https://cmu-l3.github.io/neurips2024-inference-tutorial/

## •

## CMU Advanced NLP Advanced Inference Strategies, https://cmu-

## l3.github.io/anlp-spring2025/static_files/anlp-s2025-21-inference.pdf

## •

## Brown et al., 2024, Large Language Monkeys: Scaling Inference

## Compute with Repeated Sampling

## •

## Wu et al., 2024, Inference Scaling Laws: An Empirical Analysis of

## Compute-Optimal Inference for Problem-Solving with Language

## Models

## •

## Gu et al., 2024, A Survey on LLM-as-a-Judge

## •

## Kamoi et al., 2024, When Can LLMs Actually Correct Their Own

## Mistakes? A Critical Survey of Self-Correction of LLMs

## •

## 2024Fall 大規模言語モデル(LLM)講座特別回：LLMの自己修正〜OpenAI

## o1 の関連研究〜

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

64

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料(発展的なプロンプト)

## •

## Grok prompts, https://github.com/xai-org/grok-prompts

## •

## Zou et al., 2023, Universal and Transferable Adversarial Attacks on

## Aligned Language Models

## •

## How we built our multi-agent research system,

## https://www.anthropic.com/engineering/multi-agent-research-

## system

## •

## OpenAI Codex CLI,

## https://github.com/openai/codex/blob/main/codex-

## rs/core/prompt.md

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMを使いこなしたサービス例

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

66

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## コーディング支援サービス(コードも言語)

## GitHub Copilot, Claude Code, Cursor, Cline, Windsurf, Devinなど

## Cursorは2023年リリース、今年6月$500 million in ARR, $900 million 調達

[31]Cursor at $100M ARR, https://sacra.com/research/cursor-at-100m-arr/

[32] Anysphere (2026), "Cursor - The AI-first Code Editor", Cursor, Available

at: https://cursor.com/ja

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

67

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Y Combinator(アメリカの有名VC)の出資先から見るAIサービス

## AIを使いこなして開発速度向上、AI活用による新たな価値創出

[33]Startup Directory, https://www.ycombinator.com/companies

[34]10 People + AI = Billion Dollar Company?,

https://www.youtube.com/watch?v=CKvo_kQbakU

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

68

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMを使いこなすための”context engineering”

## “次の手順・処理のために、コンテキストウィンドウ（LLMが一度に読み込める

## 情報）を最適な情報で満たす、繊細なアートであり科学”

## •

## 基本的なプロンプティング技術(今回)

## •

## RAG・Tool-use (応用編第2回)

## •

## 状態管理・マルチモーダル(応用編第７回)

[35] Andrej Karpathy (2025), "X Post

(status/1937902205765607626)", X (formerly Twitter),

Available at:

https://x.com/karpathy/status/1937902205765607626

[36]Gemini_Plays_Pokemon, https://www.twitch.tv/gemini_plays_pokemon

[37] Google (2025), "Gemini 2.5: Pushing the Frontier with Advanced

Reasoning, Multimodality, Long Context, and Next Generation Agentic

Capabilities", Google Keyword Blog, Available at:

https://blog.google/technology/ai/google-gemini-next-generation-

december-2025/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

69

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## LLMの活用についてコーディングしながら学べる講義を翻訳しました

## 日本語翻訳済のコース

## • ChatGPT Prompt Engineering for Developers

## • Building Systems with the ChatGPT API

## • How Diffusion Models Work

## • LangChain for LLM Application Development

## • LangChain Chat with Your Data

## 詳細はhttps://www.deeplearning.ai/courses/

[38] DeepLearning.AI, "Courses", DeepLearning.AI Official Website, Available at:

https://www.deeplearning.ai/courses/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

70

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料等

## •

## Andrej Karpathy: Software Is Changing (Again),

## https://www.youtube.com/watch?v=LCEmiRjPEtQ&list=PLQ-

## uHSnFig5NPx4adxl97CZb8vU4numwi&index=12

## •

## Andrew Ng: AI is Accelerating Startups,

## https://www.youtube.com/watch?v=RNJCfif1dPY

## •

## Vibe coding MenuGen, https://karpathy.bearblog.dev/vibe-coding-

## menugen/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルの選択

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

72

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルのアクセス手段による違い

## ■APIのみ

## •

## 重みは公開されていない, データを入力後に出力が得られる

## •

## 自前でコンピューターを用意することなく利用可能、従量課金

## •

## GPT (OpenAI), Gemini(Google), Claude(Anthropic) など

## ■公開モデル

## •

## 重みまで公開されている（分析にも適している）

## •

## 自分の手元のコンピューターで動かせる, 入力データを外部に出さなくて良い

## •

## Llama, Mistral, DeepSeek, Qwen, gpt-ossなど

## ■非公開モデル

## •

## 一部の研究機関のみ利用可能

## •

## PaLM (Google), Gopher (DeepMind)など

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

73

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## APIによるモデルの利用(GPTの例)

## •

## 1M tokenの入力あたり$1.25, 1M tokenの出力あたり$10

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

74

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 公開モデルの利用を便利にするライブラリ

## •

## Transformers

## •

## HuggingFaceと呼ばれるサービスにモデル・データセットが日々アップロードされる

## •

## モデル・データセット版GitHub

## •

## 様々なモデル、便利機能がすぐに利用できる

## •

## 演習でも扱います

## •

## 厄介なバグが埋め込まれることもあるので、何か問題が起きたらversionの確認を

## •

## vLLM

## •

## モデルの推論を高速に行うことができる

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

75

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 公開モデルを利用する際の計算資源

## •

## 自前でGPUを購入

## •

## H100(80GB) 1枚約600万円+ 電力消費+ メンテナンス+ 環境設定

## •

## 量子化(モデルを軽量にする手法)を施したgpt-oss-120bを利用可能

## •

## クラウド上GPU

## •

## 利用した時間に応じて課金が発生

## •

## H100 1枚を1時間あたり$1.49で利用可能な場合も

## •

## 有名なサービス: AWS, GCP, Azure, Lambda, HPC-AI, Hyperbolic

## •

## モデルホスティングサービス

## •

## モデル名を選択するだけで利用可能

## •

## GPT/Gemini等を利用する時と同じように、入出力の計算量ベースで課金が発生

## •

## 有名なサービス: Cerebras, Groq, Together.ai, Fireworks

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

76

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデルホスティングサービスの違い

## それぞれ独自の高速化・軽量化技術を開発している

[40]Cerebras Systems (2026), "Cerebras - AI

Supercomputing at Unprecedented Speed", Cerebras

Official Website, Available at: https://www.cerebras.ai/

[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers

and Performance Analysis", Artificial Analysis, Available at:

https://artificialanalysis.ai/models/gpt-oss-120b/providers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

77

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデル性能の違い

## lmarena(ユーザー投票型), HELM(複数ベンチマーク総合スコア)

## 個別のベンチマーク性能はTechnical Report参照

[41] LMSYS Org (2026), "Arena AI Leaderboard (formerly

LMSYS Chatbot Arena)", Arena AI, Available at:

https://lmarena.ai/leaderboard/

[42]Stanford CRFM, "Holistic Evaluation of Language Models

(HELM)", Center for Research on Foundation Models (CRFM),

Available at: https://crfm.stanford.edu/helm/capabilities/latest/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

78

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## モデル性能の違い(日本語)

[43]Nejumi LLMリーダーボード4,

https://wandb.ai/llm-leaderboard/nejumi-

leaderboard4/reports/Nejumi-LLM-4--VmlldzoxMzc1OTk1MA

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

79

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 自分自身で評価する際のツールと、評価の際の注意点

## •

## simple-evals/evals (OpenAI社)

## •

## llm-jp-eval (LLM-jp)

## •

## Lighteval (HuggingFace)

## プロンプトの違いや

## 選択肢の絞り方の違いにより

## 同じモデルでも

## 大きく異なるスコアが出る

## 同じモデルでも設定の違いにより

## 性能が大きく異なる

[44]Hugging Face (2024), "What's going on with the Open LLM Leaderboard and

MMLU?", Hugging Face Blog, Available at: https://huggingface.co/blog/open-llm-

leaderboard-mmlu

[45] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and

Performance Analysis", Artificial Analysis, Available at:

https://artificialanalysis.ai/models/gpt-oss-120b/providers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

80

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## 性能・価格・処理速度のトレードオフ

## とりあえずは一番性能の良いモデル(一番高いモデル)の使用を推奨

## ChatGPT, Gemini appの無料版ではなく有料版

## あるいはAPI playgroundで試してみる

[45] Google DeepMind (2026), "Gemini - Google's Next-Generation AI Models",

Google DeepMind, Available at: https://deepmind.google/models/gemini/

[39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers

and Performance Analysis", Artificial Analysis, Available at:

https://artificialanalysis.ai/models/gpt-oss-120b/providers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

81

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## OpenRouterを使用して様々なモデルをシュッと試す

## 同じインターフェースで複数のモデルを簡単に試すことができる

## 正解はオールドルーキーサウナ

## 全てのモデルが不正解

[46]OpenRouter (2026), "OpenRouter - A unified API for AI

models", OpenRouter Official Website, Available at:

https://openrouter.ai/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

82

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## その他参考資料等

## •

## The Second Half, https://ysymyth.github.io/The-Second-Half/

## •

## Successful language model evals, https://www.jasonwei.net/blog/evals

## •

## How to Build Good Language Modeling Benchmarks, https://ofir.io/How-to-Build-

## Good-Language-Modeling-Benchmarks/

## •

## Why You Should Stop Using HotpotQA for AI Agents Evaluation in 2025,

## https://qipeng.me/blog/stop-using-hotpotqa/

## •

## Singh et al., The Leaderboard Illusion, https://arxiv.org/abs/2504.20879

## •

## TinyML and Efficient Deep Learning Computing,

## https://hanlab.mit.edu/courses/2024-fall-65940

## •

## The Ultra-Scale Playbook: Training LLMs on GPU Clusters,

## https://huggingface.co/spaces/nanotron/ultrascale-playbook

## •

## How to Scale Your Model, https://jax-ml.github.io/scaling-book/

## •

## Stanford CS336 Lecture 5~7, https://stanford-cs336.github.io/spring2025/

## •

## AIと半導体AI半導体講座, https://weblab.t.u-tokyo.ac.jp/lecture/course-list/ai-and-

## semiconductors/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

83

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## [1]Chatterji et al., 2025, How People Use ChatGPT

## [2]How to generate text: using different decoding methods for language generation with Transformers,

## https://huggingface.co/blog/how-to-generate

## [3]Cohere (2024), "Parameters for Controlling Outputs", Cohere LLMU, Available at: https://cohere.com/llmu/parameters-

## for-controlling-outputs ,

## [4]Thinking Machines (2024), "Defeating Nondeterminism in LLM Inference", Thinking Machines Blog, Available at:

## https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/

## [5]Brown et al., 2020, Language Models are Few-Shot Learners

## [6]Liu et al., 2021, Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language

## Processing

## [7]Radford et al., 2019, Language Models are Unsupervised Multitask Learners

## [8] Agarwal et al., 2024, Many-Shot In-Context Learning

## [9]Wei et al., 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

## [10]Kojima et al., 2022, Large Language Models are Zero-Shot Reasoners

## [11]Li et al., 2024, Chain of Thought Empowers Transformers to Solve Inherently Serial Problems

## [12]Gonen et al., 2023, Demystifying Prompts in Language Models via Perplexity Estimation

## [13]Sclar et al., 2024, Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to

## start worrying about prompt formatting

## [14]Zhou et al., 2023, Large Language Models are Human-Level Prompt Engineers

## [15] Khattab et al., 2022, Large Language Models are Human-Level Prompt Engineers

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

84

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## [16]Yang et al., 2024, Large Language Models as Optimizers

## [17]Agrawal et al., 2025, GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

## [18]Welleck et al., 2024, From Decoding to Meta-Generation: Inference-time Algorithms for Large Language Models

## [19]Wang et al., 2023, Self-Consistency Improves Chain of Thought Reasoning in Language Models

## [20]Snell et al., 2024, Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters

## [21]Zheng et al., 2023, Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

## [22]Madaan et al., 2023, Self-Refine: Iterative Refinement with Self-Feedback

## [23]Anthropic Release notes, System prompts

## [24] Adversarial Prompting in LLMs

## [25]島田拓(2025), "AIに課題を書かせると資料にない内容を出力――慶應大のAI対策が話題に狙いを聞いた", ITmedia AI+, 公開

## 日: 2025/05/01, Available at: https://www.itmedia.co.jp/aiplus/articles/2504/30/news214.html

## [26]日本経済新聞(2025), "論文内に秘密の命令文、AIに「高評価せよ」日韓米など有力14大学で", 日本経済新聞, 公開日:

## 2025/06/29, Available at: https://www.nikkei.com/article/DGXZQOUC13BCW0T10C25A6000000/

## [27] Gemini Fullstack LangGraph Quickstart

## [28]Pang et al., 2025, Paper2Poster: Towards Multimodal Poster Automation from Scientific Papers

## [29]Taori et al., 2023, Alpaca: A Strong, Replicable Instruction-Following Model

## [30]Park et al., 2024, Generative Agent Simulations of 1,000 People

## [31]Cursor at $100M ARR, https://sacra.com/research/cursor-at-100m-arr/

## [32] Anysphere (2026), "Cursor - The AI-first Code Editor", Cursor, Available at: https://cursor.com/ja

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

85

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## [33]Startup Directory, https://www.ycombinator.com/companies

## [34]10 People + AI = Billion Dollar Company?, https://www.youtube.com/watch?v=CKvo_kQbakU

## [35] Andrej Karpathy (2025), "X Post (status/1937902205765607626)", X (formerly Twitter), Available at:

## https://x.com/karpathy/status/1937902205765607626

## [36]Gemini_Plays_Pokemon, https://www.twitch.tv/gemini_plays_pokemon

## [37] Google (2025), "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next

## Generation Agentic Capabilities", Google Keyword Blog, Available at: https://blog.google/technology/ai/google-gemini-next-

## generation-december-2025/

## [38] DeepLearning.AI, "Courses", DeepLearning.AI Official Website, Available at: https://www.deeplearning.ai/courses/

## [39] Artificial Analysis (2026), "GPT-OSS-120B Model Providers and Performance Analysis", Artificial Analysis, Available at:

## https://artificialanalysis.ai/models/gpt-oss-120b/providers

## [40]Cerebras Systems (2026), "Cerebras - AI Supercomputing at Unprecedented Speed", Cerebras Official Website,

## Available at: https://www.cerebras.ai/

## [41] LMSYS Org (2026), "Arena AI Leaderboard (formerly LMSYS Chatbot Arena)", Arena AI, Available at:

## https://lmarena.ai/leaderboard/

## [42]Stanford CRFM, "Holistic Evaluation of Language Models (HELM)", Center for Research on Foundation Models (CRFM),

## Available at: https://crfm.stanford.edu/helm/capabilities/latest/

## [43]Nejumi LLMリーダーボード4, https://wandb.ai/llm-leaderboard/nejumi-leaderboard4/reports/Nejumi-LLM-4--

## VmlldzoxMzc1OTk1MA

## [44]Hugging Face (2024), "What's going on with the Open LLM Leaderboard and MMLU?", Hugging Face Blog, Available at:

## https://huggingface.co/blog/open-llm-leaderboard-mmlu

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

86

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

## Reference

## [45] Google DeepMind (2026), "Gemini - Google's Next-Generation AI Models", Google DeepMind, Available at:

## https://deepmind.google/models/gemini/

## [46]OpenRouter (2026), "OpenRouter - A unified API for AI models", OpenRouter Official Website, Available at:

## https://openrouter.ai/

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY OF TOKYO

## LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0
