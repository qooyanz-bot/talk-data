# 2026-09-06 Address synthetic-only validate enforcement

## 追加

- `address_runtime.validate` が LIMITATIONS `world_scope=SYNTHETIC_ONLY` を実行時に強制。
- `world_id` が `world:real:` で始まる場合は明確な errors で INVALID（`SYNTHETIC_ONLY` を含むメッセージ）。
- `world:synthetic-` は非空 suffix 必須（空 suffix `world:synthetic-` は拒否）。
- `target_value.residual` が list のとき、要素は非空文字列でなければならない。
- `REAL_CAPABILITIES` 定数はアーキテクチャ／スキーマ文書用に残置。real-world capability subset 検査は到達不能のため削除（real world は validate で先に失敗）。

## 非変更

- `fixtures/valid_synthetic_address.json` は VALID のまま（address_id 非書換）。
- 新規 golden なし。Value発見、R6-G実行、秘密・暗号・宇宙DBは対象外。
