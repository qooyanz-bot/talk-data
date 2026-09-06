# 2026-09-06 Address claim_reason closed enum

## 追加

- `CLAIM_REASON_ALLOWED` 閉集合（assess_claim emitters のみ）。
- `decision_log.verify` + response_contract（verify 経由）が claim_reason 閉集合を強制。
- decision_log 非 dict assessment fallback は gate reason（MANIFEST_INVALID）のみ。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
