# 2026-09-06 Address decision_log claim_reason / unmet align

## 追加

- Response Contract：`decision_log` と `protocol_claim` 共存時
  - `claim_reason` == `protocol_claim.reason`（reason が protocol_claim にあるとき）
  - `unmet` は null 又は文字列の list
  - `protocol_claim.unmet` があるときは sorted 等価で一致
- `decision_log.build_decision_log`：`unmet` を常に list（空可）で emit
- unittest：reason mismatch / unmet non-list / unmet mismatch；R6-G frozen BLOCKED happy path

## 非対象

- 新規 CLI evaluate golden
- Value発見、R6-G実行、秘密・暗号・宇宙DB
