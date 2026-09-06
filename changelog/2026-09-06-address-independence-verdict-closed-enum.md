# 2026-09-06 Address independence verdict closed enum single-source

## 追加

- `INDEPENDENCE_ASSESS_ALLOWED` 閉集合（COMMON_CAUSE_SUSPECT | CONTRACTED | UNVERIFIED）。`assess()` emitters の単一正本。
- `INDEPENDENCE_AUDIT_ALLOWED` 閉集合（AUDITED | UNMET）。`assess_audited_independence()` emitters の単一正本。
- `_result` / `_audit_result` が軽量 assert。assess は INDEPENDENT を決して返さない。

## 非変更

- response_contract / resolution_gate への independence 公開検証は未配線（公開応答フィールドではない）。
- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
