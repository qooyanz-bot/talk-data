Regenerator scripts for frozen documentation and conformance fixtures.

- `regenerate_limitations.py`: rebuilds `fixtures/limitations.json`
- `regenerate_conformance_report.py`: rebuilds `fixtures/conformance_report.json`
- `regenerate_runtime_manifest.py`: rebuilds `fixtures/runtime_manifest.json`
- `regenerate_contract_goldens.py`: rebuilds `fixtures/golden_contract_*.json`
- `regenerate_all_frozen_docs.py`: runs all document regenerators; `--check` for CI gate.
