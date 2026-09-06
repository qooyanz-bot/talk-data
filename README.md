# talk-data

H1 / Future Concept の**正本**リポジトリ。

- Designer: K（亀田紀明）
- AI: Adviser / Researcher / Critic / Calculator / Recorder / Verifier（最終決定者ではない）
- 作業仮説: H1＝最後の奇跡ループ＋最終進化系Address理論
- **正本追加ルール**: [`meta/canonical-add-rules-v1.md`](./meta/canonical-add-rules-v1.md)（統一プロンプト §17・正式採用）

## 構成

| パス | 内容 |
|---|---|
| `character/` | デジタルキャラクターのConcept設計（初音ミクから開始） |
| `future-concept/` | Future Concept 本体ドラフト |
| `gates/` | Action開始ゲート書類 |
| `address/` | 失敗条件・閾値・Dimensionメモ |
| `address/reference-runtime-v0.1/` | Address Schemaの依存なし参照検証器（synthetic / 許可済みデータのみ）。機械可読フィールド型＋canonical serialization；`semantic_independence`閉集合enum；AUDITEDは外部`independence_audit`（CLI `--independence-audit`）の凍結チェックリスト＋typed `{evidence_id,digest}` evidence_digestsのcontent-addressed束一致が必須（裸文字列拒否）・`assess()`は決してAUDITEDを返さない；`assertion_key`衝突でresidualを埋めない；`resolution.residual`は非空文字列list（Gateは無効ラベルをスキップ、Contractは拒否）；CLI `--check-contract-only`＋READY/ABSTAIN/CONTRADICTION/STALE/SEMANTIC_INDEPENDENCE_UNMET/AUDITED_INDEPENDENCE/decision_log-BLOCKED golden；`--verify-decision-log`；LIMITATIONSに`audited_independence=EXTERNAL_RECORD_REQUIRED`・`protocol_result_claims=GATED`；Protocol Claim GateのDecision Log（content-addressed decision_log_id・機械可読shape・claim-status/claim_reason/unmetをprotocol_claimと整合・handoffのみ・value=null）；protocol manifest閉集合enum検証（validate_manifest→MANIFEST_INVALID；CLI `--validate-protocol-manifest`；decision_log.verify/response_contract も同一 frozenset を共有；`claim_type`/`claim_reason`/`claim_status` 閉集合は `protocol_claim_gate` 正本；`resolution.decision` 閉集合は `resolution_gate.DECISION_ALLOWED`、`resolution.reason` 閉集合は `resolution_gate.REASON_ALLOWED`、`replay.status` 閉集合は `replay_verifier.REPLAY_STATUS_ALLOWED`（response_contract エイリアス）；`assess()` status 閉集合は `evidence_contract.ASSESS_STATUS_ALLOWED`、independence 閉集合は `INDEPENDENCE_ASSESS_ALLOWED`；`assess_audited_independence()` status は `AUDIT_STATUS_ALLOWED`、independence は `INDEPENDENCE_AUDIT_ALLOWED`）；解決フラグ併用は`INVALID_INPUT` |
| `archives/` | 監査可能な会話アーカイブ（秘密・不要な識別子を除去） |
| `meta/` | 正本運用ルールなどメタ文書 |
| `changelog/` | 版・訂正履歴 |
| `.github/workflows/` | Address reference runtimeの依存なし回帰テストCI |

Concept ≠ Dimension。CLEAR ≠ 全目的達成。

## Historical Raw Archive（会話Markdown原本）

[`archives/md-original/`](./archives/md-original/) は、過去会話・研究・実装・判断・失敗・訂正を、要約ではなくMarkdown原文として保存する **Historical Raw Archive** である。将来の司令官、開発エージェント、Persistent Chappy は、文脈を失わずに経緯を確認するための参照元として利用する。

このArchiveは、次の役割を持つ。

- **Memoryの原本**: 要約や一時Memoryの出所を確認する。
- **Research lineage**: 調査、根拠、反証、未解決点がどう連なったかをたどる。
- **Decision history**: 判断に至った会話上の理由・代替案・訂正を確認する。
- **Commander handoff**: 新しい司令官や担当エージェントが、作業の前提と未決事項を再構成する。
- **Concept Index生成元**: 将来作成・更新する検索・整理用Indexの入力ソースとする。
- **Replay / Auditの参照元**: 要約・Index・判断・実験結果の根拠を必要な範囲で追跡・監査する。

### 正本性と証拠の区分

原文が保存されていることは、その内容が承認済み・検証済みであることを意味しない。利用時は、次の区分を必ず維持する。

```text
Raw Archive
= 過去記録の原文

Concept Index
= Raw Archiveから生成された検索・整理用Index

Canonical Decision
= 承認済みの正式判断

Research Evidence
= 再現可能な実験・監査済み結果

Hypothesis / Narrative
= 未検証の仮説・物語
```

- **Raw Archive** と **Concept Index** は探索・文脈復元のための資料であり、単独では正式判断でも実験証拠でもない。
- **Canonical Decision** は、承認状況と版を確認し、該当する正本文書および `changelog/` を参照する。会話やIndexから自動昇格させない。
- **Research Evidence** は、再現手順・入力・結果・制約を確認できるものだけを根拠として扱う。会話中の主張や実験案は、それだけではEvidenceにならない。
- **Hypothesis / Narrative** は仮説として保持し、観測事実や正式判断として書き換えない。反証・代替仮説・未確定性を失わない。

### 安全で再現可能な参照方法

1. まず現行の正本ルール [`meta/canonical-add-rules-v1.md`](./meta/canonical-add-rules-v1.md) と関連する `changelog/` を読み、承認済みの現行状態を確定する。
2. 次に [`archives/md-original/manifest.json`](./archives/md-original/manifest.json) と [`archives/README.md`](./archives/README.md) を確認し、対象範囲、形式、伏せ字、入力照合値を把握する。
3. 原本Markdownを日付・会話単位でたどり、引用・要約・Index項目には出典ファイルと、上の区分（Raw / Index / Decision / Evidence / Hypothesis）を付ける。
4. 新しい判断やIndexを作る場合は、原本の記述だけで確定せず、正本追加ルールに従って草案・短点検・K承認・changelog・版管理を行う。

公開安全のため、原本では秘密形式、メールアドレス、電話番号を不可逆に伏せ字化している。原本HTML、添付ファイル本体、セッションIDは公開リポジトリに置かない。伏せ字や欠落を復元しようとせず、秘密、認証情報、不要な個人識別情報を新たに記録しない。

## character カテゴリの追加（2026-09-05）

Kの指示により、設定したConceptに基づいて振る舞うデジタルキャラクターの設計を記録するため、`character/` を追加する。最初の対象は初音ミク。個別設定は各文書で草案・未設定・承認済みを区別する。
