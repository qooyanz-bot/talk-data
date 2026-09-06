# Perception失敗条件 F-001〜F-010 記入済み v0.1 K承認 2026-09-06

- 文書ID: `B-failure-catalog-F001-F010`
- 版: v0.1（K承認 2026-09-06）
- **注記（必読）:** 本エントリは日本都市タクシー／newmo 類似スタック向けの **ODDシード** である。特定雇用主での観測インシデントの主張ではない。閾値はすべて暫定 【仮閾値・要実測】。ログパス・実測値は 【要差し替え：Kが実数・固有名詞を記入】。
- スキーマ出典: `B-failure-catalog-template.md`
- 対象スタック: camera / LiDAR → Perception → E2E / Planning
- 座標系: ego（BEVは ego 原点。map 併用時はエントリ内で明記）

---

## F-001 外参ドリフトによるBEVずれ

```yaml
id: F-001
title: 外参ドリフトによるBEVずれ
status: active
severity: P0
modality: [calib]
scene_tags: [urban, calibration_drift, temperature_cycle, vibration]

definition: |
  カメラまたはLiDARの外参が基準校正からずれ、同一時刻の観測をego/BEVへ投影したときに
  静的構造物・レーン・他センサ投影が系統的にずれる。仮説（温度・振動・取付緩み等）は
  定義に含めず、観測された幾何不一致として扱う。

repro:
  log_query: "calib_ok=false OR drift_score>=閾値; 都市一般道; 直近校正からの経過距離/時間でフィルタ"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 基準外参版と現行外参版で同一ログを再投影する。
    2. 静的目印（標識柱・縁石）のカメラ投影とLiDAR点のBEV距離を測る。
    3. ずれが持続する区間をクリップ化し、F-001としてタグ付けする。

metrics:
  offline:
    - name: bev_static_align_err_m
      formula: "静的目印のカメラ投影とLiDAR投影のBEVユークリッド誤差中央値"
      threshold_bad: ">= 【仮閾値・要実測】0.3 m"
  onboard_or_sim:
    - name: calib_gate_trip_rate
      formula: "走行時間あたり calib_ok=false または drift_score 超過の比率"
      threshold_bad: ">= 【仮閾値・要実測】1%/h"
  safety_proxy:
    - name: near_miss_margin
      note: "幾何不良フレームを学習・自律許可に混ぜない。ソフト損失に溶かさない"

hypotheses:
  - id: H1
    text: "温度サイクルによるブラケット変形"
    status: open
  - id: H2
    text: "振動によるねじ緩み・外参ファイルの版不一致"
    status: open

levers:
  - type: calib
    action: "外参版管理の強制＋起動時/定周期の静的目印ドリフトチェック"
    expected_effect: "F-001 発火区間の学習混入をゼロ化"
    verification: "同一評価セット再投影＋週次実車キャンペーン"
  - type: pipeline
    action: "drift_score を入力契約メタに載せ、train_eligible=false にする"
    expected_effect: "不良幾何のサイレント学習を防止"
    verification: "trainバケット監査"

hard_reject:
  triggers_gate: true
  gate_id: "HR-calib-drift"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-002, F-007]
  e2e_contract_fields: ["calib.calib_ok", "calib.drift_score", "bev.occ_uncertainty"]
```

---

## F-002 カメラ–LiDAR時刻ずれ

