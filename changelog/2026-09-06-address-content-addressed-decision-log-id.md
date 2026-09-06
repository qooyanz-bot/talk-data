# 2026-09-06 Address content-addressed decision_log_id

## 追加

- `decision_log.build_decision_log` / `create`：`decision_log_id` = `decision_log:` + sha256（`audit_log.content_digest` と同アルゴリズム）を id 除外 canonical payload から付与
- `decision_log.verify()`：必須キー・schema_version・自己アドレス整合を検査（改ざん検出）
- Response Contract：decision_log 存在時に `decision_log_id` 必須＋verify 結果を収集
- `fixtures/r6g_frozen_decision_log_blocked.json` をコードから再生成（decision_log_id 含む）
- unittest：同一入力で id 安定；改ざん検出；contract が有効 decision_log_id を要求

## 非対象

- 新規 CLI evaluate golden
- Value発見、R6-G実行、秘密・暗号・宇宙DB
