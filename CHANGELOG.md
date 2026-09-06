# Changelog

## 2026-09-06 (Address reference-runtime handoff for next agent)

- `address/handoffs/2026-09-06-address-reference-runtime-codex-handoff-continuation.md` を追加（現行 HEAD `3d80682`、実装済み一覧、推奨次増分、検証コマンド）。
- `address/handoffs/2026-09-06-next-agent-prompt.md` を追加（次担当エージェント実行用プロンプト）。
- tests 281 件全緑・conformance CONFORMANT・runtime_manifest 正常・frozen docs --check ok を確認済み。


## 2026-09-06 (Address contradiction_policy closed enum & evidence_contract frozensets)

- `address_runtime.py`: `CONTRADICTION_POLICY_ALLOWED = frozenset({"STOP_AND_REPORT_CONFLICT"})` を単一正本として export し、`validate()` での閉集合検証を適用。
- `address_runtime.py`: `REQUIRED_FIELDS`, `DIMENSIONS`, `REAL_CAPABILITIES`, `FORBIDDEN_CAPABILITY_TOKENS` を `frozenset` 定数化。
- `evidence_contract.py`: `REQUIRED_FIELDS` および `INDEPENDENCE_AXES` を `frozenset` 定数として export（`REQUIRED` はエイリアス維持）。


## 2026-09-06 (Address audit_log closed enum verification & CLI --verify-audit-log)

- `audit_log.py`: `SCHEMA_VERSION = "ADDRESS-AUDIT-1.0"` および `REQUIRED_KEYS` を export。`verify()` で `decision` (`resolution_gate.DECISION_ALLOWED`) および `reason` (`resolution_gate.REASON_ALLOWED`) の閉集合検査を追加し、改ざん・不正語彙の監査ログを厳密に拒否。
- `response_contract.py`: `DECISION_LOG_REQUIRED_KEYS` を `decision_log.REQUIRED_KEYS` から単一正本として参照。
- `address_cli.py`: `--verify-audit-log AUDIT.json` モードを追加。スタンドアロンの Audit Log を構造・閉集合・content-address で検証（`AUDIT_LOG_OK` exit 0 / `AUDIT_LOG_INVALID` exit 1 / 相互排他 `INVALID_INPUT` exit 2）。


## 2026-09-06 (Address runtime_manifest content-hash helper & conformance checks single-source)

- `runtime_manifest.py`: 凍結ファイル一覧（12モジュール）のLF正規化SHA-256およびパッケージダイジェスト（`package_digest()` → `sha256:<64 hex>`）を生成・検証するヘルパーを実装。
- Address `lineage.runtime_sha` から引用可能な実装ダイジェストとして文書化（全Addressに強制せず、null許可は維持）。
- CLI `--runtime-manifest` フラグを追加（他standaloneモードと相互排他、exit 0）。
- `fixtures/runtime_manifest.json` および再生成ツール `tools/regenerate_runtime_manifest.py` を追加、`tools/regenerate_all_frozen_docs.py` へ統合。
- `conformance.py`: `CHECK_IDS_ALLOWED` および `CHECK_STATUSES_ALLOWED` 閉集合frozensetを単一正本としてexportし、テスト内ハードコードと統合。
- CIワークフローへ `--runtime-manifest` 実行を追加。


## 2026-09-06 (Address evidence_contract status closed enum)

- `evidence_contract.ASSESS_STATUS_ALLOWED` = {INSUFFICIENT, INVALID, CONFLICT, CONTRACTED} を単一正本（assess emitters）。`_result` が status も軽量 assert。
- `evidence_contract.AUDIT_STATUS_ALLOWED` = {AUDITED, UNMET} を単一正本（assess_audited_independence emitters）。`_audit_result` が status も軽量 assert（independence とは別フィールド）。
- unittest：全 status emitters が閉集合内；assess status は AUDITED/UNMET を含めない；両集合は disjoint。新規 evaluate golden なし。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address independence verdict closed enum single-source)

