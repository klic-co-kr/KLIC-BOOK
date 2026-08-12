# Day 6

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 注意事項: 本資料の再利用(2次利用)について

## ●

本資料について

## ○

東京大学松尾・岩澤研究室が作成し、2025年10月から11月にかけて開催されたLLM大規模言語モデル講座基礎編

の講義資料です。

## ○

クリエイティブ・コモンズのCC BY-NC-SA 4.0 DEED(表示– 非営利– 継承4.0 国際)のライセンス登録を

しています。

## ●

ライセンスの表示について

## ○

各スライドのページ最下部にライセンスの記載があります。再利用時には本ライセンス表示を必ずご記載ください。

再利用時に複製が困難な場合は、下記のテキストボックスを利用の上、ハイパーリンクも含めてライセンスの表記を

するようお願いします。

## ○

再利用するページに参照論文等の引用がある場合は、巻末にあるReferenceより引用箇所を掲載してください。

## ●

非営利目的での利用について

再利用(2次利用)が許諾されています。

## ●

営利目的での再利用について

こちらからお問い合わせください。

## ●

その他

## ○

元の表現が変わらない範囲(フォント、サイズ等)であれば改変可能です。

## ○

それ以外の改変その他ライセンスについての詳細は、こちらをご覧の上適切な取り扱いをお願いします。

東京大学松尾・岩澤研究室

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 講義パート：中筋渉太

## 大規模言語モデル基礎2025 Autumn Day6

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Day6 講師自己紹介

## 1. Day6 イントロダクション

3

遠い昔のGCI講座海外研修より

## -

## 中筋渉太(NAKASUJI, Shota)

## -

## Co-Founder, CIO at SPEQTRA Investment Research Pte. Ltd.

## -

## シンガポールにて、資産運用系スタートアップを共同創業、

## データサイエンス・AIを活用したクオンツリサーチが専門

## -

## 経歴:

## -

## 2023年3月東京大学工学部物理工学科卒業

## -

## 2025年3月同大学大学院工学系研究科修了

## -

## 松尾研関連:

## -

## 共同研究プロジェクトPM

## -

## クオンツ運用プロジェクトPM

## -

## GCI講座TA・講師

## -

## 「画像認識」講座教材開発

## -

## 「金融市場取引と機械学習」講座監修・講師

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## 大規模言語モデルのFine-Tuning

4

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning における問題意識

## 1. Day6 イントロダクション

## 問題意識

## 解決の方向性

5

## -

## 大規模言語モデルの性能改善や様々な

## タスク・ドメインへの適応を実現したい

## -

## 莫大なリソースを要するPre-Training は

## 多くの主体にとってハードルが高い

## -

## Fine-Tuning によって事前学習済みモデ

## ルの性能改善やタスク・ドメイン適応を実

## 現

## -

## 特にInstruction Tuning によって、

## 対話性能やZero/Few-shot 性能を向上

## -

## 大規模言語モデルは膨大なパラメータを

## 有するため、Fine-Tuning であっても

## 全てのパラメータを扱えない場合がある

## -

## Catastrophic Forgetting や過学習で、

## 事前学習モデルの性能を毀損する恐れ

## -

## 追加的に設定したパラメータや、一部の

## パラメータのみを訓練・更新の対象とする

## ことで、効率的なFine-Tuning を実現

## -

## このような手法を特にParameter

## Efficient Fine-Tuning (PEFT) と呼ぶ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例| ChatGPT

## 1. Day6 イントロダクション

6

## -

## 事前学習済みLLMは高い性能

## を示すが、必ずしも人間の

## 価値観に沿った出力をしない

## -

## ChatGPTではInstructGPT

## 論文※で提案された手法に

## 則って、上記の問題に対処

## -

## 具体的に以下を組み合わせ、

## 人間の価値観への調整を実現

## -

## Supervised Fine-Tuning

## = Instruction Tuning

## -

## RLHF

[2] Ouyang, Long, et al. (2022), "Training language models to

follow instructions with human feedback" より引用

[1] OpenAI(2023), “Introducing ChatGPT”より引用し、一部改変

Supervised Fine-Tuning

= Instruction Tuning

Reinforcement Learning from Human Feedback

(RLHF)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例| OpenAI API Fine-Tuning

## 1. Day6 イントロダクション

7

[3] OpenAI(2024), “Fine-tuning now available for GPT-4o” より引用

## -

## OpenAI API では、Fine-

## Tuning 機能が提供

## -

## 自前のデータセットを用いた

## Fine-Tuning が実施可能

## -

## 以下のような用途が例示

## -

## 出力フォーマットの固定

## -

## 画像理解＋テキスト出力

## -

## レイアウト一貫性の強化

## -

## Prompting と比較して、

## 以下のような利点が例示

## -

## トークン・処理時間節約

## -

