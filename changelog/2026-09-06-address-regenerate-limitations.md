# 2026-09-06 Address regenerate_limitations helper

## 追加

- `tools/regenerate_limitations.py`：決定的に `fixtures/limitations.json` を再生成（`limitations.limitations()` + sort_keys）。
- `tools/regenerate_all_frozen_docs.py`：limitations + conformance 再生成を一括実行。
- `tools/README.md`：凍結文書 regenerator の一行案内。
- unittest: fixture ↔ module 一致、および regenerator 実行後の安定性。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