- `evidence_contract.INDEPENDENCE_ASSESS_ALLOWED` = {COMMON_CAUSE_SUSPECT, CONTRACTED, UNVERIFIED} を単一正本（assess emitters）。`_result` が軽量 assert。決して INDEPENDENT / AUDITED を含まない。
- `evidence_contract.INDEPENDENCE_AUDIT_ALLOWED` = {AUDITED, UNMET} を単一正本（assess_audited_independence emitters）。`_audit_result` が軽量 assert。
- response_contract / resolution_gate は independence を公開フィールドとして検証しない（export + emitter tests のみ）。unittest：emitters が閉集合内；assess は INDEPENDENT なし。新規 evaluate golden なし。Value発見・R6-G実行は行わない。


## 2026-09-06 (Cortext9 Reception runtime v0)
- Reception＋535単位の実装リポジトリを作成・初回実装: https://github.com/qooyanz-bot/cortext9-reception (`3fec520`)
- カタログ v0.4 全535登録、`/v0/invoke`・`/v0/reception/chat`、Gate0、優先ハンドラ43（N18/N03/N06/N12系ほか）。残りはスタブ。
- Tiny runtime（logical_id線）とは別リポ・別契約。Concept確定・統一プロンプト改訂はなし。

## 2026-09-06 (Address REASON_ALLOWED single-source)

- `resolution_gate.REASON_ALLOWED` = {ADDRESS_INVALID, AUDITED_INDEPENDENCE, CONTRACTED_EVIDENCE, CONTRADICTION, EVIDENCE_REJECTED, EVIDENCE_STALE, EVIDENCE_TIME_INVALID, FRESHNESS_REQUIREMENT_INVALID, SEMANTIC_INDEPENDENCE_UNMET} を単一正本（resolve emitters）。`_result` が軽量 assert。
- `response_contract.REASONS` は同一 frozenset エイリアス；`validate` が `resolution.reason` を検査。
- unittest：未知 reason は contract 拒否；共有 identity（`is`）；happy path / golden 通過。新規 evaluate golden なし。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address DECISIONS + REPLAY_STATUSES single-source)

- `resolution_gate.DECISION_ALLOWED` = {ABSTAIN, READY_FOR_VERIFICATION} を単一正本（resolve emitters）。`_result` が軽量 assert。
- `replay_verifier.REPLAY_STATUS_ALLOWED` = {REPLAY_VERIFIED, REPLAY_MISMATCH, LINEAGE_MISMATCH, INVALID_AUDIT} を単一正本（verify_replay emitters）。`_status_result` が軽量 assert。
- `response_contract.DECISIONS` / `REPLAY_STATUSES` は同一 frozenset エイリアス（ローカル set 廃止）。
- unittest：未知 decision/replay status は contract 拒否；共有 identity（`is`）；happy path 通過。新規 evaluate golden なし。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address claim_status closed enum)

- `protocol_claim_gate.CLAIM_STATUS_ALLOWED` = {ALLOWED_AS_DESIGN, ALLOWED_AS_RESULT, BLOCKED} を単一正本（assess_claim status emitters）。
- `decision_log.verify` が claim_status（非 null）閉集合を強制。`response_contract.PROTOCOL_CLAIM_STATUSES` は同一 frozenset エイリアス（protocol_claim / decision_log 双方）。
- unittest：未知 status は verify 失敗；共有定数；happy path / R6-G frozen fixture 通過。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address claim_reason closed enum)