## 応答の品質・制御性向上

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例| Med-Gemini

## 1. Day6 イントロダクション

8

## -

## Med-Gemini※ :

## -

## Google が開発した大規模言語モデルGemini を医療向けに特化させたモデル

## -

## 医療領域でのマルチモーダル能力が強化され、各種ベンチで強力な結果を報告

[4] Saab, Khaled, et al.(2024), “Capabilities of gemini models in medicine.” より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデル基礎Day6 の目標

## 1. Day6 イントロダクション

## 大規模言語モデルの典型的な訓練フローにおいて、Fine-Tuning が

## Pre-Training やRLHF・DPO に対してどう位置付けられるか説明できる

## 大規模言語モデルのFine-Tuning において、特に重要なアプローチである

## Instruction Tuning やPEFT が既存手法に対してどう異なるか説明できる

## Goal 1

## Goal 2

## Goal 3

9

## Instruction Tuning およびPEFT について、その目的や内容を十分に理解

## した上で実際にそれらを実装し、大規模言語モデルの性能改善を実現できる

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## 大規模言語モデルのFine-Tuning

10

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM 訓練フローにおけるFine-Tuning

## 2. 大規模言語モデルのFine-Tuning

## Pre-Training

## 大規模コーパスによる自己教師あり学習を通して、言語モデルに

## 語彙・文法・知識といった基本的な言語理解を獲得させる段階

## Supervised Fine-Tuning

## ラベル付きデータによる教師あり学習を通し、言語モデルの性能

## を改善したり、特定のタスクやドメインへの適応を実現する段階

## RLHF・DPO etc.

## 人間の選好にもとづく後段の最適化を通じて、言語モデルの

## 出力がより人間の価値観に沿ったものとなるよう調整する段階

11

## Step 1

## Step 2

## Step 3

## 1

## 2

## x : 次ページで整理

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Pre-Training vs. Fine-Tuning / Post-Training

## 2. 大規模言語モデルのFine-Tuning

12

## Pre-Training

## データ

## Fine-Tuning / Post-Training

## 目的

## -

## 語彙・文法・知識・推論能力など

## の言語能力を、言語モデルに導入

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

## -

## 事前学習済みモデルの性能改善

## や、

## 様々なタスクに対する適応を実現

## -

## 教師あり学習

## -

## 下流タスクへの特化

## -

## Instruction Tuning

## -

## RLHF・DPO etc.

## -

## 小規模データセット

## -

## 例LIMA: 1000サンプル(3MB)

## -

## 人間・モデルによるフィードバック

## 1

## 2

: 今回のトピック

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

従来的なFine-Tuning

## タスク

## 設計

## 重み

## 更新

大規模言語モデルのFine-Tuning

13

## 大規模言語モデルのFine-Tuning

## 2. 大規模言語モデルのFine-Tuning

## 主目的

## -

## 事前学習済みモデルをベースとし、

## 特定の下流タスクを高い精度で

## 解けるモデルを効率的に獲得

## -

## 事前学習済みモデルの出力内容や

## 形式を用途に応じて調整・制御

## -

## 事前学習済みモデルの未知タスクに

## 対するZero/Few-shot性能を改善

## -

## 解きたいタスクで教師あり学習

## -

## 例: 感情分析・自然言語推論

## -

## 指示文を入力、それに対する理想的

## な出力文を正解として教師あり学習

## (Instruction Tuning)

## -

## 事前学習済みモデルの各層内の全て

## のパラメータについて更新を実施

## (対比的にFull-FTと呼ぶことがある)

## -

## 別途設定した追加パラメータや、

## 一部のパラメータのみを更新

## (Parameter Efficient Fine-Tuning)

## A

## B

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Fine-Tuning のタスク設計

## 2. 大規模言語モデルのFine-Tuning

従来的なFine-Tuning

Instruction Tuning

14

## -

## 特定の下流タスクで教師あり学習を実施

## -

## 主に下流タスク用の特殊トークンを活用

[5] PyTorch Tutorial, “Dynamic Quantization on BERT”より引用

[6] Wei, Jason, et al.(2021) "Finetuned language models are zero-shot

learners." arXiv preprint arXiv:2109.01652 (2021). より引用し、一部改変

## -

## 指示文に対して、理想的な出力文を

## 正解とする教師あり学習を実施

## -

## 様々なタスクがこの入出力形式に内包

## A

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Fine-Tuning の重み更新

## 2. 大規模言語モデルのFine-Tuning

## 従来的なFine-Tuning (Full-FT)

## Parameter Efficient Fine-Tuning (PEFT)

15

Output

Input

## -

## 事前学習済みモデルが持つ各層内の全て

## のパラメータについて、更新を実施

## -

## より確実な性能改善が期待される一方、

## より多くの計算リソースを必要とする

Input

Output

## -

## 追加的に設定したパラメータや、

