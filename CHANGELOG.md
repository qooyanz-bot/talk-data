# Changelog

## 2026-09-07 (Physical AI Loop P0 demo implemented)

- `changelog/2026-09-07-physical-ai-loop-p0-demo-implemented.md` ��ǉ��B
- ������ƃf�B���N�g���� P0 ���֐����[�v�E�������O�E�f�� UI�E`npm test`�EREADME disclaimer ���L�^�i���@�����؁^�h�������񋉊����͔�咣�j�B
## 2026-09-07 (newmo Physical AI demo session + Grok handoff)

- K明示持E��により、newmo向けチE��経緯・採用方針�E実裁E��態を正本へ保存、E
- 追加: `changelog/2026-09-07-newmo-physical-ai-demo-session.md`
- 追加: `future-concept/cortext9-physical-ai-improvement-loop-v0.md`�E�採用チE��方針草案、EC最終ではなぁE��E
- 追加: `future-concept/handoffs/2026-09-07-grok-physical-ai-loop-agent-prompt.md`�E�次拁E��Grok用プロンプト�E�E
- 実裁E��業チE��レクトリはローカルにスターター生�E済みだが、デモ本体ロジチE��は未実裁E��記録、E

## 2026-09-06 (CharacterOS platform v1 approved specification)

- `characteros/` を新設し、K承認済みのCharacterOS-Engine / Operation / Client / Tool / Pay / Market / Gate / BASE初版仕様を追加、E
- 未検証のストア、法務、決済、GPU、スケール条件は公開前ゲートとして刁E��し、確定事実として記録しなぁE��E

## 2026-09-06 (Address CLI standalone mode mutual-exclusion matrix test)

- `test_address_cli.py` に `test_standalone_modes_mutually_exclusive_matrix` を追加、E
- 全 7 スタンドアロンモード！E--limitations` / `--runtime-manifest` / `--conformance` / `--check-contract-only` / `--verify-decision-log` / `--verify-audit-log` / `--validate-protocol-manifest`�E�が、他�E 6 モードおよ�E全解決引数�E�Eddress/evidence位置引数・`--now`・`--audit`・`--independence-audit`・`--protocol-manifest`・`--claim-type`�E�と同時持E��された場合に `INVALID_INPUT` / exit 2 になることを�E絁E��合わせ横断で固定、E
- unittest: 285 tests 全緑、E


## 2026-09-06 (Address cross-module vocabulary alias identity test)

- `test_response_contract.py` に `test_all_alias_identities_single_source` と `test_protocol_claim_statuses_alias_single_source` を追加、E
- `response_contract` の全公開語彙エイリアス�E�EDECISIONS`/`REASONS`/`REPLAY_STATUSES`/`PROTOCOL_CLAIM_STATUSES`�E�が、各 emitter module�E�Eresolution_gate`/`replay_verifier`/`protocol_claim_gate`�E��E同一 `frozenset` オブジェクトであること�E�Eis` 一致�E�値一致�E�を単一の横断チE��トで固定、E
- unittest: 284 tests 全緑、E


## 2026-09-06 (Address decision_log REQUIRED_KEYS frozenset single-source)

- `decision_log.REQUIRED_KEYS` めE`frozenset` に変更し、`response_contract.DECISION_LOG_REQUIRED_KEYS` と単一正本化（同一 object `is` 一致 + 値一致めEunittest で固定）、E
- `fixtures/runtime_manifest.json` を�E凍結、E
- unittest: 282 tests 全緑、E


## 2026-09-06 (Address reference-runtime handoff for next agent)

- `address/handoffs/2026-09-06-address-reference-runtime-codex-handoff-continuation.md` を追加�E�現衁EHEAD `3d80682`、実裁E��み一覧、推奨次増�E、検証コマンド）、E
- `address/handoffs/2026-09-06-next-agent-prompt.md` を追加�E�次拁E��エージェント実行用プロンプト�E�、E
- tests 281 件全緑�Econformance CONFORMANT・runtime_manifest 正常・frozen docs --check ok を確認済み、E


## 2026-09-06 (Address contradiction_policy closed enum & evidence_contract frozensets)

- `address_runtime.py`: `CONTRADICTION_POLICY_ALLOWED = frozenset({"STOP_AND_REPORT_CONFLICT"})` を単一正本として export し、`validate()` での閉集合検証を適用、E
- `address_runtime.py`: `REQUIRED_FIELDS`, `DIMENSIONS`, `REAL_CAPABILITIES`, `FORBIDDEN_CAPABILITY_TOKENS` めE`frozenset` 定数化、E
- `evidence_contract.py`: `REQUIRED_FIELDS` および `INDEPENDENCE_AXES` めE`frozenset` 定数として export�E�EREQUIRED` はエイリアス維持E��、E


## 2026-09-06 (Address audit_log closed enum verification & CLI --verify-audit-log)

- `audit_log.py`: `SCHEMA_VERSION = "ADDRESS-AUDIT-1.0"` および `REQUIRED_KEYS` めEexport。`verify()` で `decision` (`resolution_gate.DECISION_ALLOWED`) および `reason` (`resolution_gate.REASON_ALLOWED`) の閉集合検査を追加し、改ざん・不正語彙�E監査ログを厳寁E��拒否、E
- `response_contract.py`: `DECISION_LOG_REQUIRED_KEYS` めE`decision_log.REQUIRED_KEYS` から単一正本として参�E、E
- `address_cli.py`: `--verify-audit-log AUDIT.json` モードを追加。スタンドアロンの Audit Log を構造・閉集合�Econtent-address で検証�E�EAUDIT_LOG_OK` exit 0 / `AUDIT_LOG_INVALID` exit 1 / 相互排仁E`INVALID_INPUT` exit 2�E�、E


## 2026-09-06 (Address runtime_manifest content-hash helper & conformance checks single-source)

- `runtime_manifest.py`: 凍結ファイル一覧�E�E2モジュール�E��ELF正規化SHA-256およびパッケージダイジェスト！Epackage_digest()` ↁE`sha256:<64 hex>`�E�を生�E・検証するヘルパ�Eを実裁E��E
- Address `lineage.runtime_sha` から引用可能な実裁E��イジェストとして斁E��化（�EAddressに強制せず、null許可は維持E��、E
- CLI `--runtime-manifest` フラグを追加�E�他standaloneモードと相互排他、exit 0�E�、E
- `fixtures/runtime_manifest.json` および再生成ツール `tools/regenerate_runtime_manifest.py` を追加、`tools/regenerate_all_frozen_docs.py` へ統合、E
- `conformance.py`: `CHECK_IDS_ALLOWED` および `CHECK_STATUSES_ALLOWED` 閉集吁Erozensetを単一正本としてexportし、テスト�Eハ�Eドコードと統合、E
- CIワークフローへ `--runtime-manifest` 実行を追加、E


## 2026-09-06 (Address evidence_contract status closed enum)

- `evidence_contract.ASSESS_STATUS_ALLOWED` = {INSUFFICIENT, INVALID, CONFLICT, CONTRACTED} を単一正本�E�Essess emitters�E�。`_result` ぁEstatus も軽釁Eassert、E
- `evidence_contract.AUDIT_STATUS_ALLOWED` = {AUDITED, UNMET} を単一正本�E�Essess_audited_independence emitters�E�。`_audit_result` ぁEstatus も軽釁Eassert�E�Endependence とは別フィールド）、E
- unittest�E��E status emitters が閉雁E��冁E��assess status は AUDITED/UNMET を含めなぁE��両雁E��は disjoint。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address independence verdict closed enum single-source)

- `evidence_contract.INDEPENDENCE_ASSESS_ALLOWED` = {COMMON_CAUSE_SUSPECT, CONTRACTED, UNVERIFIED} を単一正本�E�Essess emitters�E�。`_result` が軽釁Eassert。決して INDEPENDENT / AUDITED を含まなぁE��E
- `evidence_contract.INDEPENDENCE_AUDIT_ALLOWED` = {AUDITED, UNMET} を単一正本�E�Essess_audited_independence emitters�E�。`_audit_result` が軽釁Eassert、E
- response_contract / resolution_gate は independence を�E開フィールドとして検証しなぁE��Export + emitter tests のみ�E�。unittest�E�emitters が閉雁E��冁E��assess は INDEPENDENT なし。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Cortext9 Reception runtime v0)
- Reception�E�E35単位�E実裁E��ポジトリを作�E・初回実裁E https://github.com/qooyanz-bot/cortext9-reception (`3fec520`)
- カタログ v0.4 全535登録、`/v0/invoke`・`/v0/reception/chat`、Gate0、優先ハンドラ43�E�E18/N03/N06/N12系ほか）。残りはスタブ、E
- Tiny runtime�E�Eogical_id線）とは別リポ�E別契紁E��Eoncept確定�E統一プロンプト改訂�Eなし、E

## 2026-09-06 (Address REASON_ALLOWED single-source)

- `resolution_gate.REASON_ALLOWED` = {ADDRESS_INVALID, AUDITED_INDEPENDENCE, CONTRACTED_EVIDENCE, CONTRADICTION, EVIDENCE_REJECTED, EVIDENCE_STALE, EVIDENCE_TIME_INVALID, FRESHNESS_REQUIREMENT_INVALID, SEMANTIC_INDEPENDENCE_UNMET} を単一正本�E�Eesolve emitters�E�。`_result` が軽釁Eassert、E
- `response_contract.REASONS` は同一 frozenset エイリアス�E�`validate` ぁE`resolution.reason` を検査、E
- unittest�E�未知 reason は contract 拒否�E��E朁Eidentity�E�Eis`�E�；happy path / golden 通過。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address DECISIONS + REPLAY_STATUSES single-source)

