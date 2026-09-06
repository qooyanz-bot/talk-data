# newmo Physical AI デモ経緯 — 2026-09-07

- 文書種別: Chat-derived record / changelog
- 版: v0.1
- 状態: K（亀田紀明）の明示保存指示により記録
- 正本リポジトリ: https://github.com/qooyanz-bot/talk-data
- 関連草案: `future-concept/cortext9-physical-ai-improvement-loop-v0.md`
- Grok引き継ぎ: `future-concept/handoffs/2026-09-07-grok-physical-ai-loop-agent-prompt.md`

## 1. 保存対象

2026-09-07 の対話から、再利用可能な経緯・方針・実装状態を要約した。
会話全文の無差別転載ではなく、次担当エージェントが継続できる設計情報を記録する。

## 2. 観測事実（確定として書いてよい範囲）

1. Kは newmo の求人グループを参照した:
   `https://herp.careers/v1/newmo/requisition-groups/f125051c-eb4d-4930-8bb9-dfb0394f9fcb`
2. Kの明示目標: 同社向けに最高水準のデモを作り、開発費が稼げる可能性を探る。
3. Kの制約: 機能は本質的に Cortext9 社が開発するあらゆるロボットにも応用できるものから最優先する。
4. 先行エージェント（Codex）がデモ方針として **Cortext9 Physical AI Improvement Loop** を提案し、Kが「提案を採用します全部最高水準まで開発実装を自律的に開始」と指示した。
5. 実装着手先:
   `C:\Users\qooya\Documents\Codex\2026-09-07\https-herp-careers-v1-newmo-requisition\work\cortext9-physical-ai-loop`
6. 同ディレクトリには `@openai/sites` 系スターター（Next/Vite + shadcn）が生成済み。`app/page.tsx` は骨格プレースホルダのまま。デモ本体ロジックは未実装。
7. Codex が利用制限に達し、経緯の GitHub 保存と Grok 引き継ぎプロンプト作成の途中で停止した。
8. Kは「今までの経緯を全てGithubに保存してGrokにエージェントを担当させるプロンプトを書け」と明示した（本記録の根拠）。

## 3. 戦略・仮説（確定事実ではない）

以下は採用デモ方針の草案であり、Future Concept 最終版でも、newmo 採用保証でもない。

- 見せ方の核: モデル単体の賢さより、「実世界で失敗を回収し、安全に改善し続けるロボット基盤」。
- 一本化デモ名: **Cortext9 Physical AI Improvement Loop**
- ループ:
  実機ログ/動画投入
  → 異常・危険・失敗場面の自動抽出
  → Closed-Loop シミュレーション再現
  → E2E/VLA 出力を Safety Filter で補正
  → 改善前後の定量比較
  → 次の収集・学習・評価タスク自動生成
- 優先機能（Cortext9 全ロボット汎用を最優先）:
  1. Safety Filter / Intent Shield
  2. Closed-Loop Failure Replay Simulator
  3. Data Quality Autopilot
  4. Incident-to-Training Loop
  5. Semantic Perception Layer
  6. Human-Readable Autonomy Debugger
  7. Edge-to-Lab Robot Fleet Pipeline

求人寄せの根拠（公開求人からの推定・未検証の解釈を含む）:
- newmo 自動運転開発室は E2E、Perception、車載データ、車両制御、最適制御、Closed-Loop シミュレータ、Field Integration を強く求める記述が多い、という先行分析。
- 詳細本文は草案側に分離する。仮説と観測を混同しない。

## 4. 実装状態（2026-09-07 時点）

| 項目 | 状態 |
|---|---|
| 方針合意 | K採用済み（実装開始指示あり） |
| Web スターター生成 | 完了 |
| デモ UI / ループ実装 | 未着手（page はスケルトン） |
| 専用 GitHub 実装リポ | 未作成 |
| talk-data 正本への経緯保存 | 本 changelog で実施 |
| Grok 担当プロンプト | `future-concept/handoffs/` に配置 |

## 5. 除外

- パスワード、APIキー、秘密鍵、未公開個人識別に不要な生データ
- H1 / Future Concept の意味改訂
- 「採用される」「開発費が必ず稼げる」などの未観測断定
- 実車・実機での未実施評価結果の捏造

## 6. 次回扱い

- 実装継続は Grok エージェントが `future-concept/handoffs/2026-09-07-grok-physical-ai-loop-agent-prompt.md` に従う。
- 方針の意味改訂や Future Concept への昇格は、canonical-add-rules-v1 の承認手順が必要。
- 本記録自体は会話継続用の要約であり、未承認の Future Concept 最終版ではない。

---
記録日: 2026-09-07 JST
記録者役割: AI Recorder（Grok）
承認根拠: K明示「経緯を全てGithubに保存」