## 一部のパラメータのみを訓練・更新

## -

## 適切に用いることができれば、少ない

## リソースで性能改善を達成できる

追加設定分や

パラメータの

一部を更新

層の中の全て

のパラメータ

が更新対象

## B

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## 大規模言語モデルのFine-Tuning

16

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Fine-Tuning のタスク設計(再掲)

## 従来的なFine-Tuning

## Instruction Tuning

17

## -

## 特定の下流タスクで教師あり学習を実施

## -

## 主に下流タスク用の特殊トークンを活用

[5] PyTorch Tutorial “Dynamic Quantization on BERT”より引用

[6] Wei, Jason, et al. "Finetuned language models are zero-shot learners."

(2021). より引用し、一部改変

## -

## 指示文に対して、理想的な出力文を

## 正解とする教師あり学習を実施

## -

## 様々なタスクがこの入出力形式に内包

## A

## 3. Instruction Tuning

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning 概要| FLAN論文による提案

## 3. Instruction Tuning

18

[7] Google Research(2021), “Introducing FLAN: More generalizable

Language Models with Instruction Fine-Tuning”より引用

## -

## Wei, Jason, et al. "Finetuned language

## models are zero-shot learners." arXiv

## preprint arXiv:2109.01652 (2021).

## -

## 様々なタスクを指示・回答という入出力

## 形式に統一したデータセットによって、

## 言語モデルをFine-Tuning する手法を提案

## (Instruction Tuning)

## -

## このようにFine-Tuning されたモデルは

## 評価に用いられた25のタスクの内、

## -

## 21タスクで、Zero-shot性能が向上

## -

## 20タスクで、よりパラメータ数の多い

## GPT-3と比べ、より高いZero-shot性能

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning 概要| タスク構成と入出力例

## 3. Instruction Tuning

## 入力(Instruction)

## 出力(Instance)

## 構成

## 具体例

## (FLAN※)

## -

## タスクを指定する指示文

## -

## (Optional) 付随する補足情報

## -

## "Víte, rozhodl jsem se, že si

## pořídím psa. Translate to

## English"

## -

## 与えられた指示文に対する、

## 理想的な回答例

19

## -

## "You know, I decided to get a

## dog."

## -

## "i'm 10x cooler than all of

## you! What is the sentiment of

## this tweet?"

## -

## "positive"

## xx : 元データでの記述

## xx : テンプレートにより

## 付加した指示部分

[8] HuggingFace, "flan2021_submix_original" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning の有効性

## 3. Instruction Tuning

## Zero-shot性能の向上

## 指示応答性能の向上

20

## -

## FLAN※1

## -

## 137Bモデルに対して、Instruction

## Tuning を適用し、GPT-3と比較

## -

## パラメータ数で大幅に勝るGPT-3 の

## Zero-shot およびFew-shot 性能を

## 超えるZero-shot 性能を示した

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners" よ

り引用

[9] Taori, Rohan, et al. (2023), "Alpaca" より引用

## -

## Alpaca※2

## -

## Meta社が開発したLLaMA 7Bモデル

## にInstruction Tuning を適用

## -

## パラメータ数で大幅に勝るGPT-3.5

## と同程度の指示応答挙動に改善

-

入力例: What is an alpaca? How is it

different from a llama?

-

出力例: An alpaca is domesticated species of

South American camelid, related to the

llama and the vicuna. It is smaller than a

llama, and has finer and softer fleece. ...

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction Tuning の難しさ

## 3. Instruction Tuning

## データセット作成上の困難

## 知識は導入可能か

21

## -

## Instruction Tuning によって望ましい

## 挙動を実現するためには、高品質かつ

## 無害なデータセットの用意が必要

## ➢人力で作成するのがよい?

## -

## 一方、指示に含まれる個別のタスクや

## 形式の多様性の重要性も指摘されている

## ➢既存のデータセットを活用?

## -

## そうした様々な観点を考慮に入れて

## データセットを構築するためには、

## 多くの人的・技術的リソースを要する

## ➢データセットもLLMで生成?

[9] Taori, Rohan, et al. (2023), "Alpaca" より引用

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment" より引用

## -

## LIMA (2023)[10]

## -

## Fine-Tuning は、事前学習で獲得され

## た知識・能力を”引き出す”ことで性能

## 改善を実現しているとする、

## Superficial Alignment Hypothesis

## を提唱

## -

## Kung and Peng (2023)[9]

## -

## Instruction Tuning による性能改善が

## タスクの理解を通じてではなく、出力

## 形式といった表面的事項の学習に起因

## する可能性を指摘

## : 次ページ以降で詳解

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

22

## Instruction データセット作成上の要点

## 3. Instruction Tuning

## -

## LIMA[10]: Instruction Tuning ではデータの量より質が重要だと主張

## -