- `resolution_gate.DECISION_ALLOWED` = {ABSTAIN, READY_FOR_VERIFICATION} を単一正本�E�Eesolve emitters�E�。`_result` が軽釁Eassert、E
- `replay_verifier.REPLAY_STATUS_ALLOWED` = {REPLAY_VERIFIED, REPLAY_MISMATCH, LINEAGE_MISMATCH, INVALID_AUDIT} を単一正本�E�Eerify_replay emitters�E�。`_status_result` が軽釁Eassert、E
- `response_contract.DECISIONS` / `REPLAY_STATUSES` は同一 frozenset エイリアス�E�ローカル set 廁E���E�、E
- unittest�E�未知 decision/replay status は contract 拒否�E��E朁Eidentity�E�Eis`�E�；happy path 通過。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address claim_status closed enum)

- `protocol_claim_gate.CLAIM_STATUS_ALLOWED` = {ALLOWED_AS_DESIGN, ALLOWED_AS_RESULT, BLOCKED} を単一正本�E�Essess_claim status emitters�E�、E
- `decision_log.verify` ぁEclaim_status�E�非 null�E�閉雁E��を強制。`response_contract.PROTOCOL_CLAIM_STATUSES` は同一 frozenset エイリアス�E�Erotocol_claim / decision_log 双方�E�、E
- unittest�E�未知 status は verify 失敗；�E有定数�E�happy path / R6-G frozen fixture 通過。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address claim_reason closed enum)

- `protocol_claim_gate.CLAIM_REASON_ALLOWED` = {NO_RESULT_CLAIM, EVIDENCE_GATES_UNMET, MANIFEST_INVALID, CLAIM_TYPE_UNKNOWN, CAPABILITY_EVIDENCE_NOT_RESULT_BACKED, RECORDED_EVIDENCE_GATES_PASS} を単一正本�E�Essess_claim が実際に emit する全 reason�E�、E
- `decision_log.verify` ぁEclaim_reason�E�非 null�E�閉雁E��を強制。非 dict assessment の fallback は `ASSESSMENT_INVALID` をやめE`MANIFEST_INVALID`�E�Eate reason のみ�E�、E
- Response Contract は既存どおり `decision_log.verify` 経由で同一検査。unittest�E�未知 reason は verify/contract 失敗；happy path / R6-G frozen fixture は通過。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address claim_type closed enum)

- `protocol_claim_gate.CLAIM_TYPE_ALLOWED` = {DESIGN_DESCRIPTION, EXPERIMENT_RESULT, CAPABILITY_CLAIM} を単一正本�E�`assess_claim` が未知めEBLOCKED / CLAIM_TYPE_UNKNOWN、E
- `decision_log.verify` ぁEclaim_type 閉集合を強制�E�空・UNKNOWN 拒否�E�、ELI は `--protocol-manifest` に `--claim-type` 忁E��、未知は INVALID_INPUT、E
- unittest�E�verify 拒否、CLI 拒否、�E有定数。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address regenerator --check + CI drift)

- `tools/regenerate_limitations.py` / `regenerate_conformance_report.py` / `regenerate_all_frozen_docs.py` に `--check`�E�dry-run�E�on-disk fixture が生成�E容と一致すれば exit 0、書き換えが忁E��なら非0�E�書込みなし）、E
- CI `.github/workflows/address-reference-runtime.yml` に `python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check` スチE��プを追加、E
- unittest�E�`--check` 成功�E�一致�E�と失敗！Eemp mutate / mismatch・書込みなし）。tools/README + package README 更新。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address regenerate_limitations + all_frozen_docs)

- `tools/regenerate_limitations.py`�E�`limitations()` から `fixtures/limitations.json` を決定的に再生成。`tools/regenerate_all_frozen_docs.py` で limitations + conformance 一括再生成。unittest ぁEfixture 一致と regenerator 安定性を検査、E
- tools/README 追加。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address regenerate_conformance_report helper)

- `tools/regenerate_conformance_report.py`�E�`run_conformance()` から `fixtures/conformance_report.json` を決定的に再生成（手編雁E��要E��。unittest の fixture 一致検査と対、E
- README に実行例を追記。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address conformance report fixture + CI)

- `fixtures/conformance_report.json` めE`limitations.json` と同様に凍結！Erun_conformance()` の決定的出力；タイムスタンプなし）。unittest ぁEfixture と live `run_conformance()` の完�E一致を検査、E
- CI `.github/workflows/address-reference-runtime.yml` に `python address/reference-runtime-v0.1/address_cli.py --conformance` スチE��プを追加�E�Enittest の後；green main で exit 0�E�、E
- README 更新。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address conformance runner)

