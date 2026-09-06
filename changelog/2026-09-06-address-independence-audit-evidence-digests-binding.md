# 2026-09-06 Address independence_audit evidence_digests binding

## 追加

- `audit_log.content_digest` / `evidence_digest_entries` を公開ヘルパとして固定（Audit Log と independence_audit で同一 digest）。
- `assess_audited_independence(..., evidence=...)` の content-addressed 束一致検査。
- Resolution Gate が AUDITED 経路で evidence を監査検査へ渡す。

## 挙動

- チェックリスト有効かつ digests が供給束と完全一致 → AUDITED / READY（value=null）。
- 別束への PASS 監査・placeholder digests → UNMET / SEMANTIC_INDEPENDENCE_UNMET。
- `assess()` 単体は決して AUDITED を返さない。

## 非対象

- Value発見、R6-G実行、秘密・暗号・宇宙DB。
- AUDITED READY golden の追加（任意・本増分では未実施）。
