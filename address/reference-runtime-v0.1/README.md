# Address Reference Runtime v0.1

依存ライブラリを使わず、`Addressable Concept Architecture v0.1` の最小安全不変条件を検査する参照実装である。

## 対象

- required field、型、最小のConcept / Dimension分離、系譜ハッシュ
- malformed inputの安全な拒否。境界検査は例外停止ではなく `INVALID` を返す。
- Memory scopeの `authorized / versioned / revocable` 要件と、SHA-256で固定したLineage入力参照。
- `world_id`、Memory / Capability scope、Evidence / Law contract、残差のabstain表現
- real worldでの公開・許可済みread/verify scope以外の拒否
- canonical JSONからの安定した `address_id` 再計算
- Evidence Contractの共通authority / generator / semantic law検出。path IDだけの相違は独立性と扱わない。
- Resolution Gateによる `READY_FOR_VERIFICATION` / `ABSTAIN` 判定。証拠不足、共通原因、鮮度切れ、矛盾ではValueを返さない。
- content-addressed Audit Log。Valueやassertion本文を保存せず、Address・証拠digest・判定を再検算可能にする。
- Replay Verifier。保存済み監査ログに対して同じAddress・Evidence・時刻でGateを再実行し、判断と系譜の完全一致を検証する。
- Protocol Claim Gate。凍結・未実行・監査未完了のProtocolから、実験結果又は能力を主張することを防ぐ。
- Response Contract。CLIの公開出力で `value=null`、既知の判定状態、Auditとの判断一致、任意の`protocol_claim`を強制する。
- READY_FOR_VERIFICATIONでもunknown slotは`residual`として未充填のまま残す。Valueは埋めない。
- Protocol Claim GateをCLIの`--protocol-manifest` / `--claim-type`へ接続。
- golden CLI fixtureによる公開契約の構造回帰検査。
- typed `target_value` の機械検査: dict、非空`type`、`value=null`、`residual`はnull又はlist、`no_speculation=true`。
- 事前検証ランタイムでは`lineage.result_sha`をnullに固定し、非null入力を拒否。
- Resolution Gateの`resolution.residual`は、未解決unknown slotと`target_value.residual`ラベルの和集合。`target_value.residual`がnullでもunknownはREADY時に残す。どちらからもValueを埋めない。
- Response Contractは公開応答内の入れ子`lineage.result_sha`非nullを拒否し、事前検証で結果SHAを刻印しない。

- assertion_keyがunknown.slot / residualラベルと文字列衝突しても、residualを消さずvalueにassertion_valueを束縛しない。
- CLI `--check-contract-only RESPONSE.json` で、Gate再実行なしに保存済み公開応答をresponse_contract検証（OK=0、違反は機械可読errorsで非0）。
- 保存済み公開応答のgolden fixture（`fixtures/golden_contract_ok_response.json` = READY、`fixtures/golden_contract_abstain_response.json` = ABSTAIN / shared-law EVIDENCE_REJECTED、`fixtures/golden_contract_contradiction_response.json` = ABSTAIN / CONTRADICTION・同一assertion_keyで衝突するassertion_value）で `--check-contract-only` / `response_contract.validate` の構造を凍結。value充填や入れ子`lineage.result_sha`刻印は失敗する。各goldenはdecision・value=null・residualあり・audit整合を固定。
- `tools/regenerate_contract_goldens.py` が固定入力からevaluate()でREADY/ABSTAIN/CONTRADICTION goldenを再生成し、digestの手編集を不要にする。unittestがfixtureとfresh evaluate()の完全一致を検査する。
- `--check-contract-only` と address/evidence/`--now`/`--audit`/`--protocol-manifest`/`--claim-type` の併用は早期に `INVALID_INPUT`（機械可読JSON・非0）で拒否する。

## 非対象

- Valueの発見、現実の秘密・個人情報・未来値の取得
- Address Lawの自動発見、暗号又は認証の回避
- R6-Gの実装、実験、Holdoutの開封又は実行

## 実行

```text
python -m unittest discover -s address/reference-runtime-v0.1/tests -v
python address/reference-runtime-v0.1/address_runtime.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json
python address/reference-runtime-v0.1/address_cli.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json address/reference-runtime-v0.1/fixtures/valid_evidence_bundle.json --now 2026-09-06T00:00:00Z
python address/reference-runtime-v0.1/address_cli.py --check-contract-only path/to/saved_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_ok_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_abstain_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_contradiction_response.json
python address/reference-runtime-v0.1/tools/regenerate_contract_goldens.py
```

契約goldenの再生成は `python address/reference-runtime-v0.1/tools/regenerate_contract_goldens.py` （固定Address・Evidence・`--now`相当時刻からevaluate()出力を書き戻す）。手編集しない。

結果は `VALID`、又は機械可読な `INVALID` と違反一覧で返す。統合CLIはResolutionとvalue-free Audit Logを返し、`--audit` 指定時はReplayも検証する。`--check-contract-only` はGateを再実行せず、保存済み公開応答の契約だけを検査する（`CONTRACT_OK` / `CONTRACT_INVALID`）。address/evidence/`--now` など解決用引数と併用すると早期に `INVALID_INPUT` JSONで非0終了する。外部接続・ファイル書込み・Value導出はしない。