- `protocol_claim_gate.CLAIM_REASON_ALLOWED` = {NO_RESULT_CLAIM, EVIDENCE_GATES_UNMET, MANIFEST_INVALID, CLAIM_TYPE_UNKNOWN, CAPABILITY_EVIDENCE_NOT_RESULT_BACKED, RECORDED_EVIDENCE_GATES_PASS} を単一正本（assess_claim が実際に emit する全 reason）。
- `decision_log.verify` が claim_reason（非 null）閉集合を強制。非 dict assessment の fallback は `ASSESSMENT_INVALID` をやめ `MANIFEST_INVALID`（gate reason のみ）。
- Response Contract は既存どおり `decision_log.verify` 経由で同一検査。unittest：未知 reason は verify/contract 失敗；happy path / R6-G frozen fixture は通過。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address claim_type closed enum)

- `protocol_claim_gate.CLAIM_TYPE_ALLOWED` = {DESIGN_DESCRIPTION, EXPERIMENT_RESULT, CAPABILITY_CLAIM} を単一正本；`assess_claim` が未知を BLOCKED / CLAIM_TYPE_UNKNOWN。
- `decision_log.verify` が claim_type 閉集合を強制（空・UNKNOWN 拒否）。CLI は `--protocol-manifest` に `--claim-type` 必須、未知は INVALID_INPUT。
- unittest：verify 拒否、CLI 拒否、共有定数。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address regenerator --check + CI drift)

- `tools/regenerate_limitations.py` / `regenerate_conformance_report.py` / `regenerate_all_frozen_docs.py` に `--check`：dry-run；on-disk fixture が生成内容と一致すれば exit 0、書き換えが必要なら非0（書込みなし）。
- CI `.github/workflows/address-reference-runtime.yml` に `python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check` ステップを追加。
- unittest：`--check` 成功（一致）と失敗（temp mutate / mismatch・書込みなし）。tools/README + package README 更新。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address regenerate_limitations + all_frozen_docs)

- `tools/regenerate_limitations.py`：`limitations()` から `fixtures/limitations.json` を決定的に再生成。`tools/regenerate_all_frozen_docs.py` で limitations + conformance 一括再生成。unittest が fixture 一致と regenerator 安定性を検査。
- tools/README 追加。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address regenerate_conformance_report helper)

- `tools/regenerate_conformance_report.py`：`run_conformance()` から `fixtures/conformance_report.json` を決定的に再生成（手編集不要）。unittest の fixture 一致検査と対。
- README に実行例を追記。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address conformance report fixture + CI)

- `fixtures/conformance_report.json` を `limitations.json` と同様に凍結（`run_conformance()` の決定的出力；タイムスタンプなし）。unittest が fixture と live `run_conformance()` の完全一致を検査。
- CI `.github/workflows/address-reference-runtime.yml` に `python address/reference-runtime-v0.1/address_cli.py --conformance` ステップを追加（unittest の後；green main で exit 0）。
- README 更新。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address conformance runner)

- `conformance.py` / `run_conformance() -> dict`：機械可読適合レポート（`schema_version=address-conformance-v1`、`checks: [{id, status, detail}]`、overall=`CONFORMANT`|`FAIL`）。
- 集約: LIMITATIONS 文書（status=`LIMITATIONS`、PASS 再解釈なし）；synthetic validate VALID + evaluate READY value=null + shared-law ABSTAIN value=null；R6-G frozen manifest MANIFEST_VALID；EXPERIMENT_RESULT は NOT_RUN|BLOCKED（実行済み主張なし）。
- CLI `--conformance`（他 standalone / resolve と相互排他）。exit 0=CONFORMANT、FAIL があれば非0。
- unittest：report shape、synthetic VALID/READY value=null、R6-G 未実行、flag hygiene。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address CLI --validate-protocol-manifest)

- CLI `--validate-protocol-manifest MANIFEST.json` を追加：`protocol_claim_gate.validate_manifest` のみ実行。成功時 exit 0 + `{status: MANIFEST_VALID, errors: []}`；失敗時非0 + `{status: MANIFEST_INVALID, errors: [...]}`（INVALID_INPUT / CONTRACT 系と同形）。
- resolve / `--limitations` / `--check-contract-only` / `--verify-decision-log` と相互排他（既存 standalone hygiene）。
- unittest：R6-G frozen fixture VALID；未知 enum INVALID；flag combo 拒否。新規 evaluate golden なし。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address decision_log closed-enum mirror)

