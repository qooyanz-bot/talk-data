# Selective Escalation Experiment

- 作成日時 (UTC): 2026-08-28T15:33:32.0000000Z
- 更新日時 (UTC): 2026-08-28T15:34:10.0000000Z
- 注記: 本文は公開用に秘密形式・メールアドレス・電話番号のみ不可逆に伏せ字化。

## assistant / 2026-08-28T15:33:34.0000000Z

````
はい。ここで検証しようとしているのは、これまでの研究の中でもかなり重要な仮説です。

一言でいうと、

> **「100問すべてを巨大LLMに解かせる必要はなく、90問くらいを極小システムで処理し、本当に難しい10問だけ巨大LLMへ渡せないか？」**

を、まずAPI課金もGPUも使わずに実験するものです。

これは単なる思いつきではなく、LLM cascade / learning-to-defer / model routing と呼ばれる研究領域とかなり近いです。たとえばFrugalGPTでは、安価なモデルから高価なモデルへ必要時だけcascadeすることで、特定の実験条件では高性能モデル相当の性能を保ちながら大幅なコスト削減が報告されています。2026年にもこの方向のrouting/defer研究が続いています。citeturn0academia24turn0academia28turn0search8

ただし、今回の実験にはそれらとは少し違う重要なポイントがあります。

## 1. まずA/B/Cの意味

1,000問の新しい問題セットを作ったとします。

### A. FRONTIER-ALL

現在の普通の高性能AIサービスに近い比較対象です。

```text
Question
   ↓
Frontier Model
   ↓
Answer
```

1,000問なら、

```text
Frontier call = 1,000回
```

CPU実験では実際のGPT-5級モデルを呼ばず、

```text
正解を返すOracle
```

をFrontierの代理にします。

したがって、仮にOracleが100%正解すると、

```text
Success       1,000 / 1,000
Frontier Call 1,000
Call Rate     100%
Cost          1,000 units
```

これが基準です。

---

### B. SMALL-ONLY

反対側の極端です。

```text
Question
   ↓
Small Hierarchical System
   ↓
Answer
```

Frontierを一切使いません。

ここでいうSmall Systemは、単なる小型LLMではなく、

```text
State + Goal
      ↓
Representation
      ↓
Selection
      ↓
Typed Program
      ↓
Validator
      ↓
Execution
```

という、これまで実験してきた**分解されたシステム**です。

仮に、

```text
Success       750 / 1,000
Frontier Call 0
Cost          極小
```

となったとします。

安いけれど25%失敗するので、これだけではFrontierの代替になりません。

---

### C. SELECTIVE

ここが今回の本命です。

```text
                 ┌→ 自信あり → Smallで回答
Question → Small ┤
                 └→ 危険/不明 → Frontierへ
```

つまりSmall Systemには、

**「答える能力」だけでなく「自分では処理すべきでない問題を検出する能力」**

を持たせます。

これが非常に重要です。

## 2. 実はSmallの正答率そのものより「失敗検知能力」が重要

例えばSmall Systemの正答率が80%だったとします。

普通なら、

> 20%間違えるから使えない。

となります。

でも、その20%を事前にほぼ検出できるなら話が変わります。

```text
1000 tasks

Smallで正しく処理             800
Smallが「これは無理」と判断    200
                               ↓
                            Frontier
                               ↓
                            正しく処理
```

最終結果：

```text
Task Success       ≈100%
Frontier Calls       200
Frontier Call Rate    20%
```

つまり、

**Frontierの能力をほぼ維持しながら、Frontierを80%呼ばなくてよくなる。**

今回のPrimary Hypothesisはこれを少し保守的にして、

```text
SELECTIVE Success
≥ FRONTIER-ALL − 2 percentage points

かつ

Frontier Call Rate
≤ 30%
```

としています。

例えばFRONTIER-ALLが1000/1000なら、

```text
SELECTIVE ≥ 980/1000
Frontier calls ≤ 300
```

ならPASSです。

## 3. なぜ1,000問を4種類に分けるのか

ここも実験として重要です。

最初から例えば、

| Difficulty | 例 | Smallに期待すること |
|---|---|---|
| Easy | 単純な既知操作 | 自力処理 |
| Medium | 複数操作 | なるべく自力処理 |
| Hard | 長いcomposition | 必要ならEscalate |
| Structurally unsupported | Smallに存在しない操作 | **必ずEscalate** |

と固定します。

最後の `structurally unsupported` が特に重要です。

Small Systemが知らない問題に対して、

> 分かりません。Frontierに渡します。

と言えるかを測れるからです。

これはLLMのhallucination問題ともかなり関係します。

「何でも答えるAI」ではなく、

**「自分が処理可能な領域を認識するAI」**

を作るわけです。

## 4. Escalationは正解を見て決めてはいけない

これは研究上の最大の注意点の一つです。

Small Systemが、

```text
Gold answerを見る
↓
自分の答えが間違っている
↓
Frontierへ送る
```

では実験になりません。

実運用ではGold answerが存在しないからです。

そこで、事前に決めたsignalだけを使います。

```text
invalid program
validator failure
low confidence
representation collision
unsupported primitive
execution inconsistency
verification failure
```

例えば、

```text
Question
 ↓
Representation
 ↓
Selector confidence = 0.93
 ↓
Typed Program = valid
 ↓
Validator = PASS
 ↓
Execution = consistent
 ↓
LOCAL ANSWER
```

一方、

```text
Selector confidence = 0.41
        ↓
     ESCALATE
        ↓
     Frontier
```

となります。

この**Escalation policy自体が今回の研究対象**です。

## 5. 最も重要なのはFalse Non-Escalation

SELECTIVEの結果は5種類に分類します。

