# (C) E2E 入力スキーマ草案（Perception → E2E / Planning）

- 版: v0.1（K承認 2026-09-06）
- 正本: talk-data canonicalization / README.md
- 原則: Representation First。モデルは契約の実現手段。契約変更は版上げ。
- 非目標: 特定アーキテクチャ（特定BEVネット等）の固定

## 0. 設計意図

E2Eが直接センサから学ぶ場合でも、Perception側が提供しうるものは次の三層に分ける。

1. **Raw-aligned** — 同期・校正済みセンサテンソル（学習の主入力になりうる）
2. **Contract features** — 下流が読んでよい中間表現（占有・動的・不確実性）
3. **Gates** — 学習・推論に混ぜない Hard Reject 信号

本草案は主に 2 と 3、および 1 のメタデータを定義する。

## 1. 共通メタ（すべてのフレーム）

```json
{
  "schema_version": "0.1.0",
  "frame_id": "string",
  "timestamp_ns": 0,
  "ego_pose": {
    "frame": "map|odometry",
    "xyz": [0.0, 0.0, 0.0],
    "quat_wxyz": [1.0, 0.0, 0.0, 0.0]
  },
  "sync": {
    "camera_lidar_skew_ms": 0.0,
    "sync_ok": true
  },
  "calib": {
    "extrinsic_version": "string",
    "calib_ok": true,
    "drift_score": 0.0
  },
  "weather_tags": ["clear|rain|fog|snow|unknown"],
  "operational_domain": "urban_taxi_jp_v0"
}
```

`sync_ok=false` または `calib_ok=false` のフレームは、学習バケットを分離する（デフォルト: train禁止 / eval専用）。

## 2. Raw-aligned（参照）

```json
{
  "cameras": [
    {
      "name": "front_wide",
      "image_ref": "uri-or-tensor-handle",
      "intrinsics": {"fx":0,"fy":0,"cx":0,"cy":0,"distortion":[]},
      "extrinsics_ego": {"xyz":[0,0,0],"quat_wxyz":[1,0,0,0]},
      "exposure_meta": {}
    }
  ],
  "lidar": {
    "name": "top",
    "points_ref": "uri-or-tensor-handle",
    "fields": ["x","y","z","intensity","timestamp_offset"],
    "extrinsics_ego": {"xyz":[0,0,0],"quat_wxyz":[1,0,0,0]}
  }
}
```

## 3. Contract features（E2Eが読んでよい本体）

単位系: メートル、ラジアン、秒。グリッドは ego 原点。

### 3.1 Occupancy / BEV

```json
{
  "bev": {
    "x_range_m": [-40, 80],
    "y_range_m": [-40, 40],
    "resolution_m": 0.2,
    "occ_prob": "HxW float32 [0,1]",
    "occ_uncertainty": "HxW float32 [0,1]",
    "height_mean_m": "HxW float32",
    "height_var": "HxW float32",
    "ground_prob": "HxW float32"
  }
}
```

### 3.2 Dynamic objects（トラック）

```json
{
  "dynamics": {
    "tracks": [
      {
        "track_id": "string",
        "class_id": "veh|ped|cyclist|motorcycle|unknown",
        "class_conf": 0.0,
        "xyz": [0.0, 0.0, 0.0],
        "size_lwh_m": [0.0, 0.0, 0.0],
        "yaw_rad": 0.0,
        "velocity_mps": [0.0, 0.0, 0.0],
        "exists_prob": 0.0,
        "attr": {
          "occluded": false,
          "truncated": false
        }
      }
    ],
    "max_tracks": 256
  }
}
```

### 3.3 Contradiction / fusion residuals（消さない矛盾）

```json
{
  "residuals": {
    "cam_lidar_depth_disagree": "HxW float32",
    "lidar_only_occupancy": "HxW float32",
    "camera_only_semantic_peak": "HxW float32",
    "notes": "融合で平均化して消さない。E2Eと安全モニタの入力"
  }
}
```

### 3.4 Optional semantics（契約に含めるなら版付き）

```json
{
  "semantics": {
    "enabled": false,
    "label_map_version": "sem-jp-taxi-v0",
    "bev_logits_ref": null,
    "forbidden_as_hard_fact": ["medical", "legal", "intent_of_person"]
  }
}
```

## 4. Gates（モデルスコアで上書き禁止）

```json
{
  "gates": {
    "hard_reject": [
      {
        "gate_id": "HR-pedestrian-disappear",
        "active": false,
        "evidence_refs": [],
        "action": "inhibit_autonomy|force_safe_stop|degrade_to_teleop"
      }
    ],
    "quality_flags": {
      "geometry_healthy": true,
      "time_sync_healthy": true,
      "train_eligible": true
    }
  }
}
```

## 5. Planning IF（最小）

PlanningがE2Eと並走／監視する場合の最小面:

| フィールド | 用途 |
|---|---|
| `bev.occ_prob` + `occ_uncertainty` | 静的・準静的の余裕 |
| `dynamics.tracks` | 予測の種 |
| `residuals.*` | 過信抑制 |
| `gates.*` | 上書き不可の抑制 |

IF変更は `schema_version` の minor/major で管理。口頭合意禁止。

## 6. 欠損・パディング規則

- 欠センサ: テンソルは NaN または mask チャネル。ゼロ埋め黙殺禁止
- トラック数不足: パディング＋ `valid` マスク
- 低信頼: `exists_prob` / `occ_uncertainty` で表現し、クラスを捏造しない

## 7. 評価フック（スキーマに紐づく）

- 契約適合率: 必須フィールド欠損率
- 幾何ゲート落ち率: `calib_ok`/`sync_ok` false 比率
- 残余の校正: `cam_lidar_depth_disagree` と実測深度誤差の相関
- 下流感度: 契約フィールドをマスクしたときのE2E劣化（微小介入で測定）

## 8. 90日での凍結方針

- v0.1: メタ＋BEV占有＋不確実性＋tracks＋gates の型だけ凍結
- 中身の解像度・レンジは計測後に v0.2 で版上げ
- 特定ネットワーク出力次元への依存は契約に書かない

## 9. Critic

- 厚すぎる契約はE2Eの端到端学習を阻害しうる → Raw-alignedを主、Contractは補助／監視に落とすオプションを残す
- 不確実性が未校正だと害 → 必ず評価フック§7の校正をセットで導入
- タクシーODD外（高速道路など）は `operational_domain` で分離し、黙って汎用化しない