- `protocol_claim_gate` の閉集合 frozenset（`STATE_ENUMS` / `EVIDENCE_STATE_ALLOWED` 等 / `AUDITOR_HANDOFF_*`）を単一正本として export；`decision_log.verify` が状態フィールド（非 null）と `auditor_handoff.decision`（非 null → PENDING|PASS）および handoff キー厳密集合を同じ集合で検査。
- Response Contract は decision_log 存在時に `decision_log.verify` 経由で同一 enum 検査（単一路）；handoff キー定数は `AUDITOR_HANDOFF_KEYS` を共有。
- unittest：`evidence_state="EXECUTED"` 改ざんは verify/contract 失敗；R6-G frozen fixture / valid manifest の build_decision_log は通過。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address protocol manifest closed-enum validation)

- `protocol_claim_gate.validate_manifest(manifest) -> list[str]`：manifest 状態フィールドの閉集合 enum を機械検査（例外なし）。evidence_state / implementation_state / experiment_state / independent_replay_state；protocol_id 非空文字列；auditor_handoff があるときキーは厳密に {decision, primary_run_authorized}、decision=`PENDING|PASS`（FAIL は fixtures/tests 未出現のため未採用）、primary_run_authorized=bool|null。
- `assess_claim` は先に validate；errors 時は全 claim_type（DESIGN_DESCRIPTION 含む）で BLOCKED / MANIFEST_INVALID / unmet=errors。未知 enum は design すり抜け不可。
- R6-G FROZEN と既存通過 manifest は green。unittest：未知 evidence_state / typo experiment_state / 余分 handoff キー / 空 protocol_id / DESIGN の無効 enum。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address residual defense in depth)

- Resolution Gate: `target_value.residual` から `resolution.residual` へミラーするとき、非空文字列ラベルのみ emit（空文字・非文字列は例外停止せずスキップ）。
- Response Contract: `resolution.residual` は非空文字列の list（空文字・非文字列を拒否）；既存の residual+value=null 規則は維持。
- unittest: 不正 residual 要素の contract 拒否；Gate のスキップ；READY/ABSTAIN happy path は通過。新規 golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address synthetic-only validate enforcement)

- `address_runtime.validate` が LIMITATIONS `world_scope=SYNTHETIC_ONLY` を強制: `world:real:*` は明確な errors で INVALID；`world:synthetic-<non-empty>` のみ受理（空 suffix 拒否）。
- `target_value.residual` が list のとき要素は非空文字列（機械可読）。
- `REAL_CAPABILITIES` はスキーマ文書用に残置；real-world capability subset 検査は削除（real world は validate で先に失敗）。unittest / README / LIMITATIONS を整合。新規 golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address check-contract-only decision_log response)

- 公開応答 golden `fixtures/golden_contract_decision_log_blocked_response.json` を追加（evaluate(..., protocol_manifest=R6-G, claim_type=EXPERIMENT_RESULT): READY / CONTRACTED_EVIDENCE + protocol_claim BLOCKED + frozen decision_log；value=null throughout）。regenerator には未配線（golden 増殖を抑制）。
- `--check-contract-only` が decision_log 付き応答を通過；改ざん decision_log_id / 非null decision_log.value で CONTRACT_INVALID。
- CLI `--verify-decision-log DECISION_LOG.json` を追加（decision_log.verify のみ；`--limitations` / `--check-contract-only` / resolve と相互排他）。
- Value発見・R6-G実行は行わない。

## 2026-09-06 (Address content-addressed decision_log_id)