- `conformance.py` / `run_conformance() -> dict`�E�機械可読適合レポ�Eト！Eschema_version=address-conformance-v1`、`checks: [{id, status, detail}]`、overall=`CONFORMANT`|`FAIL`�E�、E
- 雁E��E LIMITATIONS 斁E���E�Etatus=`LIMITATIONS`、PASS 再解釈なし）；synthetic validate VALID + evaluate READY value=null + shared-law ABSTAIN value=null�E�R6-G frozen manifest MANIFEST_VALID�E�EXPERIMENT_RESULT は NOT_RUN|BLOCKED�E�実行済み主張なし）、E
- CLI `--conformance`�E�仁Estandalone / resolve と相互排他）。exit 0=CONFORMANT、FAIL があれ�E靁E、E
- unittest�E�report shape、synthetic VALID/READY value=null、R6-G 未実行、flag hygiene。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address CLI --validate-protocol-manifest)

- CLI `--validate-protocol-manifest MANIFEST.json` を追加�E�`protocol_claim_gate.validate_manifest` のみ実行。�E功時 exit 0 + `{status: MANIFEST_VALID, errors: []}`�E�失敗時靁E + `{status: MANIFEST_INVALID, errors: [...]}`�E�ENVALID_INPUT / CONTRACT 系と同形�E�、E
- resolve / `--limitations` / `--check-contract-only` / `--verify-decision-log` と相互排他（既孁Estandalone hygiene�E�、E
- unittest�E�R6-G frozen fixture VALID�E�未知 enum INVALID�E�flag combo 拒否。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address decision_log closed-enum mirror)

- `protocol_claim_gate` の閉集吁Efrozenset�E�ESTATE_ENUMS` / `EVIDENCE_STATE_ALLOWED` 筁E/ `AUDITOR_HANDOFF_*`�E�を単一正本として export�E�`decision_log.verify` が状態フィールド（非 null�E�と `auditor_handoff.decision`�E�非 null ↁEPENDING|PASS�E�およ�E handoff キー厳寁E��合を同じ雁E��で検査、E
- Response Contract は decision_log 存在時に `decision_log.verify` 経由で同一 enum 検査�E�単一路�E�；handoff キー定数は `AUDITOR_HANDOFF_KEYS` を�E有、E
- unittest�E�`evidence_state="EXECUTED"` 改ざんは verify/contract 失敗；R6-G frozen fixture / valid manifest の build_decision_log は通過。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address protocol manifest closed-enum validation)