```yaml
id: F-002
title: カメラ–LiDAR時刻ずれ
status: active
severity: P0
modality: [sync]
scene_tags: [urban, high_speed_relative, sync, motion_blur]

definition: |
  同一フレームとして扱われたカメラ画像とLiDARスキャンの時刻差が大きく、
  動物体の投影位置が系統的にずれる、または融合残差が急増する。
  「検出精度が悪い」ではなく、時刻同期の入力契約違反として定義する。

repro:
  log_query: "camera_lidar_skew_ms の絶対値 >= 閾値; 相対速度が高い区間; sync_ok=false"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 各センサの timestamp_ns から skew を再計算する。
    2. 動物体（先行車・二輪）について、画像バウンディングと点群クラスタのBEVずれを測る。
    3. skew を補正した再同期結果と比較し、ずれが skew 由来か確認する。

metrics:
  offline:
    - name: cam_lidar_skew_ms_p95
      formula: "フレームごとの |camera_lidar_skew_ms| の95パーセンタイル"
      threshold_bad: ">= 【仮閾値・要実測】20 ms"
  onboard_or_sim:
    - name: sync_gate_trip_rate
      formula: "sync_ok=false のフレーム比率"
      threshold_bad: ">= 【仮閾値・要実測】0.5%"
  safety_proxy:
    - name: dynamic_projection_err_m
      note: "動物体の投影誤差が増えた区間は自律許可を落とす候補"

hypotheses:
  - id: H1
    text: "ソフト同期のバッファ遅延・ドロップ"
    status: open
  - id: H2
    text: "LiDAR内部モーション補正とカメラ露光中心の定義不一致"
    status: open

levers:
  - type: pipeline
    action: "ハード／ソフト同期の健全性をゲート化し、skew超過を学習分離"
    expected_effect: "F-002 混入学習の削減"
    verification: "skewヒストグラム週次＋同一ログ再同期"
  - type: contract
    action: "入力契約に camera_lidar_skew_ms と sync_ok を必須化"
    expected_effect: "下流が不良同期を黙って使えない"
    verification: "契約適合率監査"

hard_reject:
  triggers_gate: true
  gate_id: "HR-time-sync"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-001, F-009, F-010]
  e2e_contract_fields: ["sync.camera_lidar_skew_ms", "sync.sync_ok", "residuals.cam_lidar_depth_disagree"]
```

---

## F-003 逆光下の近傍歩行者ロスト

```yaml
id: F-003
title: 逆光下の近傍歩行者ロスト
status: active
severity: P0
modality: [camera, fusion]
scene_tags: [urban, glare, pedestrian, near_field, dawn_dusk]

definition: |
  逆光・強い光源を背景にした近傍（近距離帯）の歩行者が、検出・占有・トラックのいずれかで
  欠落または存在確率が急落し、再捕捉まで空白が続く。原因仮説は定義に混ぜない。

repro:
  log_query: "時間帯=朝夕; glare/HDRメタ; 距離<近傍Rの歩行者GTまたは疑似GT; missまたはexists_prob低下"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 逆光タグ付きログから近傍歩行者区間を抽出する。
    2. フレーム単位で miss / ロスト継続時間を計測する。
    3. LiDARのみ占有が残っているかを residuals で確認する（仮説検証は別セクション）。

metrics:
  offline:
    - name: miss_rate_ped_near_glare
      formula: "距離<R【仮閾値・要実測】の歩行者における検出欠落率"
      threshold_bad: ">= 【仮閾値・要実測】5%"
  onboard_or_sim:
    - name: time_to_recapture_s
      formula: "ロストから再捕捉までの秒"
      threshold_bad: ">= 【仮閾値・要実測】0.5 s"
  safety_proxy:
    - name: near_miss_margin
      note: "歩行者ロストはソフト損失に溶かさない。ゲート参照"

hypotheses:
  - id: H1
    text: "HDR不足によるシルエット消失"
    status: open
  - id: H2
    text: "LiDAR点群疎＋融合で歩行者が占有から消える"
    status: open

levers:
  - type: data
    action: "逆光難例のオートラベル／人手確認セット追加と再学習"
    expected_effect: "miss_rate_ped_near_glare の相対改善"
    verification: "同一評価セット＋新規実車週次"
  - type: contract
    action: "カメラ欠落とLiDAR-only占有を residuals に残し、融合平均で消さない"
    expected_effect: "完全ロストの低減"
    verification: "residualsとmissの相関監査"

hard_reject:
  triggers_gate: true
  gate_id: "HR-pedestrian-disappear"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-004, F-006]
  e2e_contract_fields: ["dynamics.tracks", "bev.occ_uncertainty", "residuals.lidar_only_occupancy"]
```

---

## F-004 大型車遮断下の横断歩行者遅延検出

