# 2026-09-06 Address evidence_contract status closed enum

## 追加

- `ASSESS_STATUS_ALLOWED` 閉集合（INSUFFICIENT | INVALID | CONFLICT | CONTRACTED）。`assess()` status emitters の単一正本。
- `AUDIT_STATUS_ALLOWED` 閉集合（AUDITED | UNMET）。`assess_audited_independence()` status emitters の単一正本（independence とは別フィールド）。
- `_result` / `_audit_result` が status を軽量 assert。assess status は AUDITED / UNMET を決して返さない。

## 非変更

- response_contract / resolution_gate への status 公開検証は未配線（公開応答フィールドではない）。
- independence 閉集合（前コミット）は維持。
- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