- `protocol_claim_gate.validate_manifest(manifest) -> list[str]`�E�manifest 状態フィールド�E閉集吁Eenum を機械検査�E�例外なし）。evidence_state / implementation_state / experiment_state / independent_replay_state�E�protocol_id 非空斁E���E�E�auditor_handoff があるときキーは厳寁E�� {decision, primary_run_authorized}、decision=`PENDING|PASS`�E�EAIL は fixtures/tests 未出現のため未採用�E�、primary_run_authorized=bool|null、E
- `assess_claim` は先に validate�E�errors 時�E全 claim_type�E�EESIGN_DESCRIPTION 含む�E�で BLOCKED / MANIFEST_INVALID / unmet=errors。未知 enum は design すり抜け不可、E
- R6-G FROZEN と既存通過 manifest は green。unittest�E�未知 evidence_state / typo experiment_state / 余�E handoff キー / 空 protocol_id / DESIGN の無効 enum。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address residual defense in depth)

- Resolution Gate: `target_value.residual` から `resolution.residual` へミラーするとき、E��空斁E���Eラベルのみ emit�E�空斁E���E非文字�Eは例外停止せずスキチE�E�E�、E
- Response Contract: `resolution.residual` は非空斁E���Eの list�E�空斁E���E非文字�Eを拒否�E�；既存�E residual+value=null 規則は維持、E
- unittest: 不正 residual 要素の contract 拒否�E�Gate のスキチE�E�E�READY/ABSTAIN happy path は通過。新要Egolden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address synthetic-only validate enforcement)

- `address_runtime.validate` ぁELIMITATIONS `world_scope=SYNTHETIC_ONLY` を強制: `world:real:*` は明確な errors で INVALID�E�`world:synthetic-<non-empty>` のみ受理�E�空 suffix 拒否�E�、E
- `target_value.residual` ぁElist のとき要素は非空斁E���E�E�機械可読�E�、E
- `REAL_CAPABILITIES` はスキーマ文書用に残置�E�real-world capability subset 検査は削除�E�Eeal world は validate で先に失敗）。unittest / README / LIMITATIONS を整合。新要Egolden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address check-contract-only decision_log response)