## 1000件と少量の高品質データを用いたInstruction Tuning のみにより、

## RLHF で訓練されたモデルよりも高品質な回答を生成できたことを報告

## -

## 事前学習済みモデルについて懸念される有害な出力を抑制するため、

## Instruction Tuning では有害なデータを避けて学習を実施したい

## -

## Llama 2[11]: 無害なデータセット構築の実例を提示(次ページで詳解)

## -

## タスクごとの指示形式の多様化により、未知タスクに対する性能が向上

[12]

## データの質

## データの

## 無害性

## 指示形式の

## 多様性

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment" より引用

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models" より引用

[12] Sanh, Victor, et al. (2021), "Multitask prompted training enables zero-shot task generalization" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction データセット構築事例| Llama2

## 3. Instruction Tuning

23

## Llama2 とは[11]

## アノテーターの選定・指示

## -

## Meta 社が開発・公開する大規模言語モデ

## ル

## で、7B, 13B, 70Bのバリエーションを含む

## -

## 事前学習済みモデルに加えて、Instruction

## Tuning およびRLHF の適用モデルも提供

## -

## 安全性の向上を目的として、人間による

## アノテーションや評価を積極的に採用

## -

## アノテーターが様々なデータ作成

## タスクに取り組む上での資質と適性を

## 評価するため、複数のテストを実施

## -

## 選定されたアノテーターに、以下を

## 満たす指示文・回答の作成を依頼

## -

## Informative

## -

## Relevant

## -

## Harmless

## -

## 例: 指示文作成で避けるべき項目

## -

## 犯罪行為の助長

## -

## 攻撃的な言動の助長

## -

## Truthful

## -

## Clear

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned

chat models" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Instruction データセットの構築手法

## 3. Instruction Tuning

## -

## 既存のラベル付きデータセットを、

## テンプレートを用いて変換

## -

## FLAN[6] : 62個のデータセットを統合

## -

## 指示文に対する回答を人間が作成

## -

## InstructGPT[2] : 人間が作成した

## 指示文に対し、人間が回答を作成

## -

## 指示文に対する回答をLLMが生成

## -

## Self-Instruct[13] : LLMによる指示文

## と回答の生成フレームワークを提案

## ラベル付きデ

## ータセットの

## 統合

## 人間による

## データ作成

## LLMによる

## データ生成

24

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback" より引用

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners" より引用

[13] Wang, Yizhong, et al. (2022), arXiv:2212.10560 より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## LLM Fine-Tuning

25

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Fine-Tuning の重み更新

## (再掲)

## 従来的なFine-Tuning (Full-FT)

## Parameter Efficient Fine-Tuning (PEFT)

26

Output

Input

## -

## 事前学習済みモデルが持つ各層内の全て

## のパラメータについて、更新を実施

## -

## より確実な性能改善が期待される一方、

## より多くの計算リソースを必要とする

Input

Output

## -

## 追加的に設定したパラメータや、

## 一部のパラメータのみを訓練・更新

## -

## 適切に用いることができれば、少ない

## リソースで性能改善を達成できる

追加設定分や

パラメータの

一部を更新

層の中の全て

のパラメータ

が更新対象

## B

## 4. Parameter Efficient Fine-Tuning

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Full-FT vs. Parameter Efficient Fine-Tuning

## 4. Parameter Efficient Fine-Tuning

27

## Full-FT

## 保存

## 領域

## Parameter Efficient Fine-Tuning (PEFT)

## 概要

## -

## 事前学習済みモデルの全パラメータ

## について、別タスクで更新を実施

## 計算

## リソース

## -

## 大規模なモデルでは、莫大な

## 計算リソースが必要

## -

## 例GPT-3 : 1.2TBのGPUメモリ

## -

## 元モデルと同サイズのパラメータ

## を保存するため、大きな領域が必要

## -

## 例GPT-3 : 350GBの保存領域

## -

## 追加的に設定したパラメータや、

## 一部のパラメータのみで更新を実施

## -

## 大規模なモデルについても、限定的な

## 計算リソースで性能改善を実現

## -

## 例GPT-3 LoRA : 350GBのGPUメモリ※

## -

## 更新部分のパラメータのみを保存

## すればよく、小さな保存領域で十分

## -

## 例GPT-3 LoRA: 35MBの保存領域[14]

## : 次ページで詳解

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT によるGPUメモリ使用量の削減

## 4. Parameter Efficient Fine-Tuning

28

## Model Loading

## Backward

## (Gradients)

## Optimizer

## (Adam)

## Full-FT (Ntrain :

## 7B)

## PEFT (Ntrain: 1M)

## Total

## ~ 13GB

## ~ 13GB

## Estimation

## size(float) * Nall

## 2 * size(float) *

## Ntrain

## size(float) * Ntrain

## ~ 26GB

## ~ 13GB

## ~ 2MB