```yaml
id: F-004
title: 大型車遮断下の横断歩行者遅延検出
status: active
severity: P0
modality: [camera, lidar]
scene_tags: [urban, occlusion, pedestrian, crossing, bus_truck]

definition: |
  バス・トラック等の大型車による遮断の直後または最中に、横断歩行者の検出／トラック開始が遅れ、
  出現から安定トラックまでの時間が閾値を超える。遮断自体は正常現象であり、
  「遅延」を失敗として定義する。

repro:
  log_query: "大型車トラック手前; 横断歩道／横断意図タグ; 歩行者出現後の初検出遅延"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 遮断解除フレームをアノテート（またはヒューリスティックで候補抽出）する。
    2. 歩行者GT出現から exists_prob>=閾値 までの遅延を測る。
    3. カメラのみ／LiDARのみ／融合の遅延を比較記録する。

metrics:
  offline:
    - name: ped_appear_latency_s
      formula: "遮断解除後、歩行者出現から安定検出までの秒"
      threshold_bad: ">= 【仮閾値・要実測】0.4 s"
  onboard_or_sim:
    - name: crossing_ttc_proxy
      formula: "横断歩行者に対する余裕時間プロキシの悪化率"
      threshold_bad: "【仮閾値・要実測】（実測後に設定）"
  safety_proxy:
    - name: near_miss_margin
      note: "遅延検出はゲート候補。モデルスコアで打ち消さない"

hypotheses:
  - id: H1
    text: "遮断中のトラック初期化が保守的すぎる"
    status: open
  - id: H2
    text: "大型車の点群／マスク漏れで歩行者点が車両に吸収される"
    status: open

levers:
  - type: model
    action: "occlusion属性と短い履歴からの早期仮説トラック（低exists_probで可）"
    expected_effect: "遅延の短縮"
    verification: "遮断シナリオ評価セット"
  - type: data
    action: "大型車遮断横断の難例を意図的にサンプリング"
    expected_effect: "系統的遅延の低減"
    verification: "週次発火頻度"

hard_reject:
  triggers_gate: true
  gate_id: "HR-pedestrian-late-appear"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-003, F-009]
  e2e_contract_fields: ["dynamics.tracks.attr.occluded", "bev.occ_uncertainty"]
```

---

## F-005 雨天の地面反射ゴースト

```yaml
id: F-005
title: 雨天の地面反射ゴースト
status: active
severity: P1
modality: [lidar]
scene_tags: [urban, rain, wet_road, lidar_ghost]

definition: |
  雨天・路面湿潤時に、LiDARの地面反射や水たまり反射により、実在しない占有／物体仮説
  （ゴースト）がBEVまたはトラックに現れる。誤検出として観測し、原因断定は仮説欄へ。

repro:
  log_query: "weather_tags=rain; 低高さクラスタ; カメラに対応物体なし; 路面近傍"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 雨天ログで地面近傍の高intensity／多重反射疑いクラスタを抽出する。
    2. カメラ・地図との対応が無い占有をゴースト候補とする。
    3. ワイパー・水跳ねフレームは別タグで混同を避ける。

metrics:
  offline:
    - name: lidar_ghost_fp_rate_rain
      formula: "雨天フレームにおける地面近傍偽占有率"
      threshold_bad: ">= 【仮閾値・要実測】2%"
  onboard_or_sim:
    - name: phantom_brake_proxy
      formula: "ゴースト起因の不要減速／停止プロキシ回数"
      threshold_bad: ">= 【仮閾値・要実測】（実測後）"
  safety_proxy:
    - name: residual_camera_disagree
      note: "カメラ不一致を残差として残し、過信ブレーキの監視に使う"

hypotheses:
  - id: H1
    text: "水面スペキュラによる多重反射"
    status: open
  - id: H2
    text: "地面セグメンテーション閾値が雨天で過検知"
    status: open

levers:
  - type: data
    action: "雨天ゴースト難例のネガティブセット追加"
    expected_effect: "FP率低減"
    verification: "雨天専用評価分割"
  - type: pipeline
    action: "地面高さ・カメラ不一致ゲートでゴースト抑制（微小介入）"
    expected_effect: "phantom_brake_proxy 低減"
    verification: "同一ルート雨天キャンペーン"

hard_reject:
  triggers_gate: false
  gate_id: ""
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-007, F-006]
  e2e_contract_fields: ["bev.ground_prob", "residuals.cam_lidar_depth_disagree"]
```

