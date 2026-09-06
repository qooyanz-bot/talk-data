# 2026-09-06 Address typed independence_audit evidence_digests

## 追加 / 硬化

- AUDITED チェックリストの `evidence_digests` を `{evidence_id, digest}` オブジェクトのみに固定。
- 裸の digest 文字列は shape 段階で `UNMET`（evidence 有無を問わない）。
- evidence 供給時は `audit_log.evidence_digest_entries` の evidence_id+digest 対と完全一致。

## 挙動

- 正しい typed digests + チェックリスト通過 → AUDITED / READY（value=null）。
- 裸文字列・余分キー・id 不一致・digest 不一致 → UNMET / SEMANTIC_INDEPENDENCE_UNMET。
- `assess()` 単体は決して AUDITED を返さない。

## 非対象

- Value発見、R6-G実行、秘密・暗号・宇宙DB。
- 新規 AUDITED READY golden（本増分では未実施；既存 binding 増分と同じ方針）。