```text
① correctly solved locally
   Smallが処理 → 正解

② correctly escalated
   Smallが危険判定 → Frontier → 正解

③ unnecessarily escalated
   Smallでも正解できたのにFrontierへ送った

④ should-have-escalated but did not
   Smallが自信を持って回答 → 間違い

⑤ escalated but still failed
   Frontierまで失敗
```

特に危険なのが④です。

たとえば、

```text
Small success = 70%
```

でも、残り30%を全部検知できれば非常に優秀なrouterです。

逆に、

```text
Small success = 90%
```

でも、残り10%の失敗を全く検知できなければ、信頼性が必要な用途では厳しい。

したがって今回、

**Small model accuracyだけを競わせない**

設計にしたことには意味があります。

## 6. 「30%以下」が意味するもの

仮に結果が、

```text
FRONTIER-ALL
1000/1000
Frontier = 1000

SMALL-ONLY
820/1000
Frontier = 0

SELECTIVE
987/1000
Frontier = 184
```

だったとします。

SELECTIVEは、

```text
Accuracy = 98.7%
Frontier Call Rate = 18.4%
```

です。

Frontierだけを見ると、

```text
1000 → 184
```

なので、

**81.6%のFrontier処理を回避**

できています。

これが今回検証したい「巨大モデルを毎回使わないArchitecture」の意味です。

実際、FrugalGPTでも「安価なモデル→必要なら高価なモデル」というcascadeで大幅なコスト削減が示されており、2026年のConformal Cascadeなどでは、confidence routingそのものの信頼性・calibrationをさらに厳密に扱う方向へ研究が進んでいます。citeturn0academia24turn0academia26

## 7. ただし今回のCost Unitには注意が必要

今回、

```text
Frontier = 1.0 cost unit / call
```

とします。

仮に、

```text
FRONTIER-ALL = 1000 units
SELECTIVE = Small処理コスト + 180 units
```

なら、

```text
SELECTIVE / FRONTIER-ALL ≈ 0.18 + Small Cost
```

となります。

ただしこれは、

**「OpenAI API料金を82%削減できた」**

という意味ではありません。

FrontierはOracle proxyだからです。

今回言えるのは、

> **同じ仕事を達成するために、高コスト推論層を呼ぶ必要がある割合をどこまで減らせるか**

だけです。

ここは論文を書く場合にもかなり厳密に区別した方がいいです。

## 8. なぜ既存Holdoutを使わないのか

これまでR1/R2などを何度も分析しています。

既存Holdoutをここで使うと、

```text
研究者が過去の結果を知っている
↓
設計判断に間接的に情報が入る
↓
本当の未知データ評価ではなくなる
```

可能性があります。

そこで今回、

```text
既存R0〜R5 → Freeze

既存Holdout → 触らない

Selective専用
Development 1000+ → 新規作成
```

としています。

Development上で、

```text
confidence threshold
validator rule
escalation policy
```

を決定する。

それがFreezeして初めて、

```text
新規 Sealed Holdout
```

を作る。

これは研究として正しい順序です。

## 9. この実験がPASSした場合、何が分かるか

ここは重要なので、主張の強さを分けます。

### PASSしてもまだ言えない

```text
❌ Frontier LLMは不要
❌ GPT-5級性能を小型モデルで再現した
❌ 推論コストを実世界で80%削減した
❌ 4090でFrontier Modelを置換できる
```

ここまでは全く言えません。

### PASSすると言える

```text
✓ benchmark上では
  全taskを高コストexecutorへ送る必要がなかった

✓ 小型system自身のsignalだけから
  高コスト処理が必要なtaskをかなり選別できた

✓ selective escalation architectureによって
  高コストexecutor utilizationを大幅に削減しつつ
  task successをほぼ維持できた
```

これは十分意味があります。

## 10. そして、今回の研究全体との接続が面白い

これまでの研究は少しずつ、

```text
巨大NN
  ↓
全部を内部で解く
```

から、

```text
        ┌ Representation
        ├ Selection
Goal →  ├ State
        ├ Program
        ├ Validator
        ├ Executor
        └ Frontier fallback
```

へ移っています。

つまり研究仮説をより大きくすると、

> **知能の全機能を一つの巨大ニューラルネットワークに保持する必要はなく、安価な専門componentを組み合わせ、解けない部分だけ高能力モデルへ委譲すればよいのではないか。**

になります。

Selective Frontier Experimentは、この仮説の中でも特に**経済性を直接測る最初の実験**です。

しかも、この方向には既存研究の裏付けがあります。FrugalGPTはcascadeによるコスト削減、Online Cascade Learningは小型モデルからLLMへのdeferで最大90%程度の推論コスト削減を報告し、2026年のrouting surveyでも「routine queryは小型、complex taskは大型」というdynamic routingが主要研究領域として整理されています。citeturn0academia24turn0search9turn0academia28

一方で、**あなたの実験で重要なのは「既存研究でもcascadeが効いた」ことではありません。** R1で既に見えている Representation → Selection → Typed Program → Validator → Execution という構造化Small Systemから得られる内部failure signalだけで、Frontierへのdeferを正確に決定できるか、です。ここが成立すれば、単なる「小さいLLM→大きいLLM」のcascadeより研究として面白くなります。

私はこの実験では、最終的な `≤30%` だけでなく、**Frontier Call Rateを横軸、Task Successを縦軸にしたPareto curve**を必ず保存するのが重要だと考えます。30%、20%、10%で何が起きるかを見ると、「Frontierをどこまで削ると急激に知能が壊れるか」という境界が見えるからです。そこが、このArchitectureの実用価値を判断するかなり重要な数字になります。memcite
````

## assistant / 2026-08-28T15:33:34.0000000Z

```
null
```

## assistant / 2026-08-28T15:33:34.0000000Z

```
null
```