---

## F-006 夜間ヘッドライトフレア誤検出

```yaml
id: F-006
title: 夜間ヘッドライトフレア誤検出
status: active
severity: P1
modality: [camera]
scene_tags: [urban, night, headlight, flare, false_positive]

definition: |
  夜間、対向・隣接車両のヘッドライトフレアやレンズフレアにより、歩行者／二輪／障害物が
  誤って検出される、またはセマンティックピークが偽の高応答を示す。欠落ではなく誤検出側の失敗。

repro:
  log_query: "night; flare/bloomメタ; 高confidence検出だがLiDAR占有なし; 対向車接近"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 夜間対向シーンでカメラのみ高スコア検出を列挙する。
    2. LiDAR占有・距離と照合し、対応点が無いものをFP候補とする。
    3. 露光メタ（ゲイン、シャッター）を併記して再現セット化する。

metrics:
  offline:
    - name: night_flare_fp_rate
      formula: "夜間フレア条件でのクラス別偽陽性率"
      threshold_bad: ">= 【仮閾値・要実測】3%"
  onboard_or_sim:
    - name: false_yield_or_brake_proxy
      formula: "フレアFPに伴う不要譲歩／減速のプロキシ"
      threshold_bad: "【仮閾値・要実測】"
  safety_proxy:
    - name: cam_only_peak_without_lidar
      note: "residuals.camera_only_semantic_peak を監視。過信抑制"

hypotheses:
  - id: H1
    text: "飽和画素と学習バイアスによる歩行者様テクスチャの誤発火"
    status: open
  - id: H2
    text: "露光制御の遅れによるブルーム"
    status: open

levers:
  - type: data
    action: "夜間フレアFPのハードネガティブ採掘"
    expected_effect: "FP率低減"
    verification: "夜間holdout"
  - type: contract
    action: "camera-onlyピークを契約残差に残し、exists_probをLiDAR不一致で減衰"
    expected_effect: "過信検出の抑制"
    verification: "微小介入AB"

hard_reject:
  triggers_gate: false
  gate_id: ""
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-003, F-010]
  e2e_contract_fields: ["residuals.camera_only_semantic_peak", "dynamics.tracks.exists_prob"]
```

---

## F-007 静止障害（工事コーン）の消滅

```yaml
id: F-007
title: 静止障害（工事コーン）の消滅
status: active
severity: P0
modality: [fusion]
scene_tags: [urban, construction, static_obstacle, cone, fusion_drop]

definition: |
  工事コーン等の静止小物体が、ある区間では検出／占有されていたにもかかわらず、
  融合またはトラッキング過程で消滅し、BEV占有・トラックから消える。
  動的ロストではなく静止障害の消失として定義する。

repro:
  log_query: "construction/coneタグ; 静止; 連続フレームで存在→欠落; 自車接近"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. コーン既知区間でフレームごとの存在フラグを時系列化する。
    2. 消滅フレーム前後のカメラ応答・LiDAR点数・融合重みを記録する。
    3. 地図更新遅れと区別するため、一時設置かどうかをシーンタグで分離する。

metrics:
  offline:
    - name: static_cone_disappear_rate
      formula: "既知静止コーンが連続Nフレーム以上消滅する率"
      threshold_bad: ">= 【仮閾値・要実測】1%"
  onboard_or_sim:
    - name: clearance_violation_proxy
      formula: "消滅後に計画経路がコーン占有を横切るプロキシ"
      threshold_bad: "【仮閾値・要実測】>0 を不良候補"
  safety_proxy:
    - name: near_miss_margin
      note: "静止障害消滅はP0ゲート。スコアで上書き禁止"

hypotheses:
  - id: H1
    text: "動的モデルが静止小物体をノイズとして抑制"
    status: open
  - id: H2
    text: "低点数LiDAR＋融合閾値で占有が落ちる"
    status: open

levers:
  - type: model
    action: "静止小物体クラスの別ヘッドまたは占有持続項（微小）"
    expected_effect: "消滅率低減"
    verification: "工事シーン評価セット"
  - type: data
    action: "コーン／バー／看板の静的難例を意図サンプリング"
    expected_effect: "系統的欠落の是正"
    verification: "F-007週次発火"

hard_reject:
  triggers_gate: true
  gate_id: "HR-static-obstacle-disappear"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-001, F-005, F-008]
  e2e_contract_fields: ["bev.occ_prob", "bev.occ_uncertainty", "gates.hard_reject"]
```