- 公開応筁Egolden `fixtures/golden_contract_decision_log_blocked_response.json` を追加�E�Evaluate(..., protocol_manifest=R6-G, claim_type=EXPERIMENT_RESULT): READY / CONTRACTED_EVIDENCE + protocol_claim BLOCKED + frozen decision_log�E�value=null throughout�E�。regenerator には未配線！Eolden 増殖を抑制�E�、E
- `--check-contract-only` ぁEdecision_log 付き応答を通過�E�改ざん decision_log_id / 非null decision_log.value で CONTRACT_INVALID、E
- CLI `--verify-decision-log DECISION_LOG.json` を追加�E�Eecision_log.verify のみ�E�`--limitations` / `--check-contract-only` / resolve と相互排他）、E
- Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address content-addressed decision_log_id)

- `decision_log.build_decision_log` / `create` ぁE`decision_log_id` = `decision_log:` + sha256�E�Eaudit_log.content_digest` と同じ canonical dumps�E�を id 除夁Epayload から付与。`verify()` で忁E��Eshape と自己アドレス整合を検査、E
- Response Contract は decision_log 存在時に `decision_log_id` 忁E��＋`decision_log.verify` を要求（改ざん・欠落を拒否�E�、E
- 凍絁Efixture `r6g_frozen_decision_log_blocked.json` を�E生�E�E�正しい decision_log_id�E�。unittest�E�同一入力で id 安定�E改ざん検�E・contract が有効 id を要求。新要Eevaluate golden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address decision_log claim_reason / unmet align)

- Response Contract�E�`decision_log` と `protocol_claim` が両方あるとき、`claim_reason` めE`protocol_claim.reason`�E�Eeason がある場合）と一致要求；`unmet` は null 又�E斁E���E list�E�`protocol_claim.unmet` があるとき�E sorted 等価�E�Eultiset�E�で一致要求、E
- `decision_log.py` は `unmet` を常に list�E�空可�E�で出力（機械可読�E�。R6-G 凍絁EBLOCKED fixture は list のまま変更なし。新要ECLI evaluate golden なし、E
- unittest�E�reason mismatch / unmet non-list / unmet mismatch�E�happy path は R6-G frozen BLOCKED log で通過。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address decision_log Response Contract shape)
- Response Contract ぁE`decision_log` 存在時に機械可読 shape を強制�E�忁E��キー�E�Echema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff / value / 状慁Eフィールド）、schema_version=`decision_log.SCHEMA_VERSION`、value=null、既知 claim_status、protocol_claim.status 非矛盾、auditor_handoff は厳寁E�� {decision, primary_run_authorized}、E
- unittest で missing schema_version / wrong handoff keys / non-null value / status mismatch を固定。新要Egolden なし。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address Protocol Claim Decision Log / auditor-handoff)
- `decision_log.py` を追加。manifest + claim_type + `assess_claim` 結果から value-free な Decision Log�E�Echema_version / protocol_id / claim_type / claim_status / claim_reason / unmet / auditor_handoff の decision・primary_run_authorized のみ / 状態フィールチE/ value=null�E�を構築、E
- R6-G SPEC_ONLY + EXPERIMENT_RESULT ↁEBLOCKED めE`fixtures/r6g_frozen_decision_log_blocked.json` で凍結、ELI は既孁E`--protocol-manifest` / `--claim-type` 経路で `decision_log` めEevaluate 応答に付与、E
- Response Contract は decision_log があるとぁEvalue=null・既知 claim_status・protocol_claim.status 非矛盾を要求、EIMITATIONS に `protocol_result_claims=GATED`。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address AUDITED_INDEPENDENCE READY golden)
- 公開応筁EREADY golden `fixtures/golden_contract_audited_independence_response.json` を追加�E�Eddress `semantic_independence=AUDITED` + CONTRACTED証拠 + 有効typed `independence_audit`�E�E{evidence_id, digest}` が束と一致�E��E READY_FOR_VERIFICATION / AUDITED_INDEPENDENCE / value=null・residualあり・audit整合）。SEMANTIC_INDEPENDENCE_UNMET goldenの成功対称、E
- `tools/regenerate_contract_goldens.py` / match-evaluate / `--check-contract-only` 専用unittestに配線。value允E��・入れ孁E`lineage.result_sha`・reason非AUDITED_INDEPENDENCEで失敗する回帰を凍結、E
- Value発見�ER6-G実行�E静かな昁E��ショートカチE��は行わなぁE��E