- `decision_log.build_decision_log` / `create` が `decision_log_id` = `decision_log:` + sha256（`audit_log.content_digest` と同じ canonical dumps）を id 除外 payload から付与。`verify()` で必須 shape と自己アドレス整合を検査。
- Response Contract は decision_log 存在時に `decision_log_id` 必須＋`decision_log.verify` を要求（改ざん・欠落を拒否）。
- 凍結 fixture `r6g_frozen_decision_log_blocked.json` を再生成（正しい decision_log_id）。unittest：同一入力で id 安定・改ざん検出・contract が有効 id を要求。新規 evaluate golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address decision_log claim_reason / unmet align)

- Response Contract：`decision_log` と `protocol_claim` が両方あるとき、`claim_reason` を `protocol_claim.reason`（reason がある場合）と一致要求；`unmet` は null 又は文字列 list；`protocol_claim.unmet` があるときは sorted 等価（multiset）で一致要求。
- `decision_log.py` は `unmet` を常に list（空可）で出力（機械可読）。R6-G 凍結 BLOCKED fixture は list のまま変更なし。新規 CLI evaluate golden なし。
- unittest：reason mismatch / unmet non-list / unmet mismatch；happy path は R6-G frozen BLOCKED log で通過。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address decision_log Response Contract shape)
- Response Contract が `decision_log` 存在時に機械可読 shape を強制：必須キー（schema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff / value / 状態4フィールド）、schema_version=`decision_log.SCHEMA_VERSION`、value=null、既知 claim_status、protocol_claim.status 非矛盾、auditor_handoff は厳密に {decision, primary_run_authorized}。
- unittest で missing schema_version / wrong handoff keys / non-null value / status mismatch を固定。新規 golden なし。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address Protocol Claim Decision Log / auditor-handoff)
- `decision_log.py` を追加。manifest + claim_type + `assess_claim` 結果から value-free な Decision Log（schema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff の decision・primary_run_authorized のみ / 状態フィールド / value=null）を構築。
- R6-G SPEC_ONLY + EXPERIMENT_RESULT → BLOCKED を `fixtures/r6g_frozen_decision_log_blocked.json` で凍結。CLI は既存 `--protocol-manifest` / `--claim-type` 経路で `decision_log` を evaluate 応答に付与。
- Response Contract は decision_log があるとき value=null・既知 claim_status・protocol_claim.status 非矛盾を要求。LIMITATIONS に `protocol_result_claims=GATED`。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address AUDITED_INDEPENDENCE READY golden)
- 公開応答 READY golden `fixtures/golden_contract_audited_independence_response.json` を追加（Address `semantic_independence=AUDITED` + CONTRACTED証拠 + 有効typed `independence_audit`（`{evidence_id, digest}` が束と一致）→ READY_FOR_VERIFICATION / AUDITED_INDEPENDENCE / value=null・residualあり・audit整合）。SEMANTIC_INDEPENDENCE_UNMET goldenの成功対称。
- `tools/regenerate_contract_goldens.py` / match-evaluate / `--check-contract-only` 専用unittestに配線。value充填・入れ子 `lineage.result_sha`・reason非AUDITED_INDEPENDENCEで失敗する回帰を凍結。
- Value発見・R6-G実行・静かな昇格ショートカットは行わない。

## 2026-09-06 (Address typed independence_audit evidence_digests)
- `independence_audit.evidence_digests` を常に `{evidence_id, digest}` オブジェクト列に固定（`audit_log.evidence_digest_entries` と同形）。裸の digest 文字列は凍結チェックリストで `UNMET`。
- evidence 供給時は evidence_id+digest 対が content-addressed 束と完全一致。id または digest の不一致 → `SEMANTIC_INDEPENDENCE_UNMET`；正しいオブジェクト列 → `READY_FOR_VERIFICATION` / `value=null`。
- `assess()` 単体は引き続き決して AUDITED を返さない。Value発見・R6-G実行・静かな AUDITED 昇格は行わない。

