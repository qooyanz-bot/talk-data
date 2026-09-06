<!--
title: "Address CLI standalone mode mutual-exclusion matrix test"
date: "2026-09-06"
-->

# Address reference-runtime: CLI standalone mode mutual-exclusion matrix test

- `test_address_cli.py` に `test_standalone_modes_mutually_exclusive_matrix` を追加。
- 全 7 スタンドアロンモード（`--limitations` / `--runtime-manifest` / `--conformance` / `--check-contract-only` / `--verify-decision-log` / `--verify-audit-log` / `--validate-protocol-manifest`）が、他の 6 モードおよび全解決引数（address/evidence位置引数・`--now`・`--audit`・`--independence-audit`・`--protocol-manifest`・`--claim-type`）と同時指定された場合に `INVALID_INPUT` / exit 2 になることを全組み合わせ横断で固定。
- unittest: 285 tests 全緑。