## 2026-09-06 (Address typed independence_audit evidence_digests)
- `independence_audit.evidence_digests` を常に `{evidence_id, digest}` オブジェクト�Eに固定！Eaudit_log.evidence_digest_entries` と同形�E�。裸の digest 斁E���Eは凍結チェチE��リストで `UNMET`、E
- evidence 供給時�E evidence_id+digest 対ぁEcontent-addressed 束と完�E一致。id また�E digest の不一致 ↁE`SEMANTIC_INDEPENDENCE_UNMET`�E�正しいオブジェクト�E ↁE`READY_FOR_VERIFICATION` / `value=null`、E
- `assess()` 単体�E引き続き決して AUDITED を返さなぁE��Value発見�ER6-G実行�E静かな AUDITED 昁E��は行わなぁE��E

## 2026-09-06 (Address independence_audit evidence_digests binding)
- `assess_audited_independence(audit_record, evidence=...)` ぁE`evidence_digests` を供給エビデンス束�E content-addressed digest�E�Eaudit_log.content_digest` / `evidence_digest_entries` と同一アルゴリズム�E�と完�E一致要求。別束への PASS 監査では AUDITED にならなぁE��E
- Resolution Gate は AUDITED 要求時に evidence を監査検査へ渡す。不一致 ↁE`ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`�E�一致�E�チェチE��リスト通過 ↁE`READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` / `value=null`、E
- `assess()` 単体�E引き続き決して AUDITED を返さなぁE��Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address AUDITED path requires external independence_audit)
- Evidence Contract に凍結チェチE��リスト！Eauditor_id` / `decision=PASS` / `method` / `evidence_digests` / `audited_at`�E�と `assess_audited_independence()` を追加。通過時�Eみ `independence=AUDITED`�E�`assess()` は引き続き決して AUDITED/INDEPENDENT を返さなぁE��Eath多様性・metadata刁E��だけでは昁E��しなぁE��、E
- Resolution Gate / `evaluate` / CLI `--independence-audit` を�E線、Eddress ぁE`semantic_independence=AUDITED` のとぁECONTRACTED証拠 **かつ** 有効監査記録が忁E��。欠落・不完�E・偽造 ↁE`ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`�E�有効 ↁE`READY_FOR_VERIFICATION` / `AUDITED_INDEPENDENCE` でめE`value=null`、E
- LIMITATIONS に `audited_independence=EXTERNAL_RECORD_REQUIRED` を追加。Value発見�ER6-G実行�E行わなぁE��E


## 2026-09-06 (Address remaining machine-checkable string-list types)
- `address_runtime.validate` に `goal.id`�E�非空斁E���E�E�、`goal.success_criteria` / `state_constraints` / `capability_scope`�E�非空斁E���Eの list�E�空要素・非文字�E拒否�E�を追加。`capability_scope` の forbid-token / real-world subset は維持、E
- `valid_synthetic_address.json` は VALID のまま�E�Eddress_id 非書換）。各拒否めEunittest で固定。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address machine-checkable field types / canonical serialization)
- `address_runtime.validate` に entities / relations / unknown / lineage sha / minimum_sources の機械可読型検査を追加。例外停止せず errors リストで拒否。valid_synthetic_address.json は VALID のまま、E
- `canonical_dumps` を�E示し、`canonical_id` ぁE`sort_keys=True` + `separators=(',', ':')` のみを使ぁE��とを文書化�Eunittest固定（キー頁E�E空白は address_id 不変）、E
- Open work「各フィールド�E機械可読型と正規直列化」への実裁E���E。Value発見�ER6-G実行�E行わなぁE��E

## 2026-09-06 (Address semantic_independence closed enum + UNMET golden)
- `address_runtime.validate` ぁE`evidence_requirements.semantic_independence` を閉雁E�� enum�E�EUNVERIFIED` | `CONTRACTED` | `AUDITED`�E�として強制。他値は例外停止せず明確な errors で拒否、E
- 公開応筁Egolden `fixtures/golden_contract_semantic_independence_unmet_response.json` を追加�E�Eddress `semantic_independence=AUDITED` + CONTRACTED証拠 ↁEABSTAIN / SEMANTIC_INDEPENDENCE_UNMET / value=null・residualあり・audit整合）。regenerator / match-evaluate に配線、E
- 無効 enum・AUDITED+CONTRACTED ABSTAIN・UNVERIFIED fixture READY の回帰をunittestで固定、E

## 2026-09-06 (Address evidence independence / common-cause verdict)
- Evidence Contract `assess()` に明示皁E�� `independence` 判定を追加: 共有authority/generator/semantic_law�E�又は重複identity�E��E `COMMON_CAUSE_SUSPECT`�E�EONFLICT�E�、metadata刁E��通過は `CONTRACTED`、不足・不正は `UNVERIFIED`。path IDだけでは `INDEPENDENT` / `AUDITED` を返さなぁE��E
- Resolution Gateは READY_FOR_VERIFICATION めE`independence=CONTRACTED` のとき�Eみ許可、EddressぁE`semantic_independence: AUDITED` なのに証拠がCONTRACTED止まり�E場合�E `ABSTAIN` / `SEMANTIC_INDEPENDENCE_UNMET`。`UNVERIFIED` 要求！Ealid_synthetic_address.json�E��E従来どおりCONTRACTEDでREADY。value=null維持、E

