# 2026-09-06 Address check-contract-only decision_log response

## 追加

- `fixtures/golden_contract_decision_log_blocked_response.json`：R6-G SPEC_ONLY + EXPERIMENT_RESULT の evaluate 公開応答（resolution + generated_audit + protocol_claim + decision_log；value=null）
- unittest：`--check-contract-only` 通過；改ざん decision_log_id 失敗；非null decision_log.value 失敗
- CLI `--verify-decision-log DECISION_LOG.json`：decision_log.verify のみ（相互排他）

## 非対象

- regenerator / match-evaluate への配線（golden 増殖抑制）
- Value発見、R6-G実行、秘密・暗号・宇宙DB
