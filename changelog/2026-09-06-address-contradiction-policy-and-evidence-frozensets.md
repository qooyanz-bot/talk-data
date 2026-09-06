<!--
title: "Address contradiction_policy closed enum & evidence_contract frozensets single-source"
date: "2026-09-06"
-->

# Address reference-runtime: contradiction_policy closed enum & evidence_contract frozensets single-source

- `address_runtime.py`: `CONTRADICTION_POLICY_ALLOWED = frozenset({"STOP_AND_REPORT_CONFLICT"})` を単一正本として export し、`validate()` での閉集合検証を適用。
- `address_runtime.py`: `REQUIRED_FIELDS`, `DIMENSIONS`, `REAL_CAPABILITIES`, `FORBIDDEN_CAPABILITY_TOKENS` を `frozenset` 定数化。
- `evidence_contract.py`: `REQUIRED_FIELDS` および `INDEPENDENCE_AXES` を `frozenset` 定数として export（`REQUIRED` はエイリアス維持）。
- unittest: 281 tests 全緑。