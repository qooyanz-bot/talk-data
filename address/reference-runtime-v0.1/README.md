# Address Reference Runtime v0.1

依存ライブラリを使わず、`Addressable Concept Architecture v0.1` の最小安全不変条件を検査する参照実装である。

## 対象

- required field、型、最小のConcept / Dimension分離、系譜ハッシュ
- malformed inputの安全な拒否。境界検査は例外停止ではなく `INVALID` を返す。
- Memory scopeの `authorized / versioned / revocable` 要件と、SHA-256で固定したLineage入力参照。
- `world_id`、Memory / Capability scope、Evidence / Law contract、残差のabstain表現
- `world_id` は `world:synthetic-<non-empty>` のみ受理。`world:real:*` は schema validation で明確な errors により拒否（LIMITATIONS `world_scope=SYNTHETIC_ONLY`）。`REAL_CAPABILITIES` 定数はアーキテクチャ／スキーマ文書用に残すが、このランタイムでは real-domain 経路は到達しない。
- canonical JSONからの安定した `address_id` 再計算
- Evidence Contractの共通authority / generator / semantic law検出。path IDだけの相違は独立性と扱わない。 `assess()` は明示的な `independence` 判定を返す: 共有軸は `COMMON_CAUSE_SUSPECT`（status CONFLICT / accepted=False）、 metadata分離通過は `CONTRACTED`（accepted=True）、 不足・不正は `UNVERIFIED`。 `assess()` は決して `INDEPENDENT` / `AUDITED` を返さない。 AUDITEDへ進むには外部の意味的独立性監査記録が必要で、`assess_audited_independence(audit_record, evidence=...)` が凍結チェックリスト（`auditor_id` / `decision=PASS` / `method` / `evidence_digests` / `audited_at`）を機械検査する。 `evidence_digests` は必ず `{evidence_id, digest}` オブジェクト列（`audit_log.evidence_digest_entries` と同形；裸の digest 文字列は拒否）。 evidence 供給時は evidence_id+digest 対が content-addressed 束と完全一致すること。 チェックリスト通過かつ typed digest一致時のみ `independence=AUDITED`；不完全・偽造・裸文字列・id/digest不一致・別束のPASS監査は `UNMET`。
- Resolution Gateによる `READY_FOR_VERIFICATION` / `ABSTAIN` 判定。 UNVERIFIED/CONTRACTED要求のREADYは `independence=CONTRACTED` のときのみ。 Addressが `semantic_independence: AUDITED` を要求する場合は CONTRACTED証拠 **かつ** 有効な外部 `independence_audit`（`resolve`/`evaluate` の任意引数、CLI `--independence-audit`；typed `{evidence_id, digest}` が供給束の evidence_digest_entries と一致）が必要。 欠落・不完全・偽造・裸文字列 digests・id/digest不一致は `ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`（静かに昇格しない）。 有効監査付きは `READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` でも `value=null`（検証ゲートでありValue発見ではない）。 fixtureの `UNVERIFIED` 要求はCONTRACTED証拠でREADY可。証拠不足、共通原因、鮮度切れ、矛盾ではValueを返さない。
- content-addressed Audit Log。Valueやassertion本文を保存せず、Address・証拠digest・判定を再検算可能にする。
- Replay Verifier。保存済み監査ログに対して同じAddress・Evidence・時刻でGateを再実行し、判断と系譜の完全一致を検証する。
- Protocol Claim Gate。凍結・未実行・監査未完了のProtocolから、実験結果又は能力を主張することを防ぐ。 `validate_manifest(manifest)` が閉集合 enum を機械検査（errors list・例外なし）: evidence_state=`SPEC_ONLY|DIAGNOSTIC_ONLY|RESULT_BACKED`、 implementation_state=`NOT_IMPLEMENTED|IMPLEMENTED`、 experiment_state=`NOT_RUN|COMPLETED`、 independent_replay_state=`NOT_RUN|REPLICATED`、 protocol_id=非空文字列、 auditor_handoff があるとき dict かつキーは厳密に {decision, primary_run_authorized}、 decision=`PENDING|PASS`（fixtures/tests に FAIL は未出現のため含めない；independence_audit の FAIL とは別面）、 primary_run_authorized=bool|null。 `assess_claim` は先に validate_manifest を呼び、errors があれば全 claim_type（DESIGN_DESCRIPTION 含む）で BLOCKED / MANIFEST_INVALID / unmet=errors。未知 enum は design としてすり抜けない。 R6-G FROZEN と既存通過 manifest は green のまま。
- Response Contract。CLIの公開出力で `value=null`、既知の判定状態、Auditとの判断一致、任意の`protocol_claim` / `decision_log` shapeを強制する。
- READY_FOR_VERIFICATIONでもunknown slotは`residual`として未充填のまま残す。Valueは埋めない。
- Protocol Claim GateをCLIの`--protocol-manifest` / `--claim-type`へ接続。
- Decision Log / auditor-handoff surface（`decision_log.py`）。`--protocol-manifest` + `--claim-type` 使用時に evaluate 応答へ `decision_log` を付与（claim_status / claim_reason / unmet / 状態フィールド / auditor_handoff の decision・primary_run_authorized のみ；`value` は常に null；秘密は含めない）。 content-addressed：`decision_log_id` = `decision_log:` + sha256（`audit_log.content_digest` と同じ canonical JSON）を payload から id を除いて付与；`verify()` で改ざん検出。 Response Contract は decision_log があるとき機械可読 shape と有効な decision_log_id を強制：必須キー（schema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff / value / 状態4フィールド / decision_log_id）、schema_version=`decision_log.SCHEMA_VERSION`、value=null、既知 claim_status、protocol_claim.status との非矛盾、auditor_handoff は厳密に {decision, primary_run_authorized}（余分な秘密様キー拒否）；protocol_claim 共存時は claim_reason と protocol_claim.reason の一致、unmet は null 又は文字列 list、protocol_claim.unmet があるときは sorted 等価で一致を要求。build_decision_log は unmet を常に list（空可）で emit。R6-G SPEC_ONLY+EXPERIMENT_RESULT の BLOCKED log を `fixtures/r6g_frozen_decision_log_blocked.json` で凍結（decision_log_id 含む）。 公開応答に decision_log を含む契約 golden `fixtures/golden_contract_decision_log_blocked_response.json`（READY / CONTRACTED_EVIDENCE + protocol_claim BLOCKED + frozen decision_log；value=null throughout）で `--check-contract-only` 経路をピン留め。CLI `--verify-decision-log DECISION_LOG.json` は decision_log.verify のみ実行。
- golden CLI fixtureによる公開契約の構造回帰検査。
- `evidence_requirements.semantic_independence` は閉集合 enum: `UNVERIFIED` | `CONTRACTED` | `AUDITED`。 それ以外は `address_runtime.validate` が例外停止せず明確な errors で拒否する。
- typed `target_value` の機械検査: dict、非空`type`、`value=null`、`residual`はnull又は非空文字列のlist、`no_speculation=true`。
- 機械可読フィールド型の硬化: `entities`は非空`id`/`type`（任意`binding`は非空str）、`relations`は非空`predicate`/`subject`/`object`、`unknown`は非空`slot`＋閉集合status（`NOT_DERIVABLE`|`UNRESOLVED`|`RESIDUAL`|`OPEN`）＋`abstain_if_unresolved=true`、`lineage.protocol_sha`/`schema_sha`/`runtime_sha`はnull又は非空str、`evidence_requirements.minimum_sources`は存在時にint>=1、`goal.id`は非空str、`goal.success_criteria` / `state_constraints` / `capability_scope` / `target_value.residual`（list時）は非空文字列のlist（空要素・非文字列を拒否；capability forbid-tokenは従来どおり；real-world subset検査は `world:real:*` 拒否により不要）。
- canonical serialization: `canonical_dumps` / `canonical_id` は `sort_keys=True` と `separators=(',', ':')` のみ。キー順・空白差は `address_id` を変えない（unittestで固定）。
- 事前検証ランタイムでは`lineage.result_sha`をnullに固定し、非null入力を拒否。
- Resolution Gateの`resolution.residual`は、未解決unknown slotと`target_value.residual`の**非空文字列**ラベルの和集合。無効ラベル（空文字・非文字列）は例外停止せずスキップ。`target_value.residual`がnullでもunknownはREADY時に残す。どちらからもValueを埋めない。
- Response Contractは`resolution.residual`を非空文字列のlistとして強制（空文字・非文字列を拒否）し、既存のresidual+value=null規則を維持。公開応答内の入れ子`lineage.result_sha`非nullを拒否し、事前検証で結果SHAを刻印しない。

