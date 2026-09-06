<!--
title: "Address audit_log closed enum verification & CLI --verify-audit-log"
date: "2026-09-06"
-->

# Address reference-runtime: audit_log closed enum verification & CLI --verify-audit-log

- `audit_log.py`: `SCHEMA_VERSION = "ADDRESS-AUDIT-1.0"` および `REQUIRED_KEYS` を export。`verify()` で `decision` (`resolution_gate.DECISION_ALLOWED`) および `reason` (`resolution_gate.REASON_ALLOWED`) の閉集合検査を追加し、改ざん・不正語彙の監査ログを厳密に拒否。
- `response_contract.py`: `DECISION_LOG_REQUIRED_KEYS` を `decision_log.REQUIRED_KEYS` から単一正本として参照。
- `address_cli.py`: `--verify-audit-log AUDIT.json` モードを追加。スタンドアロンの Audit Log を構造・閉集合・content-address で検証（`AUDIT_LOG_OK` exit 0 / `AUDIT_LOG_INVALID` exit 1 / 相互排他 `INVALID_INPUT` exit 2）。