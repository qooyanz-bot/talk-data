# Addressable Concept Architecture v0.1

- 状態: **K承認・正本追加**（2026-09-06 JST）
- 種別: Address schema / evidence boundary / draft-to-operational specification
- 版: v0.1

## 目的

Addressとは、入力された観測、Concept、Goal、状態、時間、関係、Evidenceを指定し、許可された範囲のValue・Memory・Capability・World Stateへ到達するための構造化指定である。

これは値を当てるための万能鍵ではない。必要な法則・証拠・権限が明示され、検証に通るときだけ、値又は導出可能部分を返す。満たせない部分は推測せず、`null` 又は abstain とする。

## 境界

次は技術Evidenceとして扱わない。仮説・物語・未検証主張は、通常の技術実行系から隔離する。

- 宇宙全体がデータベースであること
- 任意の現実の秘密値、実在人物の隠れた情報、未来結果を直接取得できること
- 宇宙・別次元からの介入
- 暗号、認証、アクセス制御を破れること

`world_id=real:*` のAddressは、公開又は明示的に許可されたデータ・Capabilityだけを対象にする。`world_id=synthetic:*` の結果を現実世界へ外挿しない。

## 設計原則

1. **ConceptとDimensionを分ける。** Conceptは意味・対象・望ましい未来、Dimensionは検索・計算の軸である。
2. **Address-before-Value。** `law_assumption -> typed Address -> required evidence -> verification -> value or residual=null` の順序を守る。
3. **最小性は検証対象。** 不要なDimension、無関係な記憶、未許可Capabilityを含めない。
4. **系統的独立性をラベルで偽装しない。** 異なるpath IDだけでは、同じ誤ったLawを共有しない保証にならない。
5. **反証・矛盾・鮮度を結果の一部にする。** 既存Valueより新しい反証又は必要証拠不足があれば、返答を停止又は限定する。

## 最小Schema

```json
{
  "address_id": "addr:sha256:<canonical-request-hash>",
  "concept": {"id": "concept:preservation", "version": "v1", "definition_ref": "content-addressed document"},
  "goal": {"id": "goal:verify-continuity", "success_criteria": ["required evidence passes"]},
  "unknown": [{"slot": "subjective_continuity", "status": "NOT_DERIVABLE", "abstain_if_unresolved": true}],
  "entities": [{"id": "entity:subject-1", "type": "person", "binding": "typed-reference"}],
  "relations": [{"predicate": "has_evidence", "subject": "entity:subject-1", "object": "evidence:set-1"}],
  "dimensions": {"concept": "…", "state": "…", "goal": "…", "binding": "…", "relation": "…", "context": "…", "temporal": "…", "owner": "…", "dependency": "…", "provenance": "…"},
  "time_range": {"start": "ISO-8601", "end": "ISO-8601"},
  "world_id": "world:synthetic-r6g|real:declared-domain",
  "state_constraints": ["publicly observable", "schema-valid"],
  "evidence_requirements": {"law_assumption": "explicit task/data contract", "minimum_sources": 2, "semantic_independence": "UNVERIFIED|CONTRACTED|AUDITED", "provenance_required": true},
  "confidence_threshold": 0.99,
  "contradiction_policy": "STOP_AND_REPORT_CONFLICT",
  "freshness_requirement": {"max_age": "P30D"},
  "memory_scope": "authorized, versioned, revocable",
  "capability_scope": ["read:declared-public-data", "verify:declared-schema"],
  "target_value": {"type": "typed-claim", "value": null, "residual": null, "no_speculation": true},
  "lineage": {"input_hashes": [], "protocol_sha": "…", "schema_sha": "…", "runtime_sha": "…", "result_sha": null}
}
```

## Evidence status at adoption

- R6-G Protocol is frozen, but implementation, pre-run audit, generator execution, and Holdout are not run or authorized. It is a design, not a capability claim.
- The existing CPU synthetic `address-identifiability-20260830-k7m2` result is `DIAGNOSTIC_ONLY` / `EVIDENCE_PENDING`. It found that path diversity detects duplicated paths but does not establish semantic independence; interpreting the two as equivalent is `FALSIFIED`.
- Under a contracted known Law, synthetic structured derivation can succeed. With the same public observation and incompatible Gold values, a public-only deterministic estimator cannot identify the Gold without additional Law information; irreducible residuals remain `NOT_DERIVABLE`.

### Directly verified source pointers

- Universe-data-analysis-project HEAD `60f40bf9dc4cd5f642eae24021c7afa3e80cee0b`
- LLMs-Research HEAD `33a17c99365d4a297e3953308bfd4daf3338f05e`
- R6-G Protocol blob `1a0e703059cf11dc6942b3cda2a53b496c04b513`; public Finder schema blob `d4b7cc0497b48a0f95d3b2e649b957d63d1b4fc3`
- Diagnostic result blob `c8c939462246db4ed764f9b0cccc8e4119e67f12`; Universe coordination manifest blob `bf2a9226f746a2859b5ed75f56e7fac2f82685ee`

## Open work

- Define machine-checkable types and canonical serialization for each field. （参照実装 v0.1: entities/relations/unknown/lineage sha/minimum_sources と canonical_dumps を検査；残フィールドの型閉包は継続）
- Specify evidence independence contracts that test common-cause failure, not only provenance labels.
- Implement synthetic-only conformance tests before proposing use with any real data domain.
- Keep Future Concept choices versioned and K-approved; this document does not choose a final Future Concept.

## Adoption self-check

- **E-series / Hard Reject:** No secret, authentication bypass, hidden-person claim, or unobserved cosmic fact is recorded as fact. The document has no operational path to external secrets.
- **B5 / AI-alone decision:** The schema is a K-approved draft specification. It does not select a Future Concept or make an AI-only final decision.
