<!--
title: "Address cross-module vocabulary alias identity test"
date: "2026-09-06"
-->

# Address reference-runtime: cross-module vocabulary alias identity test

- `test_response_contract.py` に `test_all_alias_identities_single_source` と `test_protocol_claim_statuses_alias_single_source` を追加。
- `response_contract` の全公開語彙エイリアス（`DECISIONS`/`REASONS`/`REPLAY_STATUSES`/`PROTOCOL_CLAIM_STATUSES`）が、各 emmiter module（`resolution_gate`/`replay_verifier`/`protocol_claim_gate`）の同一 `frozenset` オブジェクトであること（`is` 一致＋値一致）を単一の横断テストで固定。
- unittest: 284 tests 全緑。