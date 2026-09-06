# 2026-09-06 Address claim_status closed enum

## 追加

- `CLAIM_STATUS_ALLOWED` 閉集合（ALLOWED_AS_DESIGN | ALLOWED_AS_RESULT | BLOCKED）。
- `decision_log.verify` + response_contract（PROTOCOL_CLAIM_STATUSES エイリアス）が同一正本を共有。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