## ~ 52GB + α

## ~ 13GB + α

## ~ 4MB

## VRAM by Steps

(※ 上記の他に、batch sizeに

比例して増加するForward分

やライブラリ確保領域がある)

## -

## 7Bモデルの16-bit Fine-Tuning を想定し、Full-FT とPEFT のGPUメモリ使用量を概算比較

## -

## 以下で、全パラメータ数Nall = 7B, 浮動小数点数のサイズsize(float) = 2byte の状況に対応

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 手法を評価する上での主要な観点

## 4. Parameter Efficient Fine-Tuning

29

## 性能改善

## 運用性

## 推論効率

## -

## Full-FT を実施した場合と比べて、性能改善に大きな劣化がないか

## -

## 事前学習済みモデルのサイズに依らず、性能改善が実現されるか

## -

## 更新する※パラメータが少なく、小さいストレージで運用が可能か

## -

## それができると複数モデルの並列運用やバージョニングが容易に

## -

## 追加するパラメータが多いことで、推論コストを増大させないか

## -

## 入力文の系列長が長くなることで、推論コストを増大させないか

## 訓練効率

## -

## 学習する※パラメータが少なく、小さいGPUメモリでも実現可能か

## -

## GPUの効率的な活用によって高速化が可能な手法となっているか

※「学習するパラメータは少ないが、それに基づいて多くのパラメータが更新される」ということがあるため、

「更新するパラメータ」と「学習するパラメータ」という似たような表現も、ここでは区別して使っている。

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 様々なPEFT 手法

## 4. Parameter Efficient Fine-Tuning

30

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning" より引用

運用性

訓練効率

推論効率

Extra FFN :

FFN層の追加によって、

推論にオーバーヘッド

No overhead :

推論にオーバーヘッド

を伴わない手法

Extra input :

入力系列への追加で、

推論にオーバーヘッド

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 手法のカテゴリー分類

## 4. Parameter Efficient Fine-Tuning

31

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient

fine-tuning" より引用

## 1

## 2

## 3

## 4

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## PEFT 手法の代表的なカテゴリー

## 4. Parameter Efficient Fine-Tuning

32

## Adapter型

## Soft Prompt型

## Reparametrization型

## Selective型

## 概要

## 代表例

## 2

## 1

## 3

## 4

## Transformer内部にMLP層

## (Adapter)を追加し、それのみの学習

## を実施

## 入力系列にタスクごとのベクトル

## (Soft Prompt) を付加し、学習を実

## 施

## 事前学習済みモデルが持つパラメー

## タのうち、一部のみで学習を実施

## 行列分解に基づき、再パラメータ化

## された重みについて学習を実施

## Adapter (2019)

## Prompt Tuning

## (2021)

## BitFit (2021)

## LoRA (2021)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Adapter型| Adapter (2019)

## 4. Parameter Efficient Fine-Tuning

33

## 1

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP" より引用し、

一部改変

Transformer内部に

学習可能なAdapter

モジュールを追加

Adapterは、単純な

MLPの構造を持つ

## -

## Transformer内部に学習可能な

## Adapterモジュールを追加・学習

## -

## 追加位置の異なる亜種が存在

## (例: Parallell Adapter※は左図とは

## 異なり、並列的にAdapterを追加)

## -

## Adapterは単純なMLPの構造を持

## つ

[17] He, Junxian, et al. (2021), "Towards a unified view of parameter-

efficient transfer learning" より引用

## -

## Transformer内部に学習可能な

## Adapterモジュールを追加・学習

## -

## 追加位置の異なる亜種が存在

## (例: Parallell Adapter※は左図とは

## 異なり、並列的にAdapterを追加)

## -

## Adapterは単純なMLPの構造を持

## つ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Adapter型| Adapter (2019)

## 4. Parameter Efficient Fine-Tuning

34

## 1

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP" より引用

横軸(対数):

訓練パラメータ数

Full-FT (トップ層のみ)

Adapter:

Full-FTと

同等の精度

## -

## Cons

## -

## Adapter が追加されること

## で、推論にオーバーヘッドが

## 発生

## -

## Pros

## -

## Full-FT に対し10-1から10-2ほ

## ど小さい訓練パラメータ数

## で、

## Full-FT と同等の精度(左図)

## -

## Adapter のみ保存すればよ

## く、柔軟に付け替え対応が可

## 能

SQuADタスク

BERT FT比較

縦軸:

F1 score

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Soft-Prompt型| Prompt Tuning (2021)

## 4. Parameter Efficient Fine-Tuning

35

## 2

[18] Lester, Brian, et al. (2021), "The power of scale for parameter-efficient prompt tuning" より引用

従来のFine-Tuning:

タスクごとにFTを実施

Prompt Tuning:

タスクごとにベクトルを

用意し、入力に付加・学習

## -

## 各タスクに対応したベクトル

