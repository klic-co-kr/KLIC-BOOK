# Day 7

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

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

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 第7回：強化学習

## 2025/11/12

許諾なく撮影や第三者への

開示を禁止します

## 大規模言語モデル講座2025

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 講師自己紹介

3

## 髙城頌太（東京大学大学院工学系研究科松尾研究室博士2年）

## •

## 経歴

## •

## 2019年3月奈良工業高等専門学校情報工学科修了

## •

## 2022年3月大阪大学基礎工学部システム化学科修了

## •

## 2022年4月〜東京大学工学系研究科技術経営戦略学専攻

## •

## インターン等

## •

## Sony ML R&D intern

## •

## DeNA backend intern

## •

## Recruit Data Specialist Intern

## •

## SanSan Intern

## •

## 専門分野：

## •

## 大規模言語モデル，強化学習，ロボティックス

## •

## その他の活動：

## •

## 「Deep Learning基礎講座」「深層強化学習スプリングセミナー」「大規模言語モデル講座」「世界モデ

## ルと知能」などの講師担当

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 今回の目的・目標

4

## •

## 目的：

## •

## LLMにおける強化学習とは何か，またその仕組みや必要性について理解する

## •

## 目標：

## •

## LLMにおける強化学習の目的について理解して説明できる．

## •

## 強化学習の手法(RLHF/DPO/GRPO)の概要を説明できる．

## •

## PyTorchで各手法の実装ができる．

## •

## 想定している前提知識：

## •

## これまでの講義の内容+ 基本的な深層学習の知識

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM 訓練フローにおけるFine-Tuning

## Pre-Training

## 大規模コーパスによる自己教師あり学習を通して、言語モデルに

## 語彙・文法・知識といった基本的な言語理解を獲得させる段階

## Supervised※ Fine-Tuning

## ラベル付きデータによる教師あり学習を通し、言語モデルの性能

## を改善したり、特定のタスクやドメインへの適応を実現する段階

## Reinforcement Learning

## 人間のフィードバックやルールベースの報酬を用いた強化学習を通し、言語モデルの

## 出力がより人間の価値観に沿ったものにしたり、推論能力を向上させるように調整

## する段階

## 5

## Step 1

## Step 2

## Step 3

※ 基本的にFine-Tuning はSupervisedのため冗長な表現に思われるが、強化学習手法(RLHF)と区別するためこのように表現される。

また、あえてこのように表現する場合には、一般の教師ありFine-Tuningではなく、後述のInstruction Tuningを指すことが多い。

## 1

## 2

## (より広義の)

## Fine-Tuning

## /

## Post-

## Training

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Pre-Training vs. Fine-Tuning / Post-Training

## 6

## Pre-Training

## データ

## Fine-Tuning / Post-Training

## 目的

## -

## 語彙・文法・知識・推論能力などの言

## 語能力を、言語モデルに導入

## 一般的な

## 手法

## -

## 自己教師あり学習

## -

## Next Token Prediction

## -

## Masked Language Model

## -

## 大規模データセット

## -

## 例CommonCrawl (GPT-3):

## 410B tokens (570GB)

## - 事前学習済みモデルの性能改善や、

## 様々なタスクに対する適応を実現

## -

## 教師あり学習

## -

## 下流タスクへの特化

## -

## Instruction Tuning

## -

## 強化学習

## -

## 良質な小規模データセット

## -

## 例LIMA: 1000サンプル(3MB)

## - 人間・モデルによるフィードバック

## 1

## 2

## : Day7のトピック

## : Day6のトピック

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## そもそも強化学習とは？

7

## •

## 問題設定

## •

## エージェント(行動主体)は環境の状態に基づいて, 逐次的に行動を決定する

## •

## 強化学習の目的

## •

## 行動の結果得られる報酬を利用し, その環境で最も良い行動ルール(最適方策)を学習したい

## 代表的な応用例: AplhaGo

## 人間の対局データなしに経験から学習して人間超えを達成

[1] DeepMind, "MuZero: Mastering Go, chess, shogi and Atari without rules" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 言語モデルにおける強化学習とは？

8

## •

## 出力文章に対して報酬を与えて，それをフィードバックする

## •

## Pretrain, Fine-TuningのNext Token Predictionとは異なる枠組みで学習する

## •

## 報酬は人間が与える場合や別のLLMを用いる場合，ルールベースのモデルで与

## える場合がある(RLHF, RLAIF, RLVR)

## LLM

## 織田信長は何年に生まれた？

## 1582年。

## 彼は本能寺で明智光秀に・・・

## 織田信長は1534年に

## 生まれました。

## 良かった出力が出やすくなるように

## フィードバック

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルにおける現在の強化学習の用途

9

## ①アライメント

## ②推論能力の向上

## •

## AIが差別的な発言や暴力的な発言をしな

## いように、人間の価値観に合わせるように学

## 習

## •

## 倫理的に問題がある発言にはマイナスのフィ

## ードバックを与えて強化学習を行う

## •

## 数学やコーディングなどのタスクで、深く思考

## するように強化学習を行うことによって飛躍

## 的に性能が向上

## •

## 長く推論することで数学オリンピックで金メダ

## ルを獲得したりIQテストで140越えを記録

[3] TrackingAI, "AI Progress Tracking" より引用

[2] CNN.co.jp (2017), AlphaGo関連記事より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 言語モデルにおける強化学習の種類

10

## •

## Reinforcement Learning from Human Feedback / Direct Preference Optimization

## •

## 人間のフィードバックデータを用いた強化学習

## •

## 人間の価値観に合わせることが目的

## •

## Reinforcement Learning with Verifiable Reward

## •

## ルールベースの報酬器を用いた強化学習

## •

## 数学能力, コーディング能力の向上が目的

## アライメントが目的

## 推論能力向上が目的

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reinforcement Learning with Human Feedback(RLHF)の概要

11

## •

## Instruct GPT, ChatGPTなどで利用されている．

## •

## LLMで同じ問題に対して複数の答えを出力させ，人間がPreferenceをつける．

## •

## Preferenceを予測するように報酬モデルを学習し，強化学習する（PPO）

## (1) Supervised Fine Tuning

## (2) Train Reward Model

## (3) Reinforcement Learning

## [5] OpenAI (2022), "Instruction Following" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの応用例(ChatGPT)

12

## •

## OpenAIは2022年11月30日にChatGPTを公開

## •

## 現在は無料公開中で，公開から1 週間で100 万ユーザ，2 ヶ月で1 億ユーザ

## に到達．

## •

## 従来の大規模言語モデルよりも高度な意味理解と会話(チャット) が可能。

## GPT-3をベースにしている．

## [6] Zhao, Wayne Xin, et al. (2023), "A Survey of Large Language Models" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reinforcement Learning with Verifiable Reward(RLVR)の概要

14

## •

## 検証可能な報酬モデルを用いて強化学習を行う

## •

## ex. 数学であれば最後の出力が合っているか, コードなら実行結果が合うか，テストが通

## るかなど

## •

## RLHFの場合は報酬モデルを学習させる必要であったが、RLVRでは不要

## Ways to compute rewards

## ●

## Math-Verify [8] HuggingFace, “Math-Verify” を参

考)

## ●

## LLM-as-a-judge for facts

## ●

## Code Sandboxes

## ●

## More!

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRの応用例

15

## •

## o1による推論スケーリングというパラダイムシフトが起こってから，様々なモデルにRLVRが

## 応用されている．

## •

## 特に数学やコードなどの深い思考が必要なタスクにおいて、飛躍的な性能向上を見せて

## いる

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models" より

引用

[10] ARC Prize, "ARC Prize Leaderboard" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 目次

16

## • 人間のフィードバックからの強化学習について(RLHF/DPO)

## • 検証可能な報酬器からの強化学習について(RLVR)

## • LLMにおける強化学習のアプリケーション例

## • 今後の方向性

## • まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## これまでの言語モデルの問題点

17

## •

## 人間にとって好ましくない発言(設計者が意図しない発言)を行い炎上してし

## まう事態が発生

## マイクロソフトTay 1日で公開中止(2016年)

## 韓国イ・ルダ1 ヶ月でサービス提供停止(2021年)

## o

## Twitter に登場し、24 時間で5 万人フォロワー獲得、10

## 万回ツイート

## o

## 悪意を持った利用者の発言に影響受け、16 時間でヘイト

## 発言を繰り返す

## o

## カカオトークの会話100 億件にもとづいて作成、2 週間で

## 利用者75 万人

## o

## 性的マイノリティへのヘイト発言を行った

[11] 日本経済新聞(2021), “韓国で「対話AI」暴走

機械学習が

陥ったワナ” より引用

[2] CNN.co.jp (2017), "AlphaGo関連記事" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuningでの限界点

18

## このような意図しない発言をInstruction Tuningで対処するのは非常に難しい

## 1. 自然言語でのデータを集めるにはコストがかかる

## 2. 何かを言わない様にするという正解データを作ることが難しい

## 3. 直接的に人間の意図を学習することになっていない

## text-davinci-002(instruction tuning 後& RLHF前のモデル)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFによって直接的に意図を学習する

19

## text-davinci-003(RLHF後のモデル)

## •

## どの文章が意図通りの出力なのかをモデルにフィードバックする

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

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## フィードバックを介した意図の学習(概要図)

20

## •

## 人間が言語モデルの出力に対してフィードバックを行い，人間の意図に沿う

## ように学習していく

## •

## HITL(Human in the loop)型のアプローチを用いる

[12] Wolfe, Cameron R. (2023), "Specialized LLMs: ChatGPT, LaMDA, Galactica, Codex, Sparrow, and More" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 人間の意図通りにモデルを学習

21

## ↓OpenAIのAlignmentチームのリーダー

## •

## 人間の意図通りにモデルを学習することはAlignmentと呼ばれる

## •

## Alignmentを行うためにRLHFという技術が必要となる

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## そもそも人間の意図とは

22

## •

## 意図には明示的な意図と暗黙的な意図が存在する

## •

## 明示的な意図: 言語化して伝えている意図

## •

## Ex. この指示に従ってください，アシスタントとして振る舞ってください

## •

## 暗黙的な意図: 言語化はしてないが，対話において当たり前とされている意図

## •

## Ex. 捏造しない，有害なことは言わない

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## どのような意図の基準があるか(Alignmentの基準)

23

## •

## Helpful

## •

## ユーザーの質問に対して，できるだけ簡潔で効率的な回答を行う

## •

## 不足情報がある場合，適切な質問を投げかけて情報を引き出す

## •

## 相手のレベルに合わせた質問応答を行う

## •

## Honest

## •

## 情報の虚偽がなく，正確な文章を出力する

## •

## モデル自身がどの程度の不確実性のある情報かを提示することが重要

## •

## (モデル自身がモデルの知っていることを理解している必要がある)

## •

## Harmless

