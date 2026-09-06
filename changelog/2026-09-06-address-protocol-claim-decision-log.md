# 2026-09-06 Address Protocol Claim Decision Log / auditor-handoff

## 追加

- `decision_log.py`
  - manifest + claim_type + `assess_claim` 結果から機械可読 Decision Log を構築
  - claim_status / claim_reason / unmet / 状態フィールド / auditor_handoff（decision・primary_run_authorized のみ）
  - `value` は常に null；秘密フィールドはスナップショットしない
- `fixtures/r6g_frozen_decision_log_blocked.json`
  - R6-G SPEC_ONLY + EXPERIMENT_RESULT → BLOCKED を凍結
- CLI：既存 `--protocol-manifest` / `--claim-type` 経路で evaluate 応答に `decision_log` を付与
- Response Contract：decision_log の value=null・既知 claim_status・protocol_claim.status 非矛盾
- LIMITATIONS：`protocol_result_claims=GATED`

## 非対象

- Value発見、R6-G実行、秘密・暗号・宇宙DB
- Cortext9 / CIVA の発明