## (Soft Prompt) を入力系列に

## 付加し、そのパラメータを学習

## -

## Soft Prompt は、文章の形で設

## 計されたプロンプト(Hard

## Prompt) に対する呼び方・考え方

## -

## つまり、各タスクごとに特化した

## プロンプトエンジニアリングを

## 学習していると捉えることが可能

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Soft-Prompt型| Prompt Tuning (2021)

## 4. Parameter Efficient Fine-Tuning

36

## 2

[18] Lester, Brian, et al. (2021), "The power of scale for parameter-efficient prompt tuning"

より引し、一部改変

横軸(対数):

全パラメータ数

GPT-3 Few-shot

T5 Prompt Tuning

T5 Full-FT

赤: タスクごと

橙: マルチタスク

## -

## Pros

## -

## モデルサイズが大きい場合、

## Prompt Tuning はFull-FT と

## 同等の精度(左図)

## -

## T5-XXL (11B)でSoft Prompt

## の長さを100とすると、訓練

## する

## パラメータ数は4096 * 100

## これはFull-FTの0.007%に相当

## -

## Cons

## -

## Soft Prompt が入力系列を圧

## 迫

## -

## プロンプトエンジニアリング

## の拡張として捉えると、解釈

## 性に欠けた結果となっている

SuperGLUEベンチ

マークによる比較

縦軸:

SuperGLUE Score

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Selective型| BitFit (2021)

## 4. Parameter Efficient Fine-Tuning

37

## 3

[19] Zaken, Elad Ben, et al. (2021), "BitFit: Simple parameter-efficient fine-tuning for

transformer-based masked language-models" より引用し、一部改変

## -

## Transformerの各モジュール

## に含まれる、バイアス項のみに

## ついて学習・更新を実施

## -

## 具体的に、以下に含まれている

## バイアス項が該当

## -

## Attention

## -

## Feed-Forward Network

## -

## Layer Normalization

b: バイアス項

これらのみ学習・更新

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Selective型| BitFit (2021)

## 4. Parameter Efficient Fine-Tuning

38

## 3

[19] Zaken, Elad Ben, et al. (2021), "BitFit: Simple parameter-efficient fine-tuning for

transformer-based masked language-models" より引用し、一部改変

横軸:

学習データ数

縦軸:

Exact Match

赤線: Full-FT

青線: BitFit

## -

## Pros

## -

## 学習データ数が小さい領域で

## は、BitFitがFull-FTよりも高い

## 精度を示した(左図)

## -

## BERT(Base)モデルで、BitFit

## による訓練パラメータ数は、

## Full-FTに対して0.1%ほど

## -

## Cons

## -

## GPT-3 といった、より大規模

## なモデルでは、Full-FT や他の

## PEFT手法よりも精度が劣る[14]

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation

of large language models" より引用

SQuADタスク

BERT FT比較

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization型| LoRA (2021)

## 4. Parameter Efficient Fine-Tuning

39

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large

language models" より引用し、一部改変

## -

## Fine-Tuning によって更新された

## 重みW は一般に、元の重みW0と

## 増分重みΔWの和として表せる

低ランク行列

を2つ導入

-

A: d × r

-

B: r × d

事前学習済み

モデル線形層

重みは固定

Aは正規乱数

で初期化

Bは零行列

で初期化

2つの経路の結果を足し

合わせ、次の層へ伝達

## -

## LoRAでは、この増分重みΔW を

## 2つの低ランク行列A, Bの積とし、

## それらについて学習を実施

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization型| LoRA (2021)

## 4. Parameter Efficient Fine-Tuning

40

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large

language models" より引用し、一部改変

横軸(対数):

訓練パラメータ数

Soft Prompt系手法

(緑・黄) は不安定

LoRA (ピンク)・

Adapter (橙) は

比較的安定

縦軸:

Accuracy

Full-FT

## -

## Pros

## -

## Full-FTに対し10-2から10-4ほど

## 小さい訓練パラメータ数で、

## Full-FTと同等の精度(左図)

## -

## 推論時には、得られた重みを

## 元の重みに予め足しておけ

## ば、オーバーヘッドが生じな

## い

## -

## Cons

## -

## 特に難易度の高いタスク

## (例GSM8k, 数学的推論) で、

## Full-FTに対して著しい

## 性能の劣後が生じうる※

[20] anyscale (2023), “Fine-Tuning LLMs: LoRA or Full-

Parameter? An in-depth Analysis with Llama 2”

WikiSQLタスク

GPT-3 FT比較

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization型| LoRA (2021)

## 4. Parameter Efficient Fine-Tuning

41

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models" より引用し、一部改変

## -

## Q. 訓練パラメータ数を一定としたとき、LoRAを適用する層

## の

## 種類をより増やすべきか、ランクrをより大きく取るべきか

## -

