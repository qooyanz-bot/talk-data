# 2026-09-06 Address CLI --validate-protocol-manifest

## 追加

- `address_cli.validate_protocol_manifest_only(path)` と CLI `--validate-protocol-manifest MANIFEST.json`。
  - 成功: exit 0 / `{status: MANIFEST_VALID, errors: []}`
  - 失敗: exit 1 / `{status: MANIFEST_INVALID, errors: [...]}`（load 失敗は INVALID_INPUT / exit 2）
- `_resolve_flag_conflicts` に standalone モードとして登録。resolve 入力および `--limitations` / `--check-contract-only` / `--verify-decision-log` と相互排他。

## テスト

- R6-G frozen fixture → MANIFEST_VALID
- 未知 evidence_state → MANIFEST_INVALID
- flag combo → INVALID_INPUT

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