## 2026-09-06 (Address independence_audit evidence_digests binding)
- `assess_audited_independence(audit_record, evidence=...)` が `evidence_digests` を供給エビデンス束の content-addressed digest（`audit_log.content_digest` / `evidence_digest_entries` と同一アルゴリズム）と完全一致要求。別束への PASS 監査では AUDITED にならない。
- Resolution Gate は AUDITED 要求時に evidence を監査検査へ渡す。不一致 → `ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`；一致＋チェックリスト通過 → `READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` / `value=null`。
- `assess()` 単体は引き続き決して AUDITED を返さない。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address AUDITED path requires external independence_audit)
- Evidence Contract に凍結チェックリスト（`auditor_id` / `decision=PASS` / `method` / `evidence_digests` / `audited_at`）と `assess_audited_independence()` を追加。通過時のみ `independence=AUDITED`；`assess()` は引き続き決して AUDITED/INDEPENDENT を返さない（path多様性・metadata分離だけでは昇格しない）。
- Resolution Gate / `evaluate` / CLI `--independence-audit` を配線。Address が `semantic_independence=AUDITED` のとき CONTRACTED証拠 **かつ** 有効監査記録が必要。欠落・不完全・偽造 → `ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`；有効 → `READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` でも `value=null`。
- LIMITATIONS に `audited_independence=EXTERNAL_RECORD_REQUIRED` を追加。Value発見・R6-G実行は行わない。


## 2026-09-06 (Address remaining machine-checkable string-list types)
- `address_runtime.validate` に `goal.id`（非空文字列）、`goal.success_criteria` / `state_constraints` / `capability_scope`（非空文字列の list；空要素・非文字列拒否）を追加。`capability_scope` の forbid-token / real-world subset は維持。
- `valid_synthetic_address.json` は VALID のまま（address_id 非書換）。各拒否を unittest で固定。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address machine-checkable field types / canonical serialization)
- `address_runtime.validate` に entities / relations / unknown / lineage sha / minimum_sources の機械可読型検査を追加。例外停止せず errors リストで拒否。valid_synthetic_address.json は VALID のまま。
- `canonical_dumps` を明示し、`canonical_id` が `sort_keys=True` + `separators=(',', ':')` のみを使うことを文書化・unittest固定（キー順・空白は address_id 不変）。
- Open work「各フィールドの機械可読型と正規直列化」への実装増分。Value発見・R6-G実行は行わない。

## 2026-09-06 (Address semantic_independence closed enum + UNMET golden)
- `address_runtime.validate` が `evidence_requirements.semantic_independence` を閉集合 enum（`UNVERIFIED` | `CONTRACTED` | `AUDITED`）として強制。他値は例外停止せず明確な errors で拒否。
- 公開応答 golden `fixtures/golden_contract_semantic_independence_unmet_response.json` を追加（Address `semantic_independence=AUDITED` + CONTRACTED証拠 → ABSTAIN / SEMANTIC_INDEPENDENCE_UNMET / value=null・residualあり・audit整合）。regenerator / match-evaluate に配線。
- 無効 enum・AUDITED+CONTRACTED ABSTAIN・UNVERIFIED fixture READY の回帰をunittestで固定。

## 2026-09-06 (Address evidence independence / common-cause verdict)
- Evidence Contract `assess()` に明示的な `independence` 判定を追加: 共有authority/generator/semantic_law（又は重複identity）は `COMMON_CAUSE_SUSPECT`（CONFLICT）、metadata分離通過は `CONTRACTED`、不足・不正は `UNVERIFIED`。path IDだけでは `INDEPENDENT` / `AUDITED` を返さない。
- Resolution Gateは READY_FOR_VERIFICATION を `independence=CONTRACTED` のときのみ許可。Addressが `semantic_independence: AUDITED` なのに証拠がCONTRACTED止まりの場合は `ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`。`UNVERIFIED` 要求（valid_synthetic_address.json）は従来どおりCONTRACTEDでREADY。value=null維持。