## A. LoRAを適用する層の種類を増やした方が、ランクrが小さ

## く

## なっても、より高い性能となることが示された

## -

## ※ LoRA論文ではAttentionモジュール内を適用対象とした

## が、

## その後の研究では他の線形層も対象とすることで性能が改善

Weight Type

-

q: Query projection

-

k: Key projection

-

v: Value projection

-

o: Output projection

訓練パラメータ数を18Mに固定

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization型| LoRA (2021)

## 4. Parameter Efficient Fine-Tuning

42

## 4

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models" より引用し、一部改変

## -

## Q. LoRAを適用する層の種類を固定して考える場合に、

## ランクrはどの程度の値を設定する必要があるか

## -

## A. LoRAのランクrは、2から8の範囲で性能が高い結果

## -

## ※ (タスク依存だが) ランク1で十分な性能が出る場合も

## 経験的には、ランク8程度の設定が推奨されている

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## Reparametrization型| LoRAの派生アプローチ

## 4. Parameter Efficient Fine-Tuning

43

## QLoRA

## AdaLoRA

## LoRA-Pro

## 目的

## 手法

## 4

## さらに少ない計算リソースによっても

## LoRA によるFine-Tuning を実現したい

## LoRAに4ビット量子化等のテクニック

## を適用し、メモリ使用量をさらに削減

## LoRA において、全ての層のランクが

## 単一の値に制限されている問題の解決

## Full-FTの勾配を近似できていない問題

## を緩和し、Full-FTとの性能差を詰める

## 増分重みの特異値分解に基づいて、

## 層ごとのランクを適応的に変化させる

## LoRAの2つの低ランク行列の勾配がフ

## ル勾配に整合するよう理論的に最適調

## 整

[22] Zhang, Qingru, et al. (2023), "Adaptive budget allocation for parameter-efficient fine-tuning" より引用

[21] Dettmers, Tim, et al. (2023), "QLoRA: Efficient finetuning of quantized LLMs" より引用

[23] Wang, Zhengbo, et al. (2024), "LoRA-Pro: Are low-rank adapters properly optimized?" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 代表的なPEFT 手法の比較

## 4. Parameter Efficient Fine-Tuning

44

## 性能改善

## 運用性

## (更新率※)

## 推論効率

## 訓練効率

## (訓練率※)

## Adapter

## Prompt

## Tuning

## BitFit

## LoRA

不安定な傾向

大規模モデルで劣化

入力系列長を圧迫

推論時間が増加

(タスクに依存)

(タスクに依存)

(0.1 - 6 %)

(0.1 - 6 %)

(0.1 %)

(0.1 %)

(0.05 - 0.1 %)

(0.05 - 0.1 %)

(0.01 - 0.5 %)

(~0.5 %)

[15] Lialin, Vladislav, et al. (2023), "Scaling down to scale up: A guide to parameter-efficient fine-tuning" より引用

(変化なし)

(変化なし)

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## LLM Fine-Tuning

45

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例振り返り| ChatGPT

46

[1] OpenAI(2023), “Introducing ChatGPT”より引用し、一部改変

Supervised Fine-Tuning

= Instruction Tuning

Reinforcement Learning from Human Feedback

(RLHF)

## 5. Day6 まとめ

## -

## ChatGPT ではInstructGPT

## 論文※で提案されたフローに

## 則って、以下の手法を採用

## -

## Supervised Fine-Tuning

## = Instruction Tuning

## -

## RLHF

## -

## InstructGPT では、人間が

## Instruction Tuning 用に

## 1万件強のデータを作成

## -

## これにより、人間的な価値観

## への出力の調整を実現

[2] Ouyang, Long, et al. (2022), "Training language models

to follow instructions with human feedback" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例| OpenAI API Fine-Tuning

## 1. Day6 イントロダクション

47

[3] OpenAI(2024), “Fine-tuning now available for GPT-4o” より引用

## -

## OpenAI API では、Fine-

## Tuning 機能が提供

## -

## 自前のデータセットを用いた

## Fine-Tuning が実施可能

## -

## 以下のような用途が例示

## -

## 出力フォーマットの固定

## -

## 画像理解＋テキスト出力

## -

## レイアウト一貫性の強化

## -

## Prompting と比較して、

## 以下のような利点が例示

## -

## トークン・処理時間節約

## -

## 応答の品質・制御性向上

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## LLM Fine-Tuning 事例| Med-Gemini

## 1. Day6 イントロダクション

48

## -

## Med-Gemini※ :

## -

## Google が開発した大規模言語モデルGemini を医療向けに特化させたモデル

## -

## 医療領域でのマルチモーダル能力が強化され、各種ベンチで強力な結果を報告

[4] Saab, Khaled, et al. (2024), "Capabilities of gemini models in medicine" より引用

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデル基礎Day6 の目標

