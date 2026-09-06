# 2026-09-06 Address protocol manifest closed-enum validation

## 追加

- `protocol_claim_gate.validate_manifest(manifest) -> list[str]`：閉集合 enum / handoff shape を機械検査（例外なし）。
  - evidence_state: SPEC_ONLY | DIAGNOSTIC_ONLY | RESULT_BACKED
  - implementation_state: NOT_IMPLEMENTED | IMPLEMENTED
  - experiment_state: NOT_RUN | COMPLETED
  - independent_replay_state: NOT_RUN | REPLICATED
  - protocol_id: 非空文字列
  - auditor_handoff（存在時）: dict、キーは {decision, primary_run_authorized} のみ、decision=PENDING|PASS、primary_run_authorized=bool|null
- `assess_claim` は validate を先に実行；errors 時は BLOCKED / MANIFEST_INVALID / unmet=errors（DESIGN_DESCRIPTION 含む）。

## 注記

- auditor_handoff.decision に FAIL は含めない（protocol manifest fixtures/tests に未出現；independence_audit の FAIL とは別面）。

## 非変更

- 新規 evaluate golden なし。R6-G FROZEN / 既存通過 manifest は green。Value発見、R6-G実行、秘密・暗号・宇宙DB、Cortext9/CIVA は対象外。
