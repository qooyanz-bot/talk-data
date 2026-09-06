# 2026-09-06 Address conformance runner

## 追加

- `conformance.py` と `run_conformance() -> dict`（schema_version / checks / overall CONFORMANT|FAIL）。
- CLI `--conformance`：LIMITATIONS + synthetic battery + R6-G manifest/claim を単一レポートに集約。
  - LIMITATIONS 節は常に status=LIMITATIONS（PASS 能力として再解釈しない）。
  - synthetic: validate VALID；READY value=null；shared-law ABSTAIN value=null。
  - R6-G: MANIFEST_VALID；EXPERIMENT_RESULT は NOT_RUN|BLOCKED（executed=false）。
- 他 standalone モードと相互排他。exit 0 / 非0。

## テスト

- report shape；synthetic VALID/READY/ABSTAIN value=null；R6-G 未実行；flag hygiene；FAIL 時非0。

## 非変更

- 新規 evaluate golden なし。Value発見、R6-G実行、Cortext9/CIVA は対象外。
