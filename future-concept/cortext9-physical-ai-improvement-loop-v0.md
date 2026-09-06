# Cortext9 Physical AI Improvement Loop v0

- 文書種別: デモ方針草案（Draft）
- 版: v0
- 状態: Kが実装方針として採用（2026-09-07）。Future Concept 最終確定ではない
- 正本: https://github.com/qooyanz-bot/talk-data
- 経緯: `changelog/2026-09-07-newmo-physical-ai-demo-session.md`
- エージェント指示: `future-concept/handoffs/2026-09-07-grok-physical-ai-loop-agent-prompt.md`

## 0. 目的と非目的

### 目的
1. newmo 向けに、技術面談で即触れる最高水準デモを作る。
2. その機能を、Cortext9 が作るあらゆるロボットへ本質転用できる形で優先実装する。
3. 「AIで動く」ではなく、「実世界で壊れながら安全に賢くなる基盤」を見せる。

### 非目的
- Future Concept / H1 の意味改訂
- 実車・実機の未実施結果を成功として主張すること
- 秘密データや未観測事実の確定偽証

## 1. 一文定義

**Cortext9 Physical AI Improvement Loop** とは、実機ログから失敗を資産化し、Closed-Loop 再現と Safety Filter で改善前後を比較し、次の収集・学習・評価までつなぐ、ロボット横断の Physical AI 改善基盤である。

## 2. エンドツーエンド流れ

```
実機ログ / 動画
  → Incident / Hazard / Failure 抽出
  → Closed-Loop Failure Replay
  → E2E / VLA 行動出力
  → Safety Filter / Intent Shield 補正
  → Before / After 定量比較
  → 再収集・再学習・評価タスク生成
```

## 3. 優先開発リスト（汎用性最優先）

順序は「あらゆるロボットに効くか」を最優先した。

### P0 — デモの一本化に必須
1. **Safety Filter / Intent Shield**
   - E2E/VLA の行動をそのまま実行せず、物理・衝突・人距離・速度制約でリアルタイム補正する。
   - 応用: 車、AMR、アーム、配送、ドローン。
2. **Closed-Loop Failure Replay Simulator**
   - 失敗ログを同条件で再現し、改善前後を比較する。
3. **Incident-to-Training Loop**
   - ヒヤリハット/停止を評価シナリオ・再学習候補・テストケースへ変換する。

### P1 — 基盤品質と説得力
4. **Data Quality Autopilot**
   - 同期ズレ、欠損、フレームドロップ、GNSSロスト、ネットワーク瞬断を自動検出。
5. **Semantic Perception Layer**
   - 物体名だけでなく「通れる / 待つべき / 触れてよい / 危険」など行動可能性表現。
6. **Human-Readable Autonomy Debugger**
   - なぜ止まったか、どのセンサーが怪しいか、どの安全制約が発火したかを説明。

### P2 — 運用説得力
7. **Edge-to-Lab Robot Fleet Pipeline**
   - 収集 → メタデータ → 品質検査 → 圧縮 → アップロード → 学習/評価キュー。

## 4. newmo 寄せ（推定・要再確認）

参照入口:
`https://herp.careers/v1/newmo/requisition-groups/f125051c-eb4d-4930-8bb9-dfb0394f9fcb`

先行分析上、求人群は次を強調している（公開求人の読解に基づく推定。個別JDの文言は実装前に再確認すること）:
- End-to-End モデル
- Perception / 下流が扱いやすい表現
- 車載データ収集と高速フィードバック
- 車両制御・最適制御
- E2E 出力への安全フィルタ・軌道修正
- Photo-Realistic Closed-Loop シミュレータ
- Field Integration / 現場と開発の情報整合

本デモは上記に「寄せる」が、Cortext9 汎用ロボット基盤を犠牲にして車専用に閉じない。

## 5. デモ成功条件（v0）

面談で 5–10 分で次が見えること。

1. サンプル失敗ログを選ぶ
2. 危険/失敗区間が自動抽出される
3. シミュレータ上で再現される
4. Safety Filter OFF/ON で軌道と指標が変わる
5. 改善前後の定量差（衝突余裕、制約違反回数、成功率など）が出る
6. 「次に集めるべきデータ / 次のテスト」が生成される

## 6. 実装メモ（現状）

- 作業ディレクトリ:
  `C:\Users\qooya\Documents\Codex\2026-09-07\https-herp-careers-v1-newmo-requisition\work\cortext9-physical-ai-loop`
- 現状: sites スターター生成済み、デモロジック未実装
- 推奨: まずローカル Web デモとしてサンプルデータ駆動で P0 を通し、後で専用 GitHub リポへ分離

## 7. 品質ゲート（実装時）

- 仮説と観測を UI / README で混同しない
- 「実機検証済み」は実機ログがある場合のみ表示
- 危険指示デモでも、Safety Filter が常に最終実行権限を持つことを明示
- 秘密・個人識別不要データをリポに入れない
- force-push 禁止。破壊的削除禁止

## 8. 未決

- 専用実装リポジトリ名（候補: `cortext9-physical-ai-loop`）
- 実機データの有無（当面は合成ログで可）
- newmo 提出物の最終形態（ライブデモ / 録画 / リポ URL）
- Cortext9 Reception / Tiny runtime との接続有無（初期は独立でよい）
