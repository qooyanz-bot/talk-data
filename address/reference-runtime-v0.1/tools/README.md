# tools

Frozen-doc regenerators: `regenerate_limitations.py`, `regenerate_conformance_report.py`, or both via `regenerate_all_frozen_docs.py`. Pass `--check` for dry-run drift detection (exit 0 if fixtures already match; non-zero if a rewrite would change files; no writes). Contract goldens: `regenerate_contract_goldens.py`. Do not hand-edit fixtures.
