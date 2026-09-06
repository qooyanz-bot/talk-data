# 2026-09-06 Address DECISIONS + REPLAY_STATUSES single-source

## 追加

- `DECISION_ALLOWED` 閉集合（ABSTAIN | READY_FOR_VERIFICATION）。
- `REPLAY_STATUS_ALLOWED` 閉集合（REPLAY_VERIFIED | REPLAY_MISMATCH | LINEAGE_MISMATCH | INVALID_AUDIT）。
- response_contract が両 frozenset をエイリアス共有。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
