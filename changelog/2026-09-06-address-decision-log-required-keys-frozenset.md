<!--
title: "Address decision_log REQUIRED_KEYS frozenset single-source"
date: "2026-09-06"
-->

# Address reference-runtime: decision_log REQUIRED_KEYS frozenset single-source

- `decision_log.REQUIRED_KEYS` を `frozenset` に変更し、`response_contract.DECISION_LOG_REQUIRED_KEYS` と単一正本化（同一 object `is` 一致 + 値一致を unittest で固定）。
- `fixtures/runtime_manifest.json` を再凍結。
- unittest: 282 tests 全緑。