## 2026-09-06 (Address LIMITATIONS / synthetic-only conformance)
- `limitations.py` と `fixtures/limitations.json` を追加。world_scope=SYNTHETIC_ONLY、value_discovery=NOT_IMPLEMENTED、r6g_experiment=NOT_RUN�E�EPEC_ONLY�E�、real_domain_extrapolation / secret_access / crypto_bypass / future_direct=FORBIDDEN を機械可読に宣言、ELI `--limitations` でJSON出力！Exit 0�E�。resolve / `--check-contract-only` と相互排他。R6-G実行�EValue発見�E現実外挿は主張しなぁE��E

## 2026-09-06 (Address contract-only EVIDENCE_STALE golden)
- 公開応答EVIDENCE_STALE golden `fixtures/golden_contract_stale_response.json` を追加�E�Ebserved_atが`--now`とfreshness max_ageに対して古ぁE��evaluate出劁E ABSTAIN / EVIDENCE_STALE / value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value允E��・入れ孁E`lineage.result_sha`・reason非EVIDENCE_STALEで失敗する回帰をREADY/ABSTAIN/CONTRADICTIONと対称に凍結、E
- `tools/regenerate_contract_goldens.py` と match-evaluate unittest に EVIDENCE_STALE を追加、E

## 2026-09-06 (Address contract-only CONTRADICTION golden + regenerator)
- 公開応答CONTRADICTION golden `fixtures/golden_contract_contradiction_response.json` を追加�E�同一assertion_keyで衝突するassertion_valueの実evaluate出劁E ABSTAIN / CONTRADICTION / value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value允E��・入れ孁E`lineage.result_sha`・reason非CONTRADICTIONで失敗する回帰をREADY/ABSTAINと対称に凍結、E
- `tools/regenerate_contract_goldens.py` でREADY/ABSTAIN/CONTRADICTION goldenをevaluate()から再生成可能に。unittestがfixtureとfresh evaluate()の完�E一致を検査する、E

## 2026-09-06 (Address contract-only ABSTAIN golden)
- 公開応答ABSTAIN golden `fixtures/golden_contract_abstain_response.json` を追加�E�Ehared-law EVIDENCE_REJECTED の実evaluate出劁E value=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value允E��・入れ孁E`lineage.result_sha`・decision非ABSTAINで失敗する回帰をREADY goldenと対称に凍結、E

## 2026-09-06 (Address contract-only golden fixture + argparse harden)
- 公開応答golden fixture `fixtures/golden_contract_ok_response.json` を追加�E�Ealue=null・residualあり・audit整合）。`--check-contract-only` / validate で通過し、value允E��めE�Eれ孁E`lineage.result_sha` 刻印で失敗する回帰を凍結、E
- `--check-contract-only` と address/evidence/`--now`/resolve系フラグの併用を早朁E`INVALID_INPUT` JSON で拒否、E

## 2026-09-06 (Address assertion/residual collision + contract-only CLI)
- Evidence `assertion_key` ぁEunknown.slot / residual ラベルと衝突してめEresidual を解消せず、`assertion_value` めEvalue に束縛しなぁE��EEADYでめEvalue=null�E�、E
- Address CLI に `--check-contract-only RESPONSE.json` を追加、Eate再実行なしで公開応答�E response_contract を検証�E�EK=0、E��反�E機械可読 errors で靁E�E�、E

## 2026-09-06 (Audit Log malformed-input hardening)
- Audit Logのevidence digest頁E��がobjectでなぁE��合も、例外停止せず明示皁E��拒否するよう修正、E

## 2026-09-06 (Address memory and lineage boundaries)
- Memory scopeにauthorized/versioned/revocableを忁E��化し、Lineageの入力参照をSHA-256形式に限定。未許可・追跡不�EなMemory�E��E力参照を拒否する、E

## 2026-09-06 (Address response contract)
- CLI出力�EResponse Contractを追加。Value非返却、既知の判定状態、Auditとの判断一致を検証し、封E��の出力回帰を防ぐ、E

## 2026-09-06 (Address reference runtime CI)
- `address/reference-runtime-v0.1/` の変更時に全unittestを実行する最小GitHub Actions CIを追加。外部チE�Eタ、秘寁E��実世界Valueの取得�E行わなぁE��E

