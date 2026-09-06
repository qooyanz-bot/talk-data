# 2026-09-06 Address decision_log Response Contract shape harden

## 追加

- Response Contract：`decision_log` があるとき機械可読 shape を強制
  - 必須キー：schema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff / value / evidence_state / experiment_state / implementation_state / independent_replay_state
  - schema_version は `decision_log.SCHEMA_VERSION` と一致
  - value は常に null
  - claim_status は既知集合、かつ protocol_claim.status があるとき非矛盾
  - auditor_handoff は厳密に {decision, primary_run_authorized}（余分な秘密様キー拒否）
- unittest：missing schema_version / wrong handoff keys / non-null value / status mismatch

## 非対象

- 新規 golden
- Value発見、R6-G実行、秘密・暗号・宇宙DB