## 2026-09-06 (Address LIMITATIONS / synthetic-only conformance)
- `limitations.py` と `fixtures/limitations.json` を追加。world_scope=SYNTHETIC_ONLY、value_discovery=NOT_IMPLEMENTED、r6g_experiment=NOT_RUN（SPEC_ONLY）、real_domain_extrapolation / secret_access / crypto_bypass / future_direct=FORBIDDEN を機械可読に宣言。CLI `--limitations` でJSON出力（exit 0）。resolve / `--check-contract-only` と相互排他。R6-G実行・Value発見・現実外挿は主張しない。

## 2026-09-06 (Address contract-only EVIDENCE_STALE golden)
- 公開応答EVIDENCE_STALE golden `fixtures/golden_contract_stale_response.json` を追加（observed_atが`--now`とfreshness max_ageに対して古い実evaluate出力: ABSTAIN / EVIDENCE_STALE / value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value充填・入れ子 `lineage.result_sha`・reason非EVIDENCE_STALEで失敗する回帰をREADY/ABSTAIN/CONTRADICTIONと対称に凍結。
- `tools/regenerate_contract_goldens.py` と match-evaluate unittest に EVIDENCE_STALE を追加。

## 2026-09-06 (Address contract-only CONTRADICTION golden + regenerator)
- 公開応答CONTRADICTION golden `fixtures/golden_contract_contradiction_response.json` を追加（同一assertion_keyで衝突するassertion_valueの実evaluate出力: ABSTAIN / CONTRADICTION / value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value充填・入れ子 `lineage.result_sha`・reason非CONTRADICTIONで失敗する回帰をREADY/ABSTAINと対称に凍結。
- `tools/regenerate_contract_goldens.py` でREADY/ABSTAIN/CONTRADICTION goldenをevaluate()から再生成可能に。unittestがfixtureとfresh evaluate()の完全一致を検査する。

## 2026-09-06 (Address contract-only ABSTAIN golden)
- 公開応答ABSTAIN golden `fixtures/golden_contract_abstain_response.json` を追加（shared-law EVIDENCE_REJECTED の実evaluate出力: value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value充填・入れ子 `lineage.result_sha`・decision非ABSTAINで失敗する回帰をREADY goldenと対称に凍結。

## 2026-09-06 (Address contract-only golden fixture + argparse harden)
- 公開応答golden fixture `fixtures/golden_contract_ok_response.json` を追加（value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value充填や入れ子 `lineage.result_sha` 刻印で失敗する回帰を凍結。
- `--check-contract-only` と address/evidence/`--now`/resolve系フラグの併用を早期 `INVALID_INPUT` JSON で拒否。

## 2026-09-06 (Address assertion/residual collision + contract-only CLI)
- Evidence `assertion_key` が unknown.slot / residual ラベルと衝突しても residual を解消せず、`assertion_value` を value に束縛しない（READYでも value=null）。
- Address CLI に `--check-contract-only RESPONSE.json` を追加。Gate再実行なしで公開応答の response_contract を検証（OK=0、違反は機械可読 errors で非0）。

## 2026-09-06 (Audit Log malformed-input hardening)
- Audit Logのevidence digest項目がobjectでない場合も、例外停止せず明示的に拒否するよう修正。

## 2026-09-06 (Address memory and lineage boundaries)
- Memory scopeにauthorized/versioned/revocableを必須化し、Lineageの入力参照をSHA-256形式に限定。未許可・追跡不能なMemory／入力参照を拒否する。

## 2026-09-06 (Address response contract)
- CLI出力のResponse Contractを追加。Value非返却、既知の判定状態、Auditとの判断一致を検証し、将来の出力回帰を防ぐ。

## 2026-09-06 (Address reference runtime CI)
- `address/reference-runtime-v0.1/` の変更時に全unittestを実行する最小GitHub Actions CIを追加。外部データ、秘密、実世界Valueの取得は行わない。