---

## F-008 希少クラス（車椅子・幼児車）の系統的欠落

```yaml
id: F-008
title: 希少クラス（車椅子・幼児車）の系統的欠落
status: active
severity: P0
modality: [data]
scene_tags: [urban, rare_class, wheelchair, stroller, long_tail]

definition: |
  車椅子・幼児車（ベビーカー）等の希少クラスが、評価・実車で系統的に未検出または
  汎用歩行者／不明に潰され、クラス別リコールが他クラスより大きく劣る。
  単発ミスではなくデータ分布・ラベル方針に起因しうる系統欠落として定義する。

repro:
  log_query: "class in {wheelchair, stroller}; 都市歩道・横断; ラベル版を固定"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 希少クラスのholdoutを別バケットで固定する（漏洩禁止）。
    2. クラス別リコール／欠落モード（未検出 vs 誤クラス）を集計する。
    3. 訓練セット内の出現頻度と欠落の相関を記録する（因果断定はしない）。

metrics:
  offline:
    - name: rare_class_recall
      formula: "車椅子・幼児車の検出リコール（クラス別）"
      threshold_bad: "<= 【仮閾値・要実測】0.7 または多数クラスとのギャップ大"
  onboard_or_sim:
    - name: rare_class_miss_event_rate
      formula: "実車キャンペーンでの希少クラス見逃しイベント率"
      threshold_bad: "【仮閾値・要実測】"
  safety_proxy:
    - name: vulnerable_user_margin
      note: "弱者ユーザはP0。平均mAPに溶かさない"

hypotheses:
  - id: H1
    text: "訓練データ出現頻度不足"
    status: open
  - id: H2
    text: "ラベル定義が歩行者に吸収されている"
    status: open

levers:
  - type: data
    action: "希少クラスの意図的収集・提携データ・合成の方針を文書化しholdoutを分離"
    expected_effect: "リコール改善と系統欠落の可視化"
    verification: "希少クラス専用ダッシュボード"
  - type: contract
    action: "unknown/脆弱ユーザ属性を契約に残し、無理に多数クラスへ落とさない"
    expected_effect: "黙殺の防止"
    verification: "ラベルマップ版監査"

hard_reject:
  triggers_gate: true
  gate_id: "HR-rare-vulnerable-miss"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-003, F-007]
  e2e_contract_fields: ["dynamics.tracks.class_id", "semantics.label_map_version"]
```

---

## F-009 急減速先行車のトラッキングID破綻

```yaml
id: F-009
title: 急減速先行車のトラッキングID破綻
status: active
severity: P1
modality: [track]
scene_tags: [urban, hard_brake, lead_vehicle, id_switch]

definition: |
  先行車が急減速した際に、同一物体のトラックIDが切れ・付け替わり（ID switch）し、
  速度推定や予測の連続性が失われる。検出は残っていてもトラック同一性の失敗として定義する。

repro:
  log_query: "lead_vehicle; 減速度|a|>=閾値; ID switchまたはトラック再初期化"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 急減速区間をCAN／相対速度から抽出する。
    2. 同一GT物体に対するID変化回数を数える。
    3. 遮断・車線変更と混同しないようシーンタグで分離する。

metrics:
  offline:
    - name: id_switch_rate_hard_brake
      formula: "急減速イベントあたりのIDスイッチ回数"
      threshold_bad: ">= 【仮閾値・要実測】1回/イベント"
  onboard_or_sim:
    - name: velocity_discontinuity_mps
      formula: "ID切替前後の速度推定ジャンプ"
      threshold_bad: ">= 【仮閾値・要実測】3 m/s"
  safety_proxy:
    - name: rear_end_ttc_proxy
      note: "追突余裕の悪化を別帳簿で監視"

hypotheses:
  - id: H1
    text: "モーションモデルが急減速を外れ値として切り捨てる"
    status: open
  - id: H2
    text: "部分遮断で検出ボックスが飛び、関連付けが切れる"
    status: open

levers:
  - type: model
    action: "急減速を許容するモーション／関連付けコストの微小調整"
    expected_effect: "ID switch低減"
    verification: "急減速シナリオセット"
  - type: pipeline
    action: "短時間の海岸（coasting）仮説を残し、即再初期化しない"
    expected_effect: "連続性維持"
    verification: "オンボード週次"

hard_reject:
  triggers_gate: false
  gate_id: ""
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-002, F-004]
  e2e_contract_fields: ["dynamics.tracks.track_id", "dynamics.tracks.velocity_mps"]
```