## •

## 攻撃的，差別的な発言をしない

## •

## 悪意のある質問を検知し，拒否をする

## 他にも，(Taxonomy, behavior, incentive, innner aspectsなど)

## この３つを合わせてalignされたAIと定義している論文もある(HHH)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## どのような意図の基準があるか: 具体例

24

## Helpful(HH-RLHF)

## Honest(HalEval)

## Harmless(Crows-Paris)

[14] Anthropic, "hh-rlhf Dataset" より引用

[15] Li, Junyi, et al. (2023), "HaluEval: A Large-Scale

Hallucination Evaluation Benchmark for Large

Language Models" より引用

[16] Nangia, Nikita, et al. (2020), "CrowS-Pairs: A

Challenge Dataset for Measuring Social Biases in

Masked Language Models" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 参考: その他の基準について

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs" より引用

## 25

## •

## LLMが潜在的に持っているリス

## クについて，3つのレベルの分

## 類で，合計60のリスクタイプに

## ついて定義

## •

## 情報の危険性，悪意のある使用，

## 差別・攻撃的な出力，誤った情報

## による害，チャットボットとの相互作

## 用による害．．など

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 人間がフィードバックを与えることの限界

26

## •

## タスクが複雑になるにつれ，人間が評価できなくなる

## •

## AIアシスタントの力を借りて人間単体では評価できなものを評価できるように

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: Superalignment

27

## • 今後どんどん賢いAI(AGI)ができた時に暴走しないように人間の意図通りに制

## 御できるのか？

## • 人間よりはるかに賢いAIシステムが人間の意図に従うようにするにはどうすれ

## ばいいのか？

[5] OpenAI (2023), "Introducing Superalignment" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: weak-to-strong generalization

28

## •

## 弱いLLMが強いLLMを監督する

[18] OpenAI (2023), "Weak-to-Strong Generalization" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: AGIとAlignmentの関係性

29

## •

## AGI(汎用人工知能)の実現が大規模言語モデルの登場によって現実的になっ

## てきており，Alignmentの研究が推進されている

## •

## AGIがAlignmentされていないと，人類に重大なリスクをもたらす可能性が

## ある(人類の絶滅，地球規模の大惨事)とOpenAIは主張

[19] Wikipedia, "Existential risk from artificial intelligence" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの全体像

30

## •

## RLHFの学習は以下の3つのステップで構成されている

## •

## プロンプトに対するStep1で学習

## させたモデルの回答を複数パター

## ン用意し、ラベラーにその中で良

## いものはどれかの順位付けをして

## もらう

## •

## 順位づけデータセットを用いて報

## 酬モデルを学習させる

## •

## Step1，Step2で学習されたモデル

## を用いて強化学習を行う

## •

## 報酬が最大となるような方策を探

## 索し，最適な回答を生成する

## ※ 方策はStep1で学習したモデル

## Step 3: 強化学習

## Step 2: 報酬モデルの学習

## Step 1: 教師あり学習

## •

## プロンプトとそれに対する適切な

## 回答のペアをラベラー(人間)が考

## 案し，データセットを作成する

## •

## このデータセットを用いて事前学

## 習モデルをfine-tuningする

## データセット

## 事前学習モデル

※ 報酬モデルには既存の事前学習モデルやfine-tuningされたモデルの最終層のみを線形層に変更したモデルが使用されることが多い

つまり．報酬モデルの出力はスカラー値となる

## 順位づけデータセット

## 報酬モデル

## モデルの回答に対して報酬値を推

## 定し，それをモデルにフィードバ

## ックすることで方策を改善

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 強化学習

31

## •

## 問題設定

## •

## エージェント(行動主体)は環境の状態に基づいて, 逐次的に行動を決定する

## •

## 強化学習の目的

## •

## 行動の結果得られる報酬を利用し, その環境で最も良い行動ルール(最適方策)

## を学習したい

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 強化学習の応用例

32

[20] CNET Japan (2018), "AI自動運転車、「強化学習」で運転方法を20分で習得" より引用

[21] CNET Japan (2017), "AI関連記事" より引用

[22] Boston Dynamics, "Boston Dynamics" より引用

