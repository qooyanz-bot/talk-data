# 2026-09-06 Address decision_log closed-enum mirror

## 追加

- `protocol_claim_gate` の閉集合 frozenset（`STATE_ENUMS` / `EVIDENCE_STATE_ALLOWED` 等 / `AUDITOR_HANDOFF_DECISION_ALLOWED` / `AUDITOR_HANDOFF_KEYS`）を単一の正本として export（`format_allowed` も公開）。
- `decision_log.verify`：状態フィールドが非 null のとき閉集合所属を要求；`auditor_handoff.decision` が非 null なら `PENDING|PASS`；handoff キーは厳密に {decision, primary_run_authorized}。
- Response Contract：decision_log 存在時の enum 検査は `decision_log.verify` 経由（単一路）。`DECISION_LOG_HANDOFF_KEYS` は `AUDITOR_HANDOFF_KEYS` の alias。

## 非変更

- 新規 evaluate golden なし。R6-G frozen decision_log fixture は green。Value発見、R6-G実行、秘密・暗号・宇宙DB、Cortext9/CIVA は対象外。