## 2026-09-06 (Historical Raw Archive documentation)
- READMEに `archives/md-original/` の目皁E��利用上�E正本性区刁E��安�Eな参�E手頁E��追加、E
- Raw Archiveを承認済み判断・再現可能なEvidence・未検証仮説と混同しなぁE��と、秘寁E��報の再記録・復允E��しなぁE��とを�E記、E

## 2026-09-06 (Address reference runtime v0.1)
- read-only Address CLIを追加、Eddress JSONとEvidence JSONを一括評価し、Resolution、value-free Audit Log、任意�EReplay検証を返す。Value導�E・外部接続�Eファイル書込みは行わなぁE��E
- Protocol Claim Gateを追加。R6-Gの直接確認済みmanifest状態を対象に、`NOT_RUN`・監査未完亁E�E未実裁E��ら実験結果�E��E力主張へ飛躍することをブロチE��する、E
- Address Runtimeの型�E時間・scope墁E��を強化。malformed inputを例外停止せず `INVALID` として返し、時間送E��、真偽値threshold、E��JSON値などを拒否する、E
- Replay Verifierを追加。保存された監査ログを�E己ハッシュだけでなく、同一Address・Evidence・時刻でGateを�E実行して検証する。�E力、系譜、判断の不一致を検�Eする、E
- content-addressed Audit Logを追加。値とassertion本斁E��記録せず、Address ID、証拠digest、判定、時刻から再計算可能な監査IDを生成�E検証する、E
- Resolution Gateを追加、Eddress・Evidence Contract・鮮度・assertion矛盾を統合し、失敗時はすべて `ABSTAIN` と `value=null` を返す、E
- Evidence Contract evaluatorを追加。authority、generator、semantic lawの共有を検�Eし、別pathでも独立性とは認定しなぁE��metadata刁E��を通過してめE`CONTRACTED` とし、semantic independenceの監査済み主張はしなぁE��E
- Addressable Concept Architecture v0.1 の最小安�E不変条件を検査する依存なし�E参�E実裁E��fixture、unittestめE`address/reference-runtime-v0.1/` に追加。秘寁E�E認証回避・直接未来取得を含むscope、hash不整合、abstain不備を拒否する、E

## 2026-09-06 (Addressable Concept Architecture v0.1)
- K承認により、検証可能なAddress SchemaとEvidence墁E��めE`address/addressable-concept-architecture-v0.1.md` に追加。R6-G未実行、既存結果のsynthetic限定性、Law不確実時のabstain要件を�E記、E

## 2026-09-06 (ChatGPT export archive)
- 380会話・17,957メチE��ージの公開用会話アーカイブを `archives/2026-09-06/` に追加。秘寁E��式�Eメール・電話番号を不可送E��置換し、原本HTML・添付本体�EセチE��ョンIDは含めなぁE���E析�E草案であり、会話冁E��を正本の決定として自動採用しなぁE��E
- 同じ会話めE`archives/md-original/` に日付頁E�E1会話1Markdownとして追加。会話冁E��由来の題名とし、�E開安�Eの伏せ字以外�E本斁E��保�Eする、E

## 2026-09-05 (Cortext9 units v0.4)
- 圧勝単位をさらに細刁E��。v0.3の359から拡張�E�薄ぁE���E系ドメインの子＋N151–N212�E�。カタログ `future-concept/Cortext9-unit-catalog-v0.4.json`、追訁E`future-concept/Cortext9-unit-api-schema-v0.4-addendum.md`。断定�E医療�E法律�E軍事�E引き続き禁止、E

## 2026-09-05 (Cortext9 units v0.3)
- 圧勝単位をさらに細刁E��。v0.2の218から拡張�E�E51–N90の子＋N91–N150系、writing/life_safe/ml_ops運用単位）。カタログ `future-concept/Cortext9-unit-catalog-v0.3.json`、追訁E`future-concept/Cortext9-unit-api-schema-v0.3-addendum.md`。断定�E医療�E法律�E軍事�E引き続き禁止、E

## 2026-09-05 (Cortext9 units v0.2)
- 圧勝単位をさらに細刁E��。v0.1の102から拡張�E�E19–N50の子ID�E�N51–N90系�E�。カタログ `future-concept/Cortext9-unit-catalog-v0.2.json`、追訁E`future-concept/Cortext9-unit-api-schema-v0.2-addendum.md`。ml_ops�E�振り�Eけ�E評価・拒否ゴールチE���E�追加。断定�E医療�E法律�E軍事�E引き続き禁止、E

## 2026-09-05
- Cortext9 圧勝単位を細刁E���E�E01–N18 の子ID�E�N19–N50�E�。カタログ `future-concept/Cortext9-unit-catalog-v0.1.json`、追記スキーチE`future-concept/Cortext9-unit-api-schema-v0.1-addendum.md`。非断定�E安�E単佁EN43–N46 を追加。断定�E医療�E法律�E軍事�E引き続き禁止、E
