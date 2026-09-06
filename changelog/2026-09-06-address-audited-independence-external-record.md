# 2026-09-06 Address AUDITED path requires external independence_audit

## 追加

- Evidence Contract の凍結チェックリストと `assess_audited_independence(audit_record)`。
  必須フィールド: `auditor_id`, `decision=PASS`, `method`, `evidence_digests`, `audited_at`。
- Resolution Gate の任意引数 `independence_audit`、CLI `--independence-audit`、`evaluate(..., independence_audit=...)`。
- LIMITATIONS `audited_independence=EXTERNAL_RECORD_REQUIRED`。

## 挙動

- Address `semantic_independence=AUDITED` + CONTRACTED証拠のみ → 従来どおり ABSTAIN / SEMANTIC_INDEPENDENCE_UNMET。
- 有効な外部監査記録付き → READY_FOR_VERIFICATION / AUDITED_INDEPENDENCE / value=null（検証ゲート）。
- 不完全・偽造監査 → ABSTAIN。
- `assess()` 単体は決して AUDITED を返さない。path多様性だけでは AUDITED にならない。

## 非対象

- Value発見、R6-G実行、秘密・暗号・宇宙DB。
- ランタイムによる意味的独立性の推論・静かな昇格。