- assertion_keyがunknown.slot / residualラベルと文字列衝突しても、residualを消さずvalueにassertion_valueを束縛しない。
- CLI `--check-contract-only RESPONSE.json` で、Gate再実行なしに保存済み公開応答をresponse_contract検証（OK=0、違反は機械可読errorsで非0）。decision_log 付き応答も検証対象（改ざん id・非null value は失敗）。
- CLI `--verify-decision-log DECISION_LOG.json` で decision_log.verify のみ実行（OK=0 / INVALID=1）。resolve / `--limitations` / `--check-contract-only` と相互排他。
- 保存済み公開応答のgolden fixture（`fixtures/golden_contract_ok_response.json` = READY / CONTRACTED_EVIDENCE、`fixtures/golden_contract_abstain_response.json` = ABSTAIN / shared-law EVIDENCE_REJECTED、`fixtures/golden_contract_contradiction_response.json` = ABSTAIN / CONTRADICTION・同一assertion_keyで衝突するassertion_value、`fixtures/golden_contract_stale_response.json` = ABSTAIN / EVIDENCE_STALE・observed_atが`--now`とfreshness max_ageに対して古い、`fixtures/golden_contract_semantic_independence_unmet_response.json` = ABSTAIN / SEMANTIC_INDEPENDENCE_UNMET・Address `semantic_independence=AUDITED` + CONTRACTED証拠（監査欠落）、`fixtures/golden_contract_audited_independence_response.json` = READY / AUDITED_INDEPENDENCE・Address `semantic_independence=AUDITED` + CONTRACTED証拠 + 有効typed `independence_audit`、`fixtures/golden_contract_decision_log_blocked_response.json` = READY / CONTRACTED_EVIDENCE + protocol_claim BLOCKED + R6-G frozen decision_log）で `--check-contract-only` / `response_contract.validate` の構造を凍結。value充填や入れ子`lineage.result_sha`刻印は失敗する。各goldenはdecision・value=null・residualあり・audit整合を固定。
- `tools/regenerate_contract_goldens.py` が固定入力からevaluate()でREADY/ABSTAIN/CONTRADICTION/EVIDENCE_STALE/SEMANTIC_INDEPENDENCE_UNMET/AUDITED_INDEPENDENCE goldenを再生成し、digestの手編集を不要にする。unittestがfixtureとfresh evaluate()の完全一致を検査する。
- `--check-contract-only` / `--verify-decision-log` / `--limitations` は相互排他。address/evidence/`--now`/`--audit`/`--protocol-manifest`/`--claim-type`/`--independence-audit` との併用は早期に `INVALID_INPUT`（機械可読JSON・非0）で拒否する。

