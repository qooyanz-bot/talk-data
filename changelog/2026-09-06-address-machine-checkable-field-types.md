# 2026-09-06 Address machine-checkable field types / canonical serialization

## 追加

- `address_runtime.validate` を硬化し、Architecture Open work「各フィールドの機械可読型と正規直列化」の増分を実装。
- `entities`: 非空 `id` / `type`；任意 `binding` は存在時に非空文字列。
- `relations`: 非空 `predicate` / `subject` / `object`。
- `unknown`: 非空 `slot`；`status` は閉集合 `NOT_DERIVABLE` | `UNRESOLVED` | `RESIDUAL` | `OPEN`；`abstain_if_unresolved=true` は従来どおり必須。
- `lineage.protocol_sha` / `schema_sha` / `runtime_sha`: null 又は非空文字列（`result_sha` は引き続き null 必須；`input_hashes` は sha256 制約のまま）。
- `evidence_requirements.minimum_sources`: 存在時は bool 以外の int かつ >= 1。
- `canonical_dumps` ヘルパを追加し、`canonical_id` が `sort_keys=True` と `separators=(',', ':')` のみを使うことを明示。キー順・空白差が `address_id` を変えないことを unittest で固定。

## 非変更

- `fixtures/valid_synthetic_address.json` の `address_id` / 内容は変更しない（VALID のまま）。
- 契約 golden の再生成は不要（canonical_id 不変のため）。
- Value発見、R6-G実行、秘密・暗号・宇宙DBは対象外。
