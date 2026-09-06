# 2026-09-06 Address remaining machine-checkable string-list types

## 追加

- `address_runtime.validate` の残り機械可読型を閉じる増分（Open work「各フィールドの機械可読型」の続き）。
- `goal.id`: 非空文字列（`isinstance(str)` のみだった検査を強化）。
- `goal.success_criteria`: 非空文字列の list（空文字列・非文字列を拒否；空 list は許容）。
- `state_constraints`: 非空文字列の list（同上）。
- `capability_scope`: 各要素を非空文字列に強化。既存の forbid-token 拒否と real-world subset 制約は維持。

## 非変更

- `fixtures/valid_synthetic_address.json` の `address_id` / 内容は変更しない（VALID のまま）。
- 契約 golden の再生成は不要。
- Value発見、R6-G実行、秘密・暗号・宇宙DBは対象外。
- AUDITED への静かな昇格は行わない（path多様性だけでは INDEPENDENT/AUDITED を返さない）。