- LIMITATIONS / synthetic-only conformance surface（`limitations.py` / `fixtures/limitations.json`）。world_scope=SYNTHETIC_ONLY（`address_runtime.validate` が `world:real:*` を schema validation で拒否し `world:synthetic-...` のみ受理）、value_discovery=NOT_IMPLEMENTED、r6g_experiment=NOT_RUN（reference SPEC_ONLY）、real_domain_extrapolation / secret_access / crypto_bypass / future_direct=FORBIDDEN、audited_independence=EXTERNAL_RECORD_REQUIRED（AUDITEDは外部監査記録が必要でランタイム推論しない）、protocol_result_claims=GATED（結果／能力主張は Protocol Claim Gate + Decision Log でゲート）を機械可読に宣言。CLI `--limitations` でJSON出力（address/evidence不要）。resolve / `--check-contract-only` / `--verify-decision-log` と相互排他。

## 非対象

- Valueの発見、現実の秘密・個人情報・未来値の取得
- Address Lawの自動発見、暗号又は認証の回避
- R6-Gの実装、実験、Holdoutの開封又は実行

## 実行

```text
python -m unittest discover -s address/reference-runtime-v0.1/tests -v
python address/reference-runtime-v0.1/address_runtime.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json
python address/reference-runtime-v0.1/address_cli.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json address/reference-runtime-v0.1/fixtures/valid_evidence_bundle.json --now 2026-09-06T00:00:00Z
python address/reference-runtime-v0.1/address_cli.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json address/reference-runtime-v0.1/fixtures/valid_evidence_bundle.json --now 2026-09-06T00:00:00Z --independence-audit path/to/independence_audit.json
python address/reference-runtime-v0.1/address_cli.py --limitations
python address/reference-runtime-v0.1/address_cli.py --check-contract-only path/to/saved_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_ok_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_abstain_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_contradiction_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_stale_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_semantic_independence_unmet_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_audited_independence_response.json
python address/reference-runtime-v0.1/address_cli.py --check-contract-only address/reference-runtime-v0.1/fixtures/golden_contract_decision_log_blocked_response.json
python address/reference-runtime-v0.1/address_cli.py --verify-decision-log address/reference-runtime-v0.1/fixtures/r6g_frozen_decision_log_blocked.json
python address/reference-runtime-v0.1/tools/regenerate_contract_goldens.py
```

契約goldenの再生成は `python address/reference-runtime-v0.1/tools/regenerate_contract_goldens.py` （固定Address・Evidence・`--now`相当時刻からevaluate()出力を書き戻す）。手編集しない。

結果は `VALID`、又は機械可読な `INVALID` と違反一覧で返す。統合CLIはResolutionとvalue-free Audit Logを返し、`--audit` 指定時はReplayも検証する。`--limitations` はAddress/EvidenceなしでLIMITATIONS文書をJSON出力する（exit 0）。`--check-contract-only` はGateを再実行せず、保存済み公開応答の契約だけを検査する（`CONTRACT_OK` / `CONTRACT_INVALID`；decision_log 付き応答含む）。`--verify-decision-log` は Decision Log の shape / content-address のみを検査する（`DECISION_LOG_OK` / `DECISION_LOG_INVALID`）。`--limitations` / `--check-contract-only` / `--verify-decision-log` と address/evidence/`--now`/`--independence-audit` など解決用引数の併用、又はこれらの相互併用は早期に `INVALID_INPUT` JSONで非0終了する。外部接続・ファイル書込み・Value導出はしない。R6-G実行や現実ドメイン外挿は主張しない。
