# 2026-09-06 Address AUDITED_INDEPENDENCE READY golden

## 追加

- `fixtures/golden_contract_audited_independence_response.json`
  - Address `semantic_independence=AUDITED`
  - CONTRACTED evidence + valid typed `independence_audit`（`{evidence_id, digest}` pairs match bundle）
  - `evaluate()` → `READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` / `value=null` / residual present / audit aligned
- Dedicated `--check-contract-only` unittest（SEMANTIC_INDEPENDENCE_UNMET golden の成功対称）
- `regenerate_contract_goldens.py` + match-evaluate 配線

## 非対象

- Value発見、R6-G実行、秘密・暗号・宇宙DB
- 静かな AUDITED 昇格ショートカット
