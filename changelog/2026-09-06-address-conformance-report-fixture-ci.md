# 2026-09-06 Address conformance report fixture + CI

## 追加

- `fixtures/conformance_report.json`：`run_conformance()` 出力を limitations.json と同様に凍結（決定的・タイムスタンプなし）。
- unittest：fixture と live `run_conformance()` の完全一致。
- CI：`address_cli.py --conformance` を unittest 後に明示実行（exit 0 on green）。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