## 2026-09-06 (Historical Raw Archive documentation)
- READMEに `archives/md-original/` の目的、利用上の正本性区分、安全な参照手順を追加。
- Raw Archiveを承認済み判断・再現可能なEvidence・未検証仮説と混同しないこと、秘密情報の再記録・復元をしないことを明記。

## 2026-09-06 (Address reference runtime v0.1)
- read-only Address CLIを追加。Address JSONとEvidence JSONを一括評価し、Resolution、value-free Audit Log、任意のReplay検証を返す。Value導出・外部接続・ファイル書込みは行わない。
- Protocol Claim Gateを追加。R6-Gの直接確認済みmanifest状態を対象に、`NOT_RUN`・監査未完了・未実装から実験結果／能力主張へ飛躍することをブロックする。
- Address Runtimeの型・時間・scope境界を強化。malformed inputを例外停止せず `INVALID` として返し、時間逆転、真偽値threshold、非JSON値などを拒否する。
- Replay Verifierを追加。保存された監査ログを自己ハッシュだけでなく、同一Address・Evidence・時刻でGateを再実行して検証する。入力、系譜、判断の不一致を検出する。
- content-addressed Audit Logを追加。値とassertion本文を記録せず、Address ID、証拠digest、判定、時刻から再計算可能な監査IDを生成・検証する。
- Resolution Gateを追加。Address・Evidence Contract・鮮度・assertion矛盾を統合し、失敗時はすべて `ABSTAIN` と `value=null` を返す。
- Evidence Contract evaluatorを追加。authority、generator、semantic lawの共有を検出し、別pathでも独立性とは認定しない。metadata分離を通過しても `CONTRACTED` とし、semantic independenceの監査済み主張はしない。
- Addressable Concept Architecture v0.1 の最小安全不変条件を検査する依存なしの参照実装、fixture、unittestを `address/reference-runtime-v0.1/` に追加。秘密・認証回避・直接未来取得を含むscope、hash不整合、abstain不備を拒否する。

## 2026-09-06 (Addressable Concept Architecture v0.1)
- K承認により、検証可能なAddress SchemaとEvidence境界を `address/addressable-concept-architecture-v0.1.md` に追加。R6-G未実行、既存結果のsynthetic限定性、Law不確実時のabstain要件を明記。

## 2026-09-06 (ChatGPT export archive)
- 380会話・17,957メッセージの公開用会話アーカイブを `archives/2026-09-06/` に追加。秘密形式・メール・電話番号を不可逆に置換し、原本HTML・添付本体・セッションIDは含めない。分析は草案であり、会話内容を正本の決定として自動採用しない。
- 同じ会話を `archives/md-original/` に日付順・1会話1Markdownとして追加。会話内容由来の題名とし、公開安全の伏せ字以外の本文を保全する。

## 2026-09-05 (Cortext9 units v0.4)
- 圧勝単位をさらに細分化。v0.3の359から拡張（薄い安全系ドメインの子＋N151–N212）。カタログ `future-concept/Cortext9-unit-catalog-v0.4.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.4-addendum.md`。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05 (Cortext9 units v0.3)
- 圧勝単位をさらに細分化。v0.2の218から拡張（N51–N90の子＋N91–N150系、writing/life_safe/ml_ops運用単位）。カタログ `future-concept/Cortext9-unit-catalog-v0.3.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.3-addendum.md`。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05 (Cortext9 units v0.2)
- 圧勝単位をさらに細分化。v0.1の102から拡張（N19–N50の子ID＋N51–N90系）。カタログ `future-concept/Cortext9-unit-catalog-v0.2.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.2-addendum.md`。ml_ops（振り分け・評価・拒否ゴールデン）追加。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05
- Cortext9 圧勝単位を細分化（N01–N18 の子ID＋N19–N50）。カタログ `future-concept/Cortext9-unit-catalog-v0.1.json`、追記スキーマ `future-concept/Cortext9-unit-api-schema-v0.1-addendum.md`。非断定の安全単位 N43–N46 を追加。断定の医療・法律・軍事は引き続き禁止。
