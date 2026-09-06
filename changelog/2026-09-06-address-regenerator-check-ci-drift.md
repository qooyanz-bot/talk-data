# 2026-09-06 Address regenerator --check + CI drift

## 追加

- `regenerate_limitations.py` / `regenerate_conformance_report.py` / `regenerate_all_frozen_docs.py` に `--check`（dry-run drift 検出；一致=0、不一致=非0・書込みなし）。
- CI: `tools/regenerate_all_frozen_docs.py --check`。
- unittest: `--check` 成功／temp mutate 失敗。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
