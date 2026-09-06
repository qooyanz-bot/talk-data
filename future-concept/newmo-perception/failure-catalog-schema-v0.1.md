# (B) Perception 失敗条件カタログ — 雛形

- 版: v0.1（K承認 2026-09-06）
- 正本: talk-data canonicalization / README.md
- 記入済みシード: `B-failure-catalog-F001-F010.md`
- 目的: 感想の「苦手」を、再現・計測・改善可能な失敗条件にする
- 運用: 新規は提案→短いゲート点検→承認後に追記。月1回以上発火しない条件は deprecate 候補

## 1. カタログ・メタ

| 項目 | 値 |
|---|---|
| 文書ID | `perception-failure-catalog` |
| 版 | v0.1（K承認 2026-09-06） |
| 対象スタック | camera / LiDAR / (optional radar) → Perception → E2E / Planning |
| 座標系 | ego / map（採用した方を明記） |
| 更新周期 | 週次レビュー、実車キャンペーン後は都度 |

## 2. 条件エントリ・スキーマ（1件ぶん）

```yaml
id: F-XXX                    # 例: F-012
title: 短い名前              # 例: 逆光下の近傍歩行者ロスト
status: candidate|active|deprecated
severity: P0|P1|P2           # P0=不可逆寄り / P1=運用阻害 / P2=品質
modality: [camera, lidar, fusion, calib, sync]
scene_tags: [urban, night, rain, glare, occlusion, highway, ...]

# 定義（必須）
definition: |
  何がどう失敗したかを1段落で。仮説と観測を混ぜない。

# 再現（必須）
repro:
  log_query: "時間帯・天候・センサ・ロケの検索条件"
  min_examples: 3
  synthetic_ok: true|false   # 実車が無いときの代替可否
  steps: |
    1. ...
    2. ...

# 観測指標（必須・二重帳簿）
metrics:
  offline:
    - name: miss_rate_ped_near
      formula: "距離<Rの歩行者で検出欠落率"
      threshold_bad: ">= X%"
  onboard_or_sim:
    - name: time_to_recapture
      formula: "ロストから再捕捉までの秒"
      threshold_bad: ">= Y s"
  safety_proxy:
    - name: near_miss_margin
      note: "ソフト損失に溶かさない。ゲート参照"

# 既知の原因仮説（候補。確定偽証しない）
hypotheses:
  - id: H1
    text: "HDR不足によるシルエット消失"
    status: open|supported|rejected
  - id: H2
    text: "LiDAR点群疎＋融合で歩行者が占有から消える"
    status: open

# 改善レバー（微小介入を優先）
levers:
  - type: data      # data|model|calib|pipeline|contract
    action: "逆光難例のオートラベル再学習セット追加"
    expected_effect: "F-XXX の miss_rate を相対Z%改善"
    verification: "同一評価セット＋新規実車週次"

# Hard Reject との関係
hard_reject:
  triggers_gate: true|false
  gate_id: "HR-pedestrian-disappear"  # あれば
  may_not_be_overridden_by_model_score: true

# リンク
links:
  example_logs: []
  related_failures: [F-00Y]
  e2e_contract_fields: ["occ_uncertainty", "dynamic_tracks"]
```

## 3. 初期シード（記入例・要実測で差し替え）

| ID | title | severity | modality |
|---|---|---|---|
| F-001 | 外参ドリフトによるBEVずれ | P0 | calib |
| F-002 | カメラ–LiDAR時刻ずれ | P0 | sync |
| F-003 | 逆光下の近傍歩行者ロスト | P0 | camera/fusion |
| F-004 | 大型車遮断下の横断歩行者遅延検出 | P0 | camera/lidar |
| F-005 | 雨天の地面反射ゴースト | P1 | lidar |
| F-006 | 夜間ヘッドライトフレア誤検出 | P1 | camera |
| F-007 | 静止障害（工事コーン）の消滅 | P0 | fusion |
| F-008 | 希少クラス（車椅子・幼児車）の系統的欠落 | P0 | data |
| F-009 | 急減速先行車のトラッキングID破綻 | P1 | track |
| F-010 | 対向二輪の距離過大推定 | P0 | camera/fusion |

各IDは上記YAMLを1ファイルまたは1セクションで埋める。空欄のまま「active」にしない。

## 4. レビューチェック（短いゲート）

- [ ] 定義に仮説断定が入っていない
- [ ] 再現手順またはログクエリがある
- [ ] offline と onboard/sim の指標が両方ある（または欠落理由）
- [ ] P0は Hard Reject／ゲート参照がある
- [ ] 改善レバーが「大モデル入替のみ」になっていない（微小介入が1つ以上）
- [ ] 秘密・個人が特定できる生データをリンクしていない

## 5. deprecate 規則

- 8週間、実車・評価で発火ゼロ → deprecate候補
- 発火ゼロでもP0は残し、監視頻度だけ下げる選択可
- 消さず `status: deprecated` ＋代替IDを残す
