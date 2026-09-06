# 2026-09-06 Address claim_type closed enum

## 追加

- `CLAIM_TYPE_ALLOWED` 閉集合（DESIGN_DESCRIPTION | EXPERIMENT_RESULT | CAPABILITY_CLAIM）。
- `decision_log.verify` + CLI（`--protocol-manifest` に `--claim-type` 必須；未知 INVALID_INPUT）。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