---

## F-010 対向二輪の距離過大推定

```yaml
id: F-010
title: 対向二輪の距離過大推定
status: active
severity: P0
modality: [camera, fusion]
scene_tags: [urban, oncoming, motorcycle, cyclist, depth_error]

definition: |
  対向の二輪（バイク／自転車）について、推定距離が真値より系統的に大きくなり、
  接近リスクを過小評価する。左右誤差より奥行き過大を本失敗の本態とする。

repro:
  log_query: "oncoming motorcycle|cyclist; カメラ距離 vs LiDAR/測距参照; 過大側誤差"
  min_examples: 3
  synthetic_ok: true
  steps: |
    1. 対向二輪区間で参照距離（LiDARクラスタまたは【要差し替え】測距）を取る。
    2. カメラ単体／融合の距離推定との符号付き誤差を集計する。
    3. 夜間フレア・細いシルエット条件をサブタグで分ける。

metrics:
  offline:
    - name: oncoming_two_wheeler_depth_bias_m
      formula: "推定距離 − 参照距離 の中央値（正=過大）"
      threshold_bad: ">= 【仮閾値・要実測】2.0 m"
  onboard_or_sim:
    - name: closing_speed_underestimate_proxy
      formula: "接近速度過小評価に伴う余裕時間プロキシ悪化"
      threshold_bad: "【仮閾値・要実測】"
  safety_proxy:
    - name: near_miss_margin
      note: "対向二輪の奥行き過大はP0。平均精度に溶かさない"

hypotheses:
  - id: H1
    text: "細いシルエットに対する単眼深度の遠方バイアス"
    status: open
  - id: H2
    text: "融合がカメラ深度を優先しLiDAR少数点を無視"
    status: open

levers:
  - type: data
    action: "対向二輪の距離付き難例セット強化"
    expected_effect: "過大バイアス低減"
    verification: "対向二輪holdout"
  - type: contract
    action: "cam_lidar_depth_disagree を残差必須化し、過大側を不確実性へ反映"
    expected_effect: "過信距離の抑制"
    verification: "残差校正フック"

hard_reject:
  triggers_gate: true
  gate_id: "HR-oncoming-twowheeler-depth"
  may_not_be_overridden_by_model_score: true

links:
  example_logs: ["【要差し替え：Kが実数・固有名詞を記入】"]
  related_failures: [F-002, F-006]
  e2e_contract_fields: ["dynamics.tracks.xyz", "residuals.cam_lidar_depth_disagree", "bev.occ_uncertainty"]
```

---

## レビューチェック（本シード）

- [x] 定義に仮説断定が入っていない（仮説は hypotheses へ分離）
- [x] 再現手順またはログクエリがある
- [x] offline と onboard/sim の指標が両方ある
- [x] P0は Hard Reject／ゲート参照がある（F-001,002,003,004,007,008,010）
- [x] 改善レバーに微小介入が1つ以上
- [x] 秘密・個人が特定できる生データをリンクしていない（プレースホルダのみ）
- [ ] 閾値の実測差し替え 【仮閾値・要実測】
- [ ] example_logs の実パス 【要差し替え：Kが実数・固有名詞を記入】

## 【要差し替え】一覧

| 箇所 | 内容 |
|---|---|
| 全F-* `threshold_bad` | 【仮閾値・要実測】 |
| 全F-* `example_logs` | 【要差し替え：Kが実数・固有名詞を記入】 |
| F-010 参照測距手段 | 【要差し替え：Kが実数・固有名詞を記入】 |
| 運用ドメイン固有タグ | 必要なら newmo 実スタック名をKが記入 |