## 大規模言語モデルの典型的な訓練フローにおいて、Fine-Tuning が

## Pre-Training やRLHF・DPO に対してどう位置付けられるか説明できる

## 大規模言語モデルのFine-Tuning において、特に重要なアプローチである

## Instruction Tuning やPEFT が既存手法に対してどう異なるか説明できる

## Goal 1

## Goal 2

## Goal 3

49

## Instruction Tuning およびPEFT について、その目的や内容を十分に理解

## した上で実際にそれらを実装し、大規模言語モデルの性能改善を実現できる

## 5. Day6 まとめ

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## 大規模言語モデルFine-Tuning

## 大規模言語モデル基礎Day6

## 目次

## 01

## 03

## 04

## Parameter Efficient Fine-Tuning

## Instruction Tuning

## Day6 まとめ

## 05

## Day6 イントロダクション

## 02

## 大規模言語モデルのFine-Tuning

50

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

51

[1] OpenAI (2023), "Introducing ChatGPT", https://openai.com/ja-JP/index/chatgpt/ アクセス日:2026/5/24

[2] Ouyang, Long, et al. (2022), "Training language models to follow instructions with human feedback", Advances in Neural

Information Processing Systems 35, pp. 27730-27744

[3] OpenAI (2024), "Fine-tuning now available for GPT-4o", https://openai.com/ja-JP/index/gpt-4o-fine-tuning/ アクセス日:2026/5/24

[4] Saab, Khaled, et al. (2024), "Capabilities of gemini models in medicine", arXiv:2404.18416

[5] PyTorch Tutorial, "Dynamic Quantization on BERT", https://docs.pytorch.org/tutorials/index.html アクセス日:2026/5/24

[6] Wei, Jason, et al. (2021), "Finetuned language models are zero-shot learners", arXiv:2109.01652

[7] Google Research (2021), "Introducing FLAN: More generalizable Language Models with Instruction Fine-Tuning",

https://research.google/blog/introducing-flan-more-generalizable-language-models-with-instruction-fine-tuning/ アクセス日

:2026/5/24

[8] HuggingFace, "flan2021_submix_original", https://huggingface.co/datasets/conceptofmind/flan2021_submix_original アクセス日

:2026/5/24

[9] Taori, Rohan, et al. (2023), "Alpaca", Stanford Center for Research on Foundation Models,

https://crfm.stanford.edu/2023/03/13/alpaca.html アクセス日:2026/5/24

[10] Zhou, Chunting, et al. (2023), "Lima: Less is more for alignment", arXiv:2305.11206

[11] Touvron, Hugo, et al. (2023), "Llama 2: Open foundation and fine-tuned chat models", arXiv:2307.09288

[12] Sanh, Victor, et al. (2021), "Multitask prompted training enables zero-shot task generalization", arXiv:2110.08207

[13] Wang, Yizhong, et al. (2022), arXiv:2212.10560

LLM 大規模言語モデル講座講義資料© 2025 by 東京大学松尾・岩澤研究室is licensed under CC BY-NC-ND 4.0

©︎MATSUO-IWASAWA LAB, THE UNIVERSITY F TOKYO

## References

52

[14] Hu, Edward J., et al. (2021), "LoRA: Low-rank adaptation of large language models", arXiv:2106.09685

[15] Lialin, Vladislav, Vijeta Deshpande, and Anna Rumshisky (2023), "Scaling down to scale up: A guide to parameter-efficient

fine-tuning", arXiv:2303.15647

[16] Houlsby, Neil, et al. (2019), "Parameter-efficient transfer learning for NLP", International Conference on Machine Learning,

PMLR

[17] He, Junxian, et al. (2021), "Towards a unified view of parameter-efficient transfer learning", arXiv:2110.04366

[18] Lester, Brian, Rami Al-Rfou, and Noah Constant (2021), "The power of scale for parameter-efficient prompt tuning",

arXiv:2104.08691

[19] Zaken, Elad Ben, Shauli Ravfogel, and Yoav Goldberg (2021), "BitFit: Simple parameter-efficient fine-tuning for

transformer-based masked language-models", arXiv:2106.10199

[20] anyscale (2023), "Fine-Tuning LLMs: LoRA or Full-Parameter? An in-depth Analysis with Llama 2",

https://www.anyscale.com/blog/fine-tuning-llms-lora-or-full-parameter-an-in-depth-analysis-with-llama-2 アクセス日

:2026/5/24

[21] Dettmers, Tim, et al. (2023), "QLoRA: Efficient finetuning of quantized LLMs", arXiv:2305.14314

[22] Zhang, Qingru, et al. (2023), "Adaptive budget allocation for parameter-efficient fine-tuning", arXiv:2303.10512

[23] Wang, Zhengbo, et al. (2024), "LoRA-Pro: Are low-rank adapters properly optimized?", arXiv:2407.18242
