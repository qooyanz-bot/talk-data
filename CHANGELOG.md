# Changelog

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