[23] OpenAI, "ChatGPT" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 強化学習の最適化アルゴリズム: PPO(Actor-Critic）

33

## •

## RLHFでもよく使われている強化学習のアル

## ゴリズム

## •

## PPOはActor-Cliticと呼ばれるアルゴリズムの

## 派生系

## •

## エージェント内にActorとCriticという役割が

## 存在し，それらが協調することでポリシーを

## 更新し，報酬を最大化していく

[24] BrainPad Platinum Data Blog (2023), "ChatGPTの仕組みを論文ベースで超詳細に解説" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 強化学習の最適化アルゴリズム: PPO(方策勾配法）

34

## •

## 方策(Actor)や価値モデル(Critic)はパラメータを持ったニューラルネットで

## 表現できる

## •

## 方策勾配法: 𝜃でパラメータ化された方策を勾配を用いることで直接最適化を

## 行う手法

## 𝜃←𝜃+ 𝛼∇𝜃𝐽(𝜋𝜃)

## 𝐽𝜋𝜃= 𝑉𝜙𝑠0

## ∇𝐽𝜋𝜃= ෠𝐸𝑡∇𝜃log 𝜋𝜃𝑎𝑡𝑠𝑡

## መ𝐴𝑡(𝑠𝑡, 𝑎𝑡)

## 方策勾配定理

## 𝑉𝜙(𝑠𝑡)

## : 価値関数

## 𝜋𝜃𝑎𝑡𝑠𝑡

## : 方策

## መ𝐴𝑡

## : アドバンテージ関数

## 目的関数

[25] zero2one, "方策勾配法(Policy Gradient Methods)" より引用

## ※アドバンテージ関数መ𝐴𝑡: ある状態𝑠𝑡に対して行動𝑎𝑡がどれだけ価値があるかの推定値

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 強化学習の最適化アルゴリズム: PPO(詳細)

35

## •

## 強化学習における手法の一つであるTRPOをシンプルにした手法

## •

## TRPO: 方策勾配法による更新幅をKL距離という制約をかけて更新することで，方策が

## 劣化することを防ぐ

## •

## PPO: 更新幅をclipすることでTRPOの計算の複雑さを軽減

## •

## 価値モデル(Critic)は，報酬和とのMSE(平均二乗誤差)

## で学習

## •

## 価値モデル: ある状態の推定価値を算出するモデル

## 𝜖

## : clippingパラメータ

## 𝜋𝜃𝑎𝑡𝑠𝑡

## : 方策

## 𝜋𝜃𝑜𝑙𝑑(𝑎𝑡|𝑠𝑡) : 更新前の方策

## 𝑟𝑡(𝜃)

## : 報酬関数

## ෠𝑅𝑡

## : 期待報酬和

## መ𝐴𝑡

## : アドバンテージ関数

## 𝑉𝜙(𝑠𝑡) : 価値関数

## 𝐿𝑃𝑃𝑂𝜃= ෠𝐸𝑡[min 𝑟𝑡𝜃መ𝐴𝑡, 𝑐𝑙𝑖𝑝𝑟𝑡𝜃, 1 −𝜖, 1 + 𝜖

## 𝐿𝑐𝑟𝑖𝑡𝑖𝑐𝜙= ෠𝐸𝑡[ 𝑉𝜙𝑠𝑡−෠𝑅𝑡

## 2]

## 𝐿𝑇𝑅𝑃𝑂𝜃= ෠𝐸𝑡𝑟𝑡𝜃መ𝐴𝑡

## 𝑟𝑡𝜃=

## 𝜋𝜃𝑎𝑡𝑠𝑡)

## 𝜋𝑜𝑙𝑑(𝑎𝑡|𝑠𝑡)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 強化学習を学ぶための資料

36

## 英語

## •

## Reinforcement Learning Specialization — by Coursera

## •

## Reinforcement Learning Lecture Series 2021 — by DeepMind x UCL

## •

## Stanford CS234: Reinforcement Learning — Winter 2019

## •

## Introduction to Reinforcement Learning with David Silver

## •

## UC Berkeley CS 285: Deep Reinforcement Learning — Fall 2021

## •

## Deep RL BootCamp — UC Berkeley

## •

## Deep Reinforcement Learning Course by HuggingFace

## 日本語

## •

## 強化学習の基礎と深層強化学習（東京大学松尾研究室深層強化学習

## サマースクール講義資料

## •

## 強化学習（第2版）

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 人間のフィードバックによる強化学習

## 37

## • OpenAIが2017年に発表した少数の人間のフィードバックから強化学習する仕組み

## • ロボットシミュレータとAtariで学習し，サンプル効率が向上したことが確認された

## ※ 同年にPPOがOpenAIからpublishされた

## Step1:

## 方策が環境での報

## 酬を最大化するよ

## うに学習

## Step2:

## 出力行動から二つ

## を選択し，人間が

## 評価

## Step3:

## 人間の比較結果をもとに

## Reward Predictorを学習

[26] OpenAI (2017), "Learning from human preferences" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 人間のフィードバックによるロボットタスクの強化学習

## 38

## • 人間が左か右かどちらが，目標(この場合はバク転)に近いかを判定する

## • AIは，人間の選択を最もよく説明する報酬関数を見つけることで、フィードバック

## に近い動きを獲得していく

[26] OpenAI (2017), "Learning from human preferences" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 人間のフィードバックによる言語モデルの強化学習

## 39

## • GPT-3を用いて要約タスクに人間のフィードバックによる強化学習を適用

## • Step1: 複数のソースから要約をサンプリングし，人間がそのペアを評価

## • Step2: 要約ペアの選考順序のデータをもとに報酬モデルを学習

## • Step3: 報酬モデルの出力を報酬として強化学習を行う

## • Fine-tuningより大幅に上回り，人間が作成した参照要約より優れているという結果

[27] Stiennon, Nisan, et al. (2020), "Learning to Summarize from Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## InstructGPT

## 40

## • ChatGPTの前進であるInstructGPTで用いられている手法

## • 要約タスクではなく，既存のGPT-3をアライメントすることが目的

## • 一般にRLHFと言うとこの手法を指すことが多い

## (1) Supervised Fine Tuning

## (2) Train Reward Model

## (3) Reinforcement Learning

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## InstructGPTの詳細

## 41

## •

## Step1

## •

## プロンプトのデータセットを用意し，そのプロンプトに対する人間のlabelerの回

## 答を元に教師あり学習を行う

## •

## Step2

## •

## あるプロンプトに対する出力を複数集め，その出力に関する「好ましさ」を，人

## 間のlabelerがランクづけする

## •

## その後，ランク付きデータをもとに，報酬モデルを学習

## •

## Step3

## •

## あるプロンプトに対するGPTモデルの出力に対して，報酬モデルが報酬を生成

## し，PPOによる強化学習を行う

## •

## Step3の完了後，強化学習した新しいGPTモデルを使用してStep2~3を行うと

## いう手順を繰り返す

## •

## この手順で学習するベースのモデルは，今まで運用していたGPT-3の学習済みモ

## デル

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 報酬モデルの学習(概要)

## 42

## • Labelerがプロンプトの出力に対してランク付けを行い，そのデータから報酬モデル

## を学習する

## • K=4~9個の出力から2つの組について全てランクづけを行う(以下の例はK=4)

お金持ちになるには

どうすれば良いでし

ょうか？

いいですね！

人から盗めば良いです。

一生懸命働くと良いです。

一生懸命働き，そして空いている時間には

本を読んだり，資格の勉強をしたり，新し

い人と話したりすると良いでしょう

## プロンプト

## SFTモデルの回答

## 2つのペアをそれぞれ比較(4C2=6通り)

いいですね！

## VS

人から盗めば良いです。

いいですね！

## VS

一生懸命働くと良いです。

## VS

一生懸命働くと良いです。

一生懸命働き，そして空いている時

間には本を読んだり，資格の勉強を

したり，新しい人と話したりすると

良いでしょう

## VS

一生懸命働くと良いです。

人から盗めば良いです。

## …

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 報酬モデルの学習(数式)

## 43

## • 報酬モデルはプロンプト𝑥に対する出力𝑦を入力として，報酬を出力するモデル

## 𝑟𝜃(𝑥, 𝑦)と書ける

## • 報酬モデルは以下の損失関数を用いて学習する

## (𝑦𝑤が𝑦𝑙よりも良い回答, 𝑤: 𝑤𝑖𝑛, 𝑙: 𝑙𝑜𝑠𝑒)

## 𝑙𝑜𝑠𝑠𝜃= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## つまり，良い回答である(𝑥, 𝑦𝑤)のペアの報酬を，悪い方の回答である(𝑥, 𝑦𝑙)のペアの報

## 酬よりも高くなる確率を学習する

## 𝜃

## :報酬モデルのパラメータ

## 𝜎

## :シグモイド関数

## ※Bradley-Terryモデルに従うと仮定する

## 𝑝∗yw ≻yl

## x) =

## exp(𝑟∗𝑥, 𝑦𝑤)

## exp 𝑟∗𝑥, 𝑦𝑤

## + exp 𝑟∗𝑥, 𝑦𝑙

## = 𝜎(𝑟∗𝑥, 𝑦𝑤

## −𝑟∗𝑥, 𝑦𝑙)

## log 𝑝𝜃yw ≻yl x)

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human

Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 言語モデルにおける強化学習

## 44

## • 報酬関数を用いて，よりスコアが高い文章を生成できるように強化学習を行う

## • つまり，「どのような文章を生成するか」を強化学習で言う戦略(方策) とし、報酬

## モデルによる出力を最大化するように方策を学習していく

## では単純に目的関数は，得られる報酬の期待値を最大化するのみ？

## →そのままでは上手く学習できないので工夫が必要

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿[𝑟𝜃(𝑥, 𝑦)]

## 𝜙

## : 方策のパラメータ

## 𝜋𝜙

𝑅𝐿

## : 学習している方策

## 𝐷𝜋𝜙

𝑅𝐿

## : 現在の方策によって得られたデータ

## 期待累積されてない報酬

## (文脈付きバンディット)

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 言語モデルにおける強化学習での問題点

## 45

## 1.

## Reward Hacking

## 2.

## Alignment Tax

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 問題①: Reward Hacking

## 46

## 報酬を最大化することを目的にしたモデルが望ましくない方策を学習してしまうこと

## 対策: KL Penalty

## • 報酬がたくさんもらえるような決まった文章ばかりを生成しないようにする

## • 生成する文章がSFTモデルから大きく変わりすぎないようにする

[27] Stiennon, Nisan, et al. (2020), "Learning to

summarize from human feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 解決策①: KL Penalty

## 47

## • SFTモデルと学習中のモデルの分布が大きく変わらないようにする

## • 𝛽はどの程度KL Penaltyを考慮するかのハイパーパラメータ

## •

## 大きいと方策の学習は安定するが目的関数も大きくなりにくい

## •

## 小さいと目的関数は大きくなりやすいが方策が崩壊しやすくなる

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿𝑟𝜃𝑥, 𝑦

## −𝛽log

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## 𝜙

## : 方策のパラメータ

## 𝜋𝜙

𝑅𝐿

## : 学習している方策

## 𝜋𝑆𝐹𝑇

## : SFTモデルの方策

## KL Penalty

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 問題②: Alignment Tax(アライメント税)

## 48

## • 人間の意図通りに事前学習モデルを学習しようとすると，汎化性能が劣化してしま

## う

## = 事前知識の忘却が起こる

## 対策: Replay

## • 事前学習時のデータを用いて汎化性能の劣化を抑える

## [79] Peng, Baolin, et al. (2023), "Stabilizing RLHF through

## Advantage Model and Selective Rehearsal" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 解決策②: Replay

## 49

## • 事前学習時のデータ𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛を用いて，汎化性能を維持

## •

## 対数尤度を最大化することで，事前学習時の文章の忘却を防ぐ

## • 𝛾はどの程度Replayを考慮するかのハイパーパラメータ

## •

## 大きいと汎化性能は維持しやすいが，報酬をあまり考慮しない

## •

## 小さいと報酬をより重視するが，汎化性能が劣化しやすい

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒2 𝜙

## = 𝛾𝐸𝑥~𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛[log(𝜋𝜃

## 𝑅𝐿𝑥)]

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## • KL PenaltyとReplayの二つを組み合わせたものがPPO-ptx

## •

## GPT, SFTと比較して大きな性能改善

## •

## PPOと比較してもPPO-ptxは性能改善が見られる

## PPO-ptx

## 50

## 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒𝜙

## = 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒1 𝜙+ 𝑜𝑏𝑗𝑒𝑐𝑡𝑖𝑣𝑒2 𝜙

## = 𝐸𝑥,𝑦~𝐷𝜋𝜙

## 𝑅𝐿𝑟𝜃𝑥, 𝑦

## −𝛽log

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## + 𝛾𝐸𝑥~𝐷𝑝𝑟𝑒𝑡𝑟𝑎𝑖𝑛[log(𝜋𝜃

## 𝑅𝐿(𝑥)]

## KL Penalty

## Replay

[28] Ouyang, Long, et al. (2022), "Training Language Models to

Follow Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## • InstructGPTはGPT-3と比較して，より正しい指示に従い，ハルシネーション(幻覚)

## が抑えられている

## • ユーザーと同じ言語を用いる割合も高くなっている(Ex. 英語では英語で返す)

## InstructGPTの評価

## 51

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow

Instructions with Human Feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの発展的内容

52

## 1.

## DPOの基礎

## 2.

## DPOの派生手法について

## 3.

## その他のアライメント手法について

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPO | 報酬モデルを使用せずに直接ランキングを学習

## 53

## •

## Reward Modelを介さず直接Preferenceを考慮した最適化を行う

## •

## Reward Modelは暗黙的に定義

## 報酬モデル(Step 2) + 強化学習(Step 3)

## 教師あり学習のみ

## ＝

## 等価

## 報酬推定が間違えた分だけ重みづけ

## 𝝅(𝒚𝒘|𝒙)の尤度最大化

## 𝝅(𝒚𝒍|𝒙)の尤度最小化

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language

Model is Secretly a Reward Model" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOの理論| RLHF = DPO

## 54

## •

## 近似や仮定なしに数学的に等価であることが示されている(証明はAppendix)

## 𝐿𝑜𝑠𝑠𝐷𝑃𝑂𝜃

## = −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log 𝜎(𝛽log 𝜋𝜃𝑦𝑤𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑤𝑥−𝛽log 𝜋𝜃(𝑦𝑙|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦𝑙|𝑥))]

## 報酬モデル(Step 2) + 強化学習(Step 3)

## 教師あり学習のみ

## ＝

## 等価

## 𝐿𝑜𝑠𝑠𝑅𝑒𝑎𝑟𝑑𝜙= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎(𝑟𝜙𝑥, 𝑦𝑤

## −𝑟𝜙𝑥, 𝑦𝑙)]

## 𝐿𝑜𝑠𝑠𝑅𝐿𝜃

## = 𝐸𝑥,𝑦~𝐷𝜋𝜃

## 𝑅𝐿𝑟𝜙𝑥, 𝑦

## −𝛽log

## 𝜋𝜃

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## ＝

## DPO

## RLHF

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの発展的内容

55

## 1.

## DPOの基礎

## 2.

## DPOの派生手法について

## 3.

## その他のアライメント手法について

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## ΨPO / IPO | DPOの派生手法

## 56

## •

## DPOを一般化したものとして提案されたアルゴリズム

## •

## Ψ: 0,1 →ℝ+となる非減少関数を導入して以下の目的関数を最小化する

## •

## Ψを次ののように置くとDPOと同じ目的関数となる

## •

## また，Ψ = 𝑞という恒等関数を用いた場合をIPO(Identify Preference

## Optimization)として提案されている

[30] Azar, Mohammad Gheshlaghi, et al. (2023), "A General Theoretical Paradigm to

Understand Learning from Human Preferences" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## KTO | DPOの派生手法

## 57

## [31] Ethayarajh, Kawin, et al. (2024), "KTO: Model Alignment

## as Prospect Theoretic Optimization" より引用

## •

## プロスペクト理論に基づいて人間の効用モデルを方策の学習に組み込んだ手法

## •

## 例: 5万円得た喜びよりも5万円失った悲しみの方が大きい

## •

## (𝑥, 𝑦𝑤, 𝑦𝑙)のPreferenceデータが必要なく, 単一のペア(𝑥, 𝑦) のみから学習できる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOの派生手法は結局どれが良いのか？

## 58

## •

## DPO, ΨPO / IPO, KTOなどはデータセットと報酬関数に関する仮定を変更して

## いる手法

## •

## DPO, IPOなどはSFTなしでも高い性能を発揮している．

## •

## ただし，DPOが一番性能としては高いので，学習コストを抑えたい場合は，

## KTOやCPOを使用するのが良い

[32] Saeidi, Amir, Verma, Shivanshu, and Baral, Chitta (2024), “Insights into

Alignment: Evaluating DPO and its Variants Across Multiple Tasks“より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOとPPOはどちらが優れているのか？

## 59

[33] Ivison, Hamish, et al. (2024), “Unpacking DPO and PPO: Disentangling

Best Practices for Learning from Preference Feedback”より引用

## •

## 現状はDPOはPPOに勝てない

## •

## PPO > filtered DPO / iterative DPO > DPO > SFT

## •

## なぜなのか？

## •

## PPOを用いることでReward Modelの外挿のデータにアクセスできるため？

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reverse KLの問題点とは？

## 60

## 𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## •

## RLHFは出力の多様性が損なわれてしまう

## •

## その原因はexp(

## 1

## 𝛽𝑟(𝑥, 𝑦))のせい

## •

## 指数関数的にSFTの分布を尖らせてしまう

## •

## expを消すためにKL-divergenceの代わりにf-divergenceを用いる研究も存在

## ここが悪さをしている

[34] Wang et al. (2024), “Beyond Reverse KL: Generalizing Direct Preference Optimization with Diverse Divergence Constraints”,より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## その他の派生手法について

## 61

## •

## Iterative / Online DPO

## •

## Self-Rewarding

## •

## Token-level DPO

## •

## DPO: from r to Q

## •

## TDPO

## •

## Merge SFT

## •

## ORPO

## •

## Reference Free

## •

## SimPO

## •

## Negative Preference

## Optimization

## •

## NPO, CPO

## •

## Nash Learning

## •

## SPPO, DNO

[85] Zhichao Wang et al. (2024) "A Comprehensive Survey of LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの発展的内容

62

## 1.

## DPOの基礎

## 2.

## DPOの派生手法について

## 3.

## その他のアライメント手法について

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Stable Alignment | 人間社会をシミュレート

[35] Liu, et al.,(2024) “Training Socially Aligned Language Models in Simulated Human Society”より引用

## 63

## •

## 模擬的な人間社会をシミュレートするサンドボックスを作成

## •

## サンドボックス中のagent同士が対話することによって，質問に対する回答を様

## 々な観点で生成

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## AlpacaFarm | 人間の評価をシミュレート

[36] Dubois, Yann, et al. (2023), “ApacaFarm: A Simulation Framework

for Methods that Learn from Human Feedback”より引用

## 64

## •

## 「人間がどんな評価を返すのか」をシミュレートすることで安価＆高速にRLHF

## を進めることができるツール

## •

## 人間との評価は高い相関で一致しており，実際の人間に評価してもらう場合に

## 比べて1/45のコスト及び遥かに短い時間で同等の評価ができると主張

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 発展的手法の大別

65

## Human Feedback or AI Feedback

## •

## Human Feedback

## •

## RLHF, RAFT, RRHF

## •

## AI Feedback

## •

## RLCD, Stable Alignment, AlpacaFarm,

## RLAIF, Constitutional AI

## Ranking or Language

## •

## Rank-based Training

## •

## DPO, PRO, RRHF, SLiC

## •

## Language-based Training

## •

## CoH, Second Thoughts, Stable

## Alignment, SelFee

## RL or not RL

## •

## Using RL

## •

## RLHF, RLCD, RLAIF,

## •

## Not Using RL

## •

## DPO, IPO, KPO, CPO, PRO, RRHF, RAFT

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 目次

66

## • 人間のフィードバックからの強化学習について(RLHF/DPO)

## • 検証可能な報酬器からの強化学習について(RLVR)

## • LLMにおける強化学習のアプリケーション例

## • 今後の方向性について

## • まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルはすごい..が簡単な問題も間違えてしまうことがある

67

## •

## 博士課程レベルの知識を図る問題で人間超えのスコアを記録

## •

## 推論能力に関しても数学オリンピックの問題を解くことができる

## •

## 一方で簡単な計算問題を間違えてしまうことがある

## ⇩専門家の人間のスコア

## ←間違い

[37] epoch.ai, “GPQA Diamond Benchmark”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 二重過程理論(Dual Process Theory)

68

## •

## ノーベル経済学賞受賞者のダニエル・カーネマンとエイモス・トヴェルスキーによって広めら

## れた理論で、人間の思考は2つの異なるシステムによって動いていると仮定する

## •

## システム1: 直感やひらめきで、無意識的に判断する考え方

## •

## システム2: 数学や論理的思考などで、じっくりゆっくり考える考え方

## •

## LLMのアナロジーで考えると、システム1は得意でシステム2は苦手であるといえる

## •

## なぜLLMはシステム1的な思考は得意なのか？

## •

## なぜLLMは大規模に訓練されていてもシステム2的思考が苦手なのか？

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLMは補完的なデータベースである

69

## •

## システム1的思考は、過去の経験や知識に

## 基づくパターンマッチングであり、関連する知

## 識の集合を迅速に補間するプロセスである。

## •

## 事前学習されたLLMは、このような動作を示

## しており、補間型データベース

## （interpolative database）のように

## 振る舞う

## •

## 実際は、LLMは単なる事実の記憶以上のこ

## とを行っている。なぜなら、訓練時に類似のタ

## スクを経験していれば、新しい未知のタスク

## を解くことができるからである。したがって、

## LLMは純粋なデータベースではない。

[38] Chollet, François (2023),

ARC Prize関連ポストより引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## ヒューリスティックの積み重ねによる思考

70

## •

## LLMは多くのヒューリスティック（経験則）を学習しており、それらは統計的な相関関係

## は持つが、根本的な因果構造を学習しているわけではない

## •

## つまり、LLMは多くの経験則組み合わせて動作していると考えられる。

## [39] Nikankin, A.et al. (2025), “Arithmetic without algorithms: Language models solve math with a bag of heuristics”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 事前学習によるスケーリング則の時代は終わった？

71

## •

## 計算能力は向上するがデータは枯渇していく(化石燃料のように)

## •

## GPT-4.5はモデルを大きくしたにも関わらず大きな性能向上に至らなかった

## •

## 実際OpenAIの多くの研究者達は新たなステップが必要と述べている

## •

## RL, Test Time Scalingにつながる

[41] OpenAI (2025), “GPT-4.5 System Card” より引用

[40] Sutskever, Ilya (2024), “Sequence to Sequence Learning with Neural

Networks at NeurIPS 2024”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 推論スケーリングの成功

72

## •

## 非常に長いChain-of-Thoughを行うように強化学習することによって、OpenAI o1や

## DeepSeek R1は推論時に深く考えれば考えるほど性能向上に寄与するようになった

## →LLMがシステム2的思考を手にいれることができ、推論スケーリング時代のきっかけとなる

[43] DeepSeek-AI, Guo, Daya, et al. (2025), “DeepSeek-R1: Incentivizing Reasoning

Capability in LLMs via Reinforcement Learning”

より引用

[42] OpenAI (2024),

“Learning to Reason with LLMs” より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## これからは経験の時代

73

## •

## 近年のAIが「ヒューマンデータの

## 時代」にあった。

## •

## LLMのように人間の膨大のデー

## タを学習することで、性能を向

## 上させてきたが、「人間を超え

## る」超人的な知能に到達するこ

## とは難しい

## •

## この限界を突破するために、「経

## 験の時代」への転換が必要であ

## る

## •

## つまり、AI自身が試行錯誤し

## て、その結果から学ぶ必要があ

## る

## →その一つの方法が強化学習

## [44] Silver, David and Sutton, Richard (2025),

## “Welcome to the Era of Experience“より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRの概要

74

## •

## 検証可能な報酬モデルを用いて強化学習を行う

## •

## ex. 数学であれば最後の出力が合っているか, コードなら実行結果が合うか，テストが通

## るかなど

## •

## RLHFの場合は報酬モデルを学習させる必要であったが、RLVRでは不要

## Ways to compute rewards

## ●

## Math-Verify (https://github.com/huggingface/Math-

Verify)

## ●

## LLM-as-a-judge for facts

## ●

## Code Sandboxes

## ●

## More!

[9] Lambert, Nathan, et al., “RLHF Book Chapter 14: Reasoning”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DeepSeek R1の成功

75

## •

## o1の成功後、オープンソースで再現する動きが多く現れたが、DeepSeek R1はオープン

## ソースで初めてo1に迫る性能を叩き出した

## •

## GRPOと呼ばれる独自の強化学習アルゴリズムを提案し、性能向上に寄与した．

[43] DeepSeek-AI, Guo, Daya, et al. (2025), “DeepSeek-R1: Incentivizing Reasoning Capability in

LLMs via Reinforcement Learning”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## GRPO：概要

76

## •

## PPOを推論向上に特化させた強化学習手法

## •

## アドバンテージ（A）をエピソード報酬（r）から直接算出することにより状態価値V(s)

## の関数近似を不要とした

[45] Shao, Zhihong, et al. (2024),“DeepSeekMath: Pushing the Limits of

Mathematical Reasoning in Open Language Models“より引用

[46] oxen.ai (2024), “Why GRPO is Important and How it Works”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

Lambert |

Experimenting with

this new RL  77

## 価値関数を学習する代わりに、同じプロンプトに対する複数の応答の統計を使用してベー

## スラインを計算する

## Clipping logic for conservative step size (from PPO)

## KL penalty in loss

## rather than reward

## Sample many answers, o, to questions, q,

## assign rewards relative to group rewards r_i

## Token length

## normalization

[45] Shao, Zhihong, et al. (2024),“DeepSeekMath: Pushing the Limits of

Mathematical Reasoning in Open Language Models“より引用

## GRPO：数式

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLMの「アハ体験」

78

## •

## RLVRによって，自分の試行錯誤の結果が間違っていた時に”Wait, wait. That’s

## an aha moment”と言って正しい解き方に気づくことがある

[43] DeepSeek-AI, Guo, Daya, et al. (2025), “DeepSeek-R1: Incentivizing

Reasoning Capability in LLMs via Reinforcement Learning”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRによっていくつかの認知行動が誘発される

79

## •

## 強化学習によって，Verification, Backtrackの行動が増加し、それに伴ってスコアも

## 向上する

## •

## 一方でRL前のモデルでこの二つの行動が全く見られない場合はRLしても性能が向上し

## ない

[47] Gandhi et al. (2025), "Cognitive Behaviors that Enable Self-Improving Reasoners,

or, Four Habits of Highly Effective STaRs"

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## GRPOの問題点

80

## Length normalization bias

## Question-level difficulty bias

## •

## トークン長で正規化されているので，長

## さを長くする方がペナルティを受けにくくな

## る

## •

## そのため学習が進むと生成長が長くなる

[48] Liu, Zichen, et al. (2025),“Understanding R1-Zero-like Training: A Critical

Perspective”より引用

## •

## アドバンテージを計算する時に，標準

## 偏差で割るので，極端に難易度が低

## い/高い問題の時，より高い重みを与え

## られる傾向がある

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## GPROの発展版: Dr. GRPO

Lambert |

Experimenting with

this new RL  81

## •

## 長さで正規化せずトークン損失を合計して最後にグループ数だけで平均することで、長さ

## に対するバイアスを減らす

## •

## より短い長さで高いスコアを達成

[48] Liu, Zichen, et al. (2025),“Understanding R1-Zero-like Training: A Critical

Perspective”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## GRPOの発展版: DAPO

Lambert |

Experimenting with

this new RL  82

## •

## DAPOは、GRPOを改良して動的サンプリングと拡張クリッピングにより探索性と安定性を

## 高めた

[49] Yu, Qiying, et al. (2025),“DAPO: An Open-Source LLM Reinforcement Learning

System at Scale”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLにおける長さバイアス

Lambert |

Experimenting with

this new RL  83

## 長さの正規化方法で短文/長文の有利さと勾配分散が変わり、左ほど安定だが偏りが大

## きく、右ほど偏りがないが不安定になる

## Default GRPO

## Per sequence length

## normalization.

## Learning slightly

## biased in every

## completion.

## Dr. GRPO*

## No length normalization

## per sequence.

## Unbiased across

## sequences and groups

## (questions).

## DAPO

## Normalize by total

## number of tokens

## across question.

## Per-question bias as

## weight is different.

## More biased,

## likely lower

## gradient

## variance

## Theoretical

## solution, will

## it translate to

## practice?

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## SFTは記憶してRLは汎化を促す

84

## •

## シンプルなトイタスクで

## SFTとRLを比較

## •

## 分布内のデータだと

## SFTが強く，分布外

## のデータだとRLの方が

## 性能が良い

## •

## つまり，SFTは記憶,

## RLは汎化能力を促し

## ていることが示唆され

## る

[50] Chu, T., et al. (2025),“SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model

Post-Training”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRによって新しい思考は獲得されるか？

85

## •

## RLVRによって新しい思考パターンが得られているわけではなく，事前学習

## 済みモデルに存在する思考パターンを強化している可能性

## •

## 一つの問題に対するサンプル数を増やすとpass@kの指標は事前学習済みモ

## デルに近づいていく

[51] Yue, Y., et al. (2025),“Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs

Beyond the Base Model?”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRによって新しい思考は獲得されるか？

86

## •

## 一方で，Prolonged RL（ProRL）という手法を用いることで，「エントロピ

## ー崩壊」を防ぎ，RLがベースモデルでは到達できない新しい推論戦略を学習

## できると主張している．

## •

## エントロピー崩壊:モデルの出力分布が学習の初期段階で多様性を失い、エントロピーが

## 急激に低下する現象

## •

## この状態になると出力の多様性が失われ，探索が停滞する

[52] Liu, M., et al. (2025),“ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 多様性を維持したまま強化学習: Pass@K Training

87

## •

## Pass@Kを最適化するように強化学習を行

## うことで学習中の探索が促され，ベースモ

## デルにはなかった推論戦略を獲得できる

## •

## エントロピー崩壊を防ぐことができ，さら

## に，Pass@1の性能も向上する

## SimKO: Simple Pass@K Policy Optimization}

[53]Ruotian Peng et al.(2025), “SimKO: Simple Pass@K Policy Optimization”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 1つのサンプルのみから強化学習

88

## •

## たった1つのトレーニングサンプルを用いた場合でもデータセット全体を用

## いた場合と同程度の性能を達成

[54] Wang, Y., et al. (2025), “Reinforcement learning for reasoning in large language models with one training example”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLVRにおける今後の課題

89

## •

## 汎化させるにはSFTが良い？RLが良い？もしくは両方？

## •

## SFTでは学習データに推論パターンを記憶してしまう一方で，RLはベースモデルの思考パターンを強化しているだ

## けとも解釈できる

## •

## SFTで新たな思考パターンを学習させてRLでそれらを強化する？

## •

## 継続的に新しい思考パターンを学習できるような手法が理想

## •

## 事前学習モデルは何を使用すれば良い？

## •

## Qwen FamilyではRLにより飛躍的な精度向上が見られているが，Llama FamilyだとQwenよりは精度が向

## 上しない

## •

## 事前学習モデルの分布によって，RLの効果が変わってしまう

## •

## 報酬は結果に対してだけ与えれば良い？中間結果に対しても与えた方が良い？

## •

## 最終結果のみに報酬を与えているが，本来は途中過程にも報酬を与えた方が効率が良い

## •

## しかし，現状それらの手法は最終結果のみに報酬を与える場合と比較して悪くなっている

## •

## 検証不可能なタスクにおける推論はどうすれば良い？

## •

## 数学，コードなど最終結果をルールベースで判定できるタスクばかりではない

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 目次

90

## • 人間のフィードバックからの強化学習について(RLHF/DPO)

## • 検証可能な報酬器からの強化学習について(RLVR)

## • LLMにおける強化学習のアプリケーション例

## • 今後の方向性

## • まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## マルチモーダルタスク

91

## •

## 言語だけでなく，画像や動画を入力として推論を行うモデルも登場している．

## •

## また，3Dシーンの理解の向上のために強化学習を用いてるケースも存在している

[55]Huang Ting et al. (2025), ”3D-R1: Enhancing Reasoning in 3D VLMs for Unified Scene Understanding”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## エージェントタスク

92

## •

## Web ページ操作を行うWebAgent やGUI 自体を操作するGUI-Agent に対して

## 強化学習を導入することで、タスクの成功率が高まることが確認されている

## •

## OSそのものの操作を強化学習を用いて学習する研究も存在する

[56] GUI-R1 (2025), ”GUI-R1 : A Generalist R1-Style Vision-Language Action Model For GUI Agents”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## ロボットタスク

93

## •

## VLA(Vision-Language-Action Model)を強化学習することによって長期タスクの性

## 能が飛躍的に向上した

## •

## また，RLによってSFT Modelで見られなかった新しい行動が学習された

[57] Li et al. (2025), ”SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 目次

94

## • 人間のフィードバックからの強化学習について(RLHF/DPO)

## • 検証可能な報酬器からの強化学習について(RLVR)

## • LLMにおける強化学習のアプリケーション例

## • 今後の方向性

## • まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 効率的な推論を行う

95

## •

## 強化学習によって生成長が長くなり，簡単な問題であっても長く考えてしま

## う問題がある．また，考えすぎることによって間違えてしまうoverthinkが発

## 生する．

## •

## 本来はタスクの難易度に応じて考える長さを制御することで効率的な推論を

## 実現して欲しい

[58]Feng et al. (2025), “Efficient Reasoning Models: A Survey”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 潜在空間上での推論

96

## •

## 思考過程を明示的にトークン化しながら推論するのは非常に効率が悪い

## •

## 人間で言えば，毎回喋りながら考えている

## •

## 潜在空間上で推論することで抽象的な事象を効率的に計算することができる

[59]Zhu et al. (2025),“A Survey on Latent Reasoning”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 事前学習から強化学習を行う

97

## •

## 今までの事前学習では，大規模なデータとNext Token Predictionに依存して

## おり，膨大なデータが必要かつ教師データ以上の性能を出すことはできな

## い．

## •

## そこで事前学習からRLを行うことで効率的に学習しつつ，データ以上の性能

## を出すことができるのではないか

[60]Dong et al. (2025),”Reinforcement Pre-Training”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 目次

98

## • 人間のフィードバックからの強化学習について(RLHF/DPO)

## • 検証可能な報酬器からの強化学習について(RLVR)

## • LLMにおける強化学習のアプリケーション例

## • 今後の方向性

## • まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## まとめ

99

## •

## RLHFはAlignment(人間の意図通りにモデルを学習)を適用する1つの方法で

## あり，人間からのフィードバックデータを用いて言語モデルを強化学習す

## る．

## •

## DPOは，教師あり学習を用いてAlignmentを適用する手法であり、RLHFと

## 数学的に等価である

## •

## RLVRは、検証可能な報酬を用いて推論能力を向上させる方法であり、

## GRPO, DAPO, Dr. GRPOなどの種類がある

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Appendix

## 100

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## データの集め方: InstructGPT

[28] Ouyang, Long, et al. (2022), "Training Language Models to

Follow Instructions with Human Feedback" より引用

## 101

## •

## Labelerの選択

## •

## 少数のデータにラベル付けを行い，スクリーニングテストの結果，ラベルとの一致度合いが

## 高いLabelerを選択

## •

## Labelerの属性に関する統計データをアンケートを用いて収集

## •

## Labelerの属性が偏らないようにする

## •

## Labelerへのinstructionを作成

## •

## Web GUIを用いてラベリング

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFを実装するためのライブラリ

102

## trl

## •

## HuggingFaceでPPO を使用して事前学習済みの言語モデルをRLHFするためのライブラ

## リ

## trlx

## •

## CarperAIによって構築されたtrlの拡張フォークで，オンラインおよびオフラインの学習

## 用の大規模なモデルを処理．現時点では，PPOとILQLを使用可能

## RL4ML

## •

## さまざまな強化学習アルゴリズム(PPO、NLPO、A2C、およびTRPO)，報酬関数，メ

## トリックを使用して，LLMのRLHFおよび評価が可能

## DeepSpeed Chat

## •

## Chat形式のモデルを学習できるツールキット

## •

## GPU1台で100億超パラメータを、複数GPUなら1000億パラメータ超のモデルを学習可

## 能

## •

## SoTAの15倍以上の高速な学習をスクリプト一つで実行でき，簡単かつ低コスト

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの評価につい

[6] Zhao, Wayne Xin, et al. (2023), "A Survey

of Large Language Models" より引用

## 103

## •

## 一般的な評価基準

## •

## Honestness

## •

## Helpfulness

## •

## Harmlessness

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの評価について: Honestness

104

## •

## TruthfulQA: 真実性を評価するベンチマーク

## •

## 健康、法律、金融、政治など38 のカテゴリーにわたる817 の質問と回答で構成

## •

## Fine-TuningされたGPT-3を用いて評価を自動化

## •

## HaluEval: ハルシネーションを認識できるかを評価するベンチマーク

## •

## ChatGPTが幻覚を起こしやすいデータで構成

## •

## Yes or Noであったり，回答が一致するかを判定する

[80] Stephanie Lin et al. (2022) "TruthfulQA: Measuring How Models Mimic Human Falsehoods"より引用

[81] Junyi Li et al. (2023) "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models"より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの評価について: Helpfulness

105

## •

## HH-RLHF: HelpfulnessとHarmlessnessに関するデータセット

## •

## Anthoropicが開発し，学習にも評価にもよく使用される

## •

## クラウドワーカによって収集

[82] Yuntao Bai et al. (2022) "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback"

arXiv:2204.05862 （Anthropic HH-RLHF Dataset）より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの評価について: Harmlessness

106

## •

## Crows-Pairs

## •

## 人種/肌の色、性別/性自認、性的指向、宗教、年齢、国籍、障害、外見、社会経済的地

## 位の9 種類の偏見に関する評価データセット

## •

## WinoGender

## •

## ジェンダーバイアスに関する評価データセット

[83] Nikita Nangia et al. (2020) "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models" より引用

[84] Rudinger, Rachel, et al. (2018), "Gender Bias in Coreference Resolution"より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## FLASK: Open-setなベンチマークでの包括的な評価

[61] Ye Seonghyeon et al. (2023), “FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets”より引用

## 107

## •

## Logical Thinking, Background Knowledge, Problem Handling, User

## Aligmentの４つの観点で合計12のスキルを評価

## •

## GPT-4を用いてそれぞれの観点で5段階の評価を行う

## •

## 左: FLASK dataset, 右: FLASK-HARD dataset

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## FLASK: Open-setなベンチマークでの包括的な評価

## 108

## •

## 人間ベースの評価(左)とGPT-4ベースの評価（右)は同様の傾向を示す

[61] Ye Seonghyeon et al. (2023), “FLASK: Fine-grained Language Model Evaluation

based on Alignment Skill Sets”より引用

[61] Ye Seonghyeon et al. (2023), “FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 参考: LLMのリスク評価のための包括的なデータセット

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A

Dataset for Evaluating Safeguards in LLMs" より引用

## 109

## •

## 各タイプごとに50個以上のプロン

## プトを作成し，合計939 個のプロ

## ンプトからなるリスク検出データ

## •

## 人間or GPT-4によって，各カテゴ

## リに該当するかを0,1で判定

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RewardBench: 報酬モデルの評価

## 110

## •

## 報酬モデルが正しく学習されているかを包括的に評価するためのベンチマーク

## •

## リーダーボードも公開されている

[62]Lambert Nathan et al. (2024), “RewardBench: Evaluating Reward Models for Language Modeling”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHF=DPOの証明

## 111

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOの理論| DPOとRLHFは等価なのか？

## 112

## max

## 𝜋

## 𝐸𝑥,𝑦~𝐷𝜋𝑟𝑥, 𝑦

## −𝛽𝐷𝐾𝐿[𝜋𝑦𝑥||𝜋𝑆𝐹𝑇𝑦𝑥]

## •

## RLHFの目的関数は以下で示される

## •

## 真の報酬を近似するためにBradley Terryモデルを用いて報酬モデルを学習

## していた

## この問題の最適解は解析的

## に解くことができる！

## 𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## ※ 𝑍𝑥は正規化のための分配関数

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: DPOとRLHFは等価なのか？

## 113

## •

## 最適方策を導出する過程の詳細

## •

## 簡単な式変形で導出できる

## •

## 前ページの𝜋𝑆𝐹𝑇𝑦𝑥が𝜋𝑟𝑒𝑓𝑦𝑥にあたる

## −𝜷で割って

## 最小化問題に

𝟏

## 𝜷𝒓(𝒙, 𝒚)を

## logの中に

## まとめる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOの理論| Your Language Model is Secretly a Reward Model

## 114

## •

## つまり，報酬𝑟(𝑥, 𝑦) が求まれば最適な方策𝜋∗𝑦𝑥が求まり，方策𝜋𝑦𝑥が求

## まれば，報酬𝑟(𝑥, 𝑦) が求まる

## •

## 𝜋𝑦𝑥と𝑟(𝑥, 𝑦) が対の関係になっている

## 𝜋∗𝑦𝑥=

## 1

## 𝑍(𝑥) 𝜋𝑆𝐹𝑇𝑦𝑥exp( 1

## 𝛽𝑟(𝑥, 𝑦))

## 𝑟𝑥, 𝑦= 𝛽log

## 𝜋(𝑦|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦|𝑥) + 𝛽log 𝑍(𝑥)

## ※ 𝑍𝑥は正規化のための分配関数

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 報酬モデルの学習(数式)

## 115

## • 報酬モデルはプロンプト𝑥に対する出力𝑦を入力として，報酬を出力するモデル

## 𝑟𝜃(𝑥, 𝑦)と書ける

## • 報酬モデルは以下の損失関数を用いて学習する

## (𝑦𝑤が𝑦𝑙よりも良い回答, 𝑤: 𝑤𝑖𝑛, 𝑙: 𝑙𝑜𝑠𝑒)

## 𝑙𝑜𝑠𝑠𝜃= −

## 1

## 𝐾

## 2

## 𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## つまり，良い回答である(𝑥, 𝑦𝑤)のペアの報酬を，悪い方の回答である(𝑥, 𝑦𝑙)のペアの報

## 酬よりも高くなる確率を学習する

## 𝜃

## :報酬モデルのパラメータ

## 𝜎

## :シグモイド関数

## ※Bradley-Terryモデルに従うと仮定する

## 𝑝∗yw ≻yl

## x) =

## exp(𝑟∗𝑥, 𝑦𝑤)

## exp 𝑟∗𝑥, 𝑦𝑤

## + exp 𝑟∗𝑥, 𝑦𝑙

## = 𝜎(𝑟∗𝑥, 𝑦𝑤

## −𝑟∗𝑥, 𝑦𝑙)

## log 𝑝𝜃yw ≻yl x)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## DPOの理論| RLHF = DPOの証明

## 116

## •

## よって，最適方策を学習するためには，Preference Dataに合うように報酬モデ

## ルを学習(=方策を学習)すれば良い

## 𝑟𝜃𝑥, 𝑦= 𝛽log

## 𝜋𝜃(𝑦|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦|𝑥) + 𝛽log 𝑍(𝑥)

## ※ 𝑍𝑥は正規化のための分配関数

## 𝑍𝑥= Σ𝑦𝜋𝑆𝐹𝑇𝑦𝑥exp(

## 1

## 𝛽𝑟(𝑥, 𝑦))

## 𝑙𝑜𝑠𝑠𝜃= −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log(𝜎𝑟𝜃𝑥, 𝑦𝑤

## −𝑟𝜃𝑥, 𝑦𝑙

## ))]

## = −𝐸𝑥,𝑦𝑤,𝑦𝑙~𝐷[log 𝜎(𝛽log

## 𝜋𝜃𝑦𝑤𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑤𝑥−𝛽log

## 𝜋𝜃(𝑦𝑙|𝑥)

## 𝜋𝑆𝐹𝑇(𝑦𝑙|𝑥))]

## 代入すると分配関数が

## 消えた！

## 普通はこれは計算できない→

## 全てのyに対して

## 総和を取るのは不可能

𝒓𝜽𝒙, 𝒚= 𝜷𝐥𝐨𝐠𝝅𝜽(𝒚|𝒙)

𝝅𝑺𝑭𝑻(𝒚|𝒙) とみなしているとも解釈できる

## 𝒍𝒐𝒈𝒑𝜽𝐲𝐰≻𝐲𝐥𝐱)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFの課題について

## 117

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLHFにおける課題| 全体像

[63] Casper Stephen et al. (2023), “Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback”より引用

## 118

## •

## Human Feedback, Reward Model, Policyのそれぞれ部分で課題がいくつか存

## 在する

## •

## Reward Model, Policyの学習どちらにも共通する課題も存在

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackにおける課題

## 119

## •

## Misaligned Evaluators

## •

## 質が高いフィードバックを提供するLabelerを選択するのが難

## しい

## •

## 評価者の中には有害な偏見や意見を持っている

## •

## ある人間が意図してデータを汚染する可能性

## •

## Difficulty of Oversight

## •

## 人間は単純な間違いを犯す

## •

## 人間は難しいタスクのパフォーマンスを適切に評価できない

## •

## Data Quality

## •

## データ収集のバイアスが生じる

## •

## コストと品質のトレードオフが存在する

## •

## Feedback Type Limitations

## •

## フィードバックの種類と効率さのトレードオフ

## •

## Ex. 2つのペアのrankingは簡単だが効率が悪い

## [63] Casper Stephen et al. (2023), “Open Problems

## and Fundamental Limitations of Reinforcement Learning

## from Human Feedback”より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackにおける課題| Misaligned Evaluators

## [64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply

## Annotated? Active Learning When Annotators May Disagree" より引用

## 120

## •

## RLHFによって訓練されたモデルは誰の意見を反映しているか？

## •

## RLHF前は低所得，低学歴と一致する意見であったが，RLHF後は逆になった

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackにおける課題| Difficulty of Oversight

## [65] Veselovsky, Veniamin, et al. (2023), "Artificial Artificial Artificial

## Intelligence: Crowd Workers Widely Use Large Language Models for Text

## Production Tasks" より引用

## 121

## •

## クラウドワーカーがLLMを使用することに経済的合理性がある

## •

## 自分で考えるよりLLMに考えて貰えばAPI代はらってもプラス

## •

## クラウドワーカーの33 ～46% がLLM を使用したと推定された

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackにおける課題| Data Quality

## [66] Zhou, Chunting, et al. (2023), "LIMA: Less Is More for Alignment" より引用

## 122

## •

## モデルの知識と能力はほとんどが事前学習時に学習されるという仮定

## •

## アライメントは対話形式のフォーマットと，言語モデルのどのドメイン分布か

## ら出力させるかを指定する

## •

## 質の良いデータを少量でも良いので集める必要がある

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackにおける課題| Feedback Type Limitations

## [67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on

## Integrating (Human) Feedback for Natural Language Generation" より引用

## 123

## •

## フィードバックの種類と効率さのトレードオフ

## •

## 2つのペアのrankingは簡単だが効率が悪い

## •

## 一方で，言語フィードバックだと質の担保が大変

## •

## そもそも人間の認知の限界としてランキングが一番効率が良い？

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reward Modelにおける課題

[63] Casper Stephen, et al. (2023), “Open Problems and Fundamental

Limitations of Reinforcement Learning from Human Feedback”より引用

## 124

## •

## Problem Misspecification

## •

## 個々の人間の価値観を報酬関数で表すのは難しい

## •

## 単一の報酬関数で人間の多様な社会を表すことはできない

## •

## Misgeneralization/Hacking

## •

## 正しいラベルのトレーニングデータからでも正しく報酬モデ

## ルが学習できるとは限らない

## •

## 報酬ハッキングが起きる可能性がある

## •

## Evaluation Difficulty

## •

## 報酬モデルを評価することは難しい

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reward Modelにおける課題| Problem Misspecification

## [64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply

## Annotated? Active Learning When Annotators May Disagree" より引用

## 125

## • 複数の意見がある問題に対して単一のスコアをつけることは難しい

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reward Modelにおける課題| Misgeneralization/Hacking

## [68] Gao, Leo, et al. (2022), "Scaling Laws for Reward Model Overoptimization" より引用

## 126

## •

## Reward Modelが過剰適合を起こすとMisgeneralization/Hackingが起きやすい

## •

## Reward Modelに関するスケーリング則(どのサイズだと過剰適合がおこるか)

## •

## 図はPolicyは1.3Bで固定,左:上位N個の出力を使用,右:すべての出力を使用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Policyにおける課題

## [63] Casper Stephen, et al. (2023), “Open Problems

## and Fundamental Limitations of Reinforcement Learning

## from Human Feedback”より引用

## 127

## •

## RL Difficulties

## •

## ポリシーを効果的に最適化することは困難

## •

## ポリシーは敵対的に悪用される可能性がある

## •

## Policy Misgeneralization

## •

## 最適なRLエージェントは，権力を求める傾向がある

## •

## Distributional Challenges

## •

## RLによってモード崩壊を起こす可能性がある

## •

## 事前モデルのバイアスが強化される可能性がある

## ※ モード崩壊: 多様性が失われて，類似した結果しか出力されなくなること

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Policyにおける課題| Robust RL Difficulties

## [69] Wei, Alexander, et al. (2023), "Jailbroken: How Does LLM Safety Training Fail?" より引用

## 128

## •

## ポリシーを敵対的に利用して，Jailbreakを引き起こすことが可能

## •

## 有名な例: GPT4へのDAN attack

## •

## モデルの安全規則・制限を無視させるテキストプロンプト

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Policyにおける課題| Distributional Challenges

## [70] OpenAI (2023), "GPT-4 Technical Report" より引用

## 129

## •

## RLHFによって，生成されるデータの多様性が失われる(モード崩壊)

## •

## GPT-4の場合はRLHF後だと自信を持って間違える場合が多くなる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reward Model & Policyにおける課題

## [63] Casper, Stephen, et al. (2023), "Open Problems and Fundamental Limitations

## of Reinforcement Learning from Human Feedback" より引用

## 130

## •

## 報酬モデルとポリシーを同時に学習することで，データの分布の変化を引き起こす

## •

## オンライン学習: 報酬モデルの分布がポリシーに影響を与え，ポリシーの出力が報酬モデ

## ルに影響

## •

## オフライン学習: 報酬モデルのバイアスにより誤った一般化に陥る可能性がある

## •

## 報酬モデルとポリシーの更新のバランス

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Human Feedbackによる対策| より詳細なフィードバック

## [71] Wu, Zeqiu, et al. (2023), "Fine-Grained Human Feedback Gives Better

## Rewards for Language Model Training" より引用

## 131

## •

## より詳細な報酬設計を行う

## (左: 通常のRLHF，右: 提案

## 手法)

## •

## (1) 各文章ごとに報酬を推定

## •

## (2) 3つの報酬モデルを学習

## し，それぞれのモデルごとに

## スコアを算出(事実の不正確

## さ、関連性のなさ、情報の不

## 完全さ)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reward Modelによる対策| 多様性の確保

## [72] Rame, Alexandre, et al. (2023),

## "Rewarded soups: towards Pareto-optimal

## alignment by interpolating weights fine-

## tuned on diverse rewards" より引用

## 132

## •

## 複数の観点で学習されたReward Modelのパラメータを混ぜる(Model Soup)

## ことによって，パレート最適なalignmentを目指す

## •

## Model Soup: 異なるハイパーパラメータで学習された複数のファインチュー

## ニングモデルの「重み」を平均化することで、精度を向上させる手法

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Policyによる対策| 複数のモデルを用いてRLの不安定さを解消

## [73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human

## Feedback without tears" より引用

## 133

## •

## 複数のモデルの出力でランク付けし，一番報酬が高い入出力ペアでSFTし，その他のペア

## に関しては出力しにくくしするように損失関数を設定

## •

## PPOをよりシンプルにした手法

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: Reverse KL vs Forward KL

## 134

## 𝐷𝐾𝐿𝜋𝜙

## 𝑅𝐿𝑦𝑥

## 𝜋𝑆𝐹𝑇𝑦𝑥

## 𝐷𝐾𝐿𝜋𝑆𝐹𝑇𝑦𝑥

## 𝜋𝜙

## 𝑅𝐿𝑦𝑥

## Forward KL

## Reverse KL

## • Forward KLだと元の分布全体をカバーするように学習されてしまう

## • Reverse KLだと特定のモードをカバーするように学習する

## →RLHFではは元の分布から大きく変わって欲しくないためこちらを採用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: 強化学習における工夫について

## 135

## • PPO-ptxによる強化学習で十分学習できるか？→そんなことはない

## • RLは基本的には学習が不安定であり，細かい実装のテクニックが必要であったり，

## ハイパーパラメータの細かい調整が必要となる

## [74] Irpan, Alex (2018), "Deep Reinforcement Learning Doesn't Work Yet" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足: PPO-max

[75] Zheng, Rui, et al. (2023),

"Secrets of RLHF in Large Language

Models Part I: PPO" より引用

## 136

## •

## 強化学習の学習安定化のための様々なテクニックを追加した方法(詳細は割愛)

## •

## Clipping, Initialization, GAE, … etx

## Policy Constraints

## Score

## Reparameterization

## Pretrained Initialization

## Others

## ※星がついている手法をPPO-Maxでは採用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 補足| PPO-maxの結果

## [75] Zheng, Rui, et al. (2023), "Secrets of RLHF in Large

## Language Models Part I: PPO" より引用

## 137

## • PPO-maxによって長期的に安定した学習を実現(左)

## • SFTモデルと比較した時の人間の評価(右)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RAFT | データのフィルタリングによるアライメント

## [76] Dong, Hanze, et al. (2023), "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment" より引用

## 138

## •

## 報酬モデルの上位100/k%をfine-tuningするデータとしてフィルタリング

## •

## PPOを使用することなく，同等以上の性能

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RLCD | コンテキスト蒸留を利用したAI Feedback

## [77] Yang, Kevin, et al. (2023), "RLCD: Reinforcement Learning from Contrast Distillation for Language Model Alignment" より引用

## 139

## •

## 有害，無害であるか等をプロンプトに埋め込み，生成された文に対して自動的

## に報酬を割り当てることで，AI Feedbackによってデータを作成

## •

## 実際にSFT, PPOする時は，有害，無害を指定するプロンプトは削除する

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## RRHF | 複数のモデルの応答をランク付け

## [73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human Feedback without tears" より引用

## 140

## •

## 複数のモデルの出力でランク付けし，一番報酬が高い入出力ペアでSFTし，その

## 他のペアに関しては出力しにくくしするように損失関数を設定

## •

## PPOをよりシンプルにした手法

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Chain of Hindsight | 後知恵によるフィードバック

## [78] Liu, Tianhao, et al. (2023), "Chain of Hindsight Aligns Language Models with Feedback" より引用

## 141

## •

## 人間がランキングした後に，なぜそのランキングなのかの理由を追加する

## •

## ランキングと理由をもとに言語モデルをfine-tuning

## •

## CoHF(Chain of Hindsight Finetuning)と呼ばれる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## •

## RealToxicity, TruthfulQAでの評価では，InstructGPTが一番良いスコアを出して

## いる(無害性，真実性)

## InstructGPTの評価: 公開データセットでの評価

## [28] Ouyang, Long, et al. (2022), "Training Language Models

## to Follow Instructions with Human Feedback" より引用

## 142

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 学習データのフォーマットについて

[67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation" より引用

## 143

## • 主に，Feedbackのタイプは数値，ランキング，自然言語，その他(MQM,

## Post-Edition等)に分けられる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 学習によく使用されるデータセット

## 144

## • 基本的には英語のデータセットがほとん

## ど

## • Anthoropic, stanfordnlpなどがリリース

## • 右はHH-RLHFの一例でchosenとrejected

## のrankingがついている

## • その他にもOppenAssistant

## datasets(oasst1, oasst2), HelpSteer, Uni-

## RLHF，UltraFeedBackなど

## [67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on

## Integrating (Human) Feedback for Natural Language Generation" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## (参考) 発展的議題①: 個人的意見を多く含みます

145

## •

## なぜRLHFで性能が上がるのか？

## •

## 性能が上がっている訳ではなさそう

## •

## 事前学習で得た分布を意図に沿う出力に変化させているだけ？

## •

## 学習を間違えると，条件付け意図しない分布から出力されてしまう

## •

## RLは本当に必要なのか？

## •

## DPO, PRO, RLCD等のRLを用いないHuman Feedbackの方法が多数提

## 案されており，RLHFと同程度以上の性能を出している

## •

## おそらくRLは必要ではない

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## (参考) 発展的議題②: 個人的意見を多く含みます

146

## •

## SFT vs RLHF

## •

## SFTも人間からのlanguage feedbackと解釈することもできる．

## •

## そうなれば，SFTだけで十分でRLHFは必要ではないのか？

## •

## ある程度まではSFTで十分，残り1%を制御するには必ず必要になる

## •

## モデルの出力制御にはHuman Feedbackは今後も必要になる

## •

## 人間のfeedbackの限界としてlanguage feedbackは難しすぎる

## •

## Rankingによる判断が一番正確？

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## (参考) 発展的議題③: 個人的意見を多く含みます

147

## •

## RLHF vs RLAIF

## •

## 人間が介在しないAI FeedbackではFeedback元のモデルの性能を超える

## こと基本的にはないと考えられる

## •

## しかし，人間のフィードバック性能をAIで引き上げる方向性としての

## RLAIFは続いていくと考えられる(Constitutional AI)

## •

## もしくは，外部ツールを用いてあらゆる形式の情報をもとにフィードバ

## ックを行なっていく形式であれば性能は向上していくと考えられる

## •

## RLCF(reinforcement learning from computational feedback)

## https://www.interconnects.ai/p/beyond-human-data-rlaif

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

148

[1] DeepMind, "MuZero: Mastering Go, chess, shogi and Atari without rules", https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-

rules/ アクセス日:2026/5/24

[2] CNN.co.jp (2017), "AlphaGo関連記事", https://www.cnn.co.jp/tech/35080140.html アクセス日:2026/5/24

[3] TrackingAI, "AI Progress Tracking", https://www.trackingai.org/home アクセス日:2026/5/24

[4] Zhang, Kaiyan, et al. (2025), "A Survey of Reinforcement Learning for Large Reasoning Models", arXiv:2509.08827

[5] OpenAI (2022), "Instruction Following", https://openai.com/research/instruction-following アクセス日:2026/5/24

[6] Zhao, Wayne Xin, et al. (2023), "A Survey of Large Language Models", arXiv:2303.18223

[7] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models", arXiv:2307.09288

[8] HuggingFace, "Math-Verify", https://github.com/huggingface/Math-Verify アクセス日:2026/5/24

[9] Lambert, Nathan, et al., "RLHF Book Chapter 14: Reasoning", https://rlhfbook.com/c/07-reasoning アクセス日:2026/5/24

[10] ARC Prize, "ARC Prize Leaderboard", https://arcprize.org/leaderboard アクセス日:2026/5/24

[11] 日本経済新聞(2021), "韓国で「対話AI」暴走

機械学習が陥ったワナ", https://www.nikkei.com/article/DGXZQOGM21B9V0R20C21A1000000/ アクセス

日:2026/5/24

[12] Wolfe, Cameron R. (2023), "Specialized LLMs: ChatGPT, LaMDA, Galactica, Codex, Sparrow, and More",

https://cameronrwolfe.substack.com/p/specialized-llms-chatgpt-lamda-galactica アクセス日:2026/5/24

[13] Stanford Online (2023), "CS25 I Stanford Seminar - Transformers United 2023: Language and Human Alignment",

https://www.youtube.com/watch?v=DJ1Yy6Aquug&list=PLoROMvodv4rNiJRchCzutFw5ItR_Z27CM&index=13 アクセス日:2026/5/24

[14] Anthropic, "hh-rlhf Dataset", https://huggingface.co/datasets/Anthropic/hh-rlhf アクセス日:2026/5/24

[15] Li, Junyi, et al. (2023), "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models", arXiv:2305.11747

[16] Nangia, Nikita, et al. (2020), "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models", arXiv:2010.00133

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

149

[17] Wang, Yuxia, et al. (2023), "Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs", arXiv:2308.13387

[18] OpenAI (2023), "Weak-to-Strong Generalization", https://openai.com/index/weak-to-strong-generalization/ アクセス日:2026/5/24

[19] Wikipedia, "Existential risk from artificial intelligence", https://en.wikipedia.org/wiki/Existential_risk_from_artificial_intelligence アクセス日:2025/3/1

[20] CNET Japan (2018), "AI自動運転車、「強化学習」で運転方法を20分で習得", https://japan.cnet.com/article/35122203/ アクセス日:2026/5/24

[21] CNET Japan (2017), "AI関連記事", https://japan.cnet.com/article/35094593/ アクセス日:2026/5/24

[22] Boston Dynamics, "Boston Dynamics", https://bostondynamics.com/ アクセス日:2026/5/24

[23] OpenAI, "ChatGPT", https://chatgpt.com/ アクセス日:2026/5/24

[24] BrainPad Platinum Data Blog (2023), "ChatGPTの仕組みを論文ベースで超詳細に解説", https://blog.brainpad.co.jp/entry/2023/05/31/160719 アクセス

日:2026/5/24

[25] zero2one, "方策勾配法(Policy Gradient Methods)", https://zero2one.jp/ai-word/policy-gradient-methods/ アクセス日:2026/5/24

[26] OpenAI (2017), "Learning from human preferences", https://openai.com/index/learning-from-human-preferences/ アクセス日:2026/5/24

[27] Stiennon, Nisan, et al. (2020), "Learning to Summarize from Human Feedback", arXiv:2009.01325

[28] Ouyang, Long, et al. (2022), "Training Language Models to Follow Instructions with Human Feedback", arXiv:2203.02155

[29] Rafailov, Rafael, et al. (2023), "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", arXiv:2305.18290

[30] Azar, Mohammad Gheshlaghi, et al. (2023), "A General Theoretical Paradigm to Understand Learning from Human Preferences", arXiv:2310.12036

[31] Ethayarajh, Kawin, et al. (2024), "KTO: Model Alignment as Prospect Theoretic Optimization", arXiv:2402.01306

[32] Saeidi, Amir, Verma, Shivanshu, and Baral, Chitta (2024), "Insights into Alignment: Evaluating DPO and its Variants Across Multiple Tasks",

arXiv:2404.14723

[33] Ivison, Hamish, et al. (2024), "Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preference Feedback", arXiv:2406.09279

[34] Wang, et al. (2024), "Beyond Reverse KL: Generalizing Direct Preference Optimization with Diverse Divergence Constraints", ICLR 2024, arXiv:2309.16240

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

150

[35] Liu, et al. (2024), "Training Socially Aligned Language Models in Simulated Human Society",

https://www.researchgate.net/publication/371124037_Training_Socially_Aligned_Language_Models_in_Simulated_Human_Society アクセス日:2026/5/24

[36] Dubois, Yann, et al. (2023), "AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback", arXiv:2305.14387

[37] epoch.ai, "GPQA Diamond Benchmark", https://epoch.ai/benchmarks/gpqa-diamond?view=graph&tab=release-date アクセス日:2026/5/24

[38] Chollet, François (2023), ARC Prize関連ポスト, https://x.com/fchollet アクセス日:2026/5/24

[39] Nikankin, A., et al. (2025), "Arithmetic without algorithms: Language models solve math with a bag of heuristics", arXiv:2410.21272

[40] Sutskever, Ilya (2024), "Sequence to Sequence Learning with Neural Networks", NeurIPS 2024,

https://proceedings.neurips.cc/paper_files/paper/2014/file/5a18e133cbf9f257297f410bb7eca942-Paper.pdf アクセス日:2026/5/24

[41] OpenAI (2025), "GPT-4.5 System Card", https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf アクセス日:2026/5/24

[42] OpenAI (2024), "Learning to Reason with LLMs", https://openai.com/index/learning-to-reason-with-llms/ アクセス日:2026/5/24

[43] DeepSeek-AI, Guo, Daya, et al. (2025), "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning", arXiv:2501.12948

[44] Silver, David and Sutton, Richard (2025), "Welcome to the Era of Experience", https://storage.googleapis.com/deepmind-media/Era-of-

Experience%20/The%20Era%20of%20Experience%20Paper.pdf アクセス日:2026/5/24

[45] Shao, Zhihong, et al. (2024), "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", arXiv:2402.03300

[46] oxen.ai (2024), "Why GRPO is Important and How it Works", https://www.oxen.ai/blog/why-grpo-is-important-and-how-it-works アクセス日:2026/5/24

[47] Gandhi, et al. (2025), "Cognitive Behaviors that Enable Self-Improving Reasoners, or, Four Habits of Highly Effective STaRs", arXiv:2503.01307

[48] Liu, Zichen, et al. (2025), "Understanding R1-Zero-like Training: A Critical Perspective", arXiv:2503.20783

[49] Yu, Qiying, et al. (2025), "DAPO: An Open-Source LLM Reinforcement Learning System at Scale", arXiv:2503.14476

[50] Chu, T., et al. (2025), "SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-Training", arXiv:2501.17161

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

151

[51] Yue, Y., et al. (2025), "Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?",

https://openreview.net/pdf?id=4OsgYD7em5 アクセス日:2026/5/24

[52] Liu, M., et al. (2025), "ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models", arXiv:2505.24864

[53] Peng, Ruotian, et al. (2025), "SimKO: Simple Pass@K Policy Optimization", arXiv:2510.14807

[54] Wang, Y., et al. (2025), "Reinforcement Learning for Reasoning in Large Language Models with One Training Example", arXiv 2025

[55] Huang, Ting, et al. (2025), "3D-R1: Enhancing Reasoning in 3D VLMs for Unified Scene Understanding", arXiv:2507.23478

[56] GUI-R1 (2025), "GUI-R1: A Generalist R1-Style Vision-Language Action Model For GUI Agents", arXiv:2504.10458

[57] Li, et al. (2025), "SimpleVLA-RL: Scaling VLA Training via Reinforcement Learning", arXiv:2509.09674

[58] Feng, et al. (2025), "Efficient Reasoning Models: A Survey", arXiv:2504.10903

[59] Zhu, et al. (2025), "A Survey on Latent Reasoning", arXiv:2507.06203

[60] Dong, et al. (2025), "Reinforcement Pre-Training", arXiv:2506.08007

[61] Ye, Seonghyeon, et al. (2023), "FLASK: Fine-grained Language Model Evaluation based on Alignment Skill Sets", arXiv:2307.10928

[62] Lambert, Nathan, et al. (2024), "RewardBench: Evaluating Reward Models for Language Modeling", arXiv:2403.13787

[63] Casper, Stephen, et al. (2023), "Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback", arXiv:2307.15217

[64] Parrish, Alicia, et al. (2023), "Which Examples Should be Multiply Annotated? Active Learning When Annotators May Disagree", ACL Findings 2023,

https://aclanthology.org/2023.findings-acl.658/ アクセス日:2026/5/24

[65] Veselovsky, Veniamin, et al. (2023), "Artificial Artificial Artificial Intelligence: Crowd Workers Widely Use Large Language Models for Text Production Tasks",

arXiv:2306.07899

[66] Zhou, Chunting, et al. (2023), "LIMA: Less Is More for Alignment", arXiv:2305.11206

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

152

## [67] Shen, Mingyang, et al. (2023), "Bridging the Gap: A Survey on Integrating (Human) Feedback for Natural Language Generation",

## arXiv:2305.00955

## [68] Gao, Leo, et al. (2022), "Scaling Laws for Reward Model Overoptimization", arXiv:2210.10760

## [69] Wei, Alexander, et al. (2023), "Jailbroken: How Does LLM Safety Training Fail?", arXiv:2307.02483

## [70] OpenAI (2023), "GPT-4 Technical Report", arXiv:2303.08774

## [71] Wu, Zeqiu, et al. (2023), "Fine-Grained Human Feedback Gives Better Rewards for Language Model Training", arXiv:2306.01693

## [72] Rame, Alexandre, et al. (2023), "Rewarded soups: towards Pareto-optimal alignment by interpolating weights fine-tuned on diverse

## rewards", arXiv:2306.04488

## [73] Yuan, Zheng, et al. (2023), "RRHF: Rank Responses to Align Language Models with Human Feedback without tears",

## arXiv:2304.05302

## [74] Irpan, Alex (2018), "Deep Reinforcement Learning Doesn't Work Yet", https://www.alexirpan.com/2018/02/14/rl-hard.html アクセス

## 日:2026/5/24

## [75] Zheng, Rui, et al. (2023), "Secrets of RLHF in Large Language Models Part I: PPO", arXiv:2307.04964

## [76] Dong, Hanze, et al. (2023), "RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment", arXiv:2304.06767

## [77] Yang, Kevin, et al. (2023), "RLCD: Reinforcement Learning from Contrast Distillation for Language Model Alignment",

## https://github.com/facebookresearch/RLCD アクセス日:2026/5/24

## [78] Liu, Tianhao, et al. (2023), "Chain of Hindsight Aligns Language Models with Feedback", arXiv:2302.02676

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

153

## [79] Peng, Baolin, et al. Stabilizing RLHF through Advantage Model and Selective Rehearsal. 2023. In arXiv:2309.10202

## [80] Stephanie Lin et al. (2022) "TruthfulQA: Measuring How Models Mimic Human Falsehoods" ACL 2022

## [81] Junyi Li et al. (2023) "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models" EMNLP 2023

## [82] Yuntao Bai et al. (2022) "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback" arXiv:2204.05862

## （Anthropic HH-RLHF Dataset）

## [83] Nikita Nangia et al. (2020) "CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models" EMNLP 2020

## [84]Rudinger, Rachel, et al. (2018), "Gender Bias in Coreference Resolution", https://github.com/rudinger/winogender-schemas アクセス日

## :2026/5/29

## [85] Zhichao Wang et al. (2024) "A Comprehensive Survey of LLM Alignment Techniques: RLHF, RLAIF, PPO, DPO and More" arXiv:2407.16216
