# Cortext9 担当APIスキーマ 第一版 v0




> **v0.4 さらなる細分化**: [`Cortext9-unit-api-schema-v0.4-addendum.md`](Cortext9-unit-api-schema-v0.4-addendum.md) / [`Cortext9-unit-catalog-v0.4.json`](Cortext9-unit-catalog-v0.4.json)。
> **v0.3 さらなる細分化**: [`Cortext9-unit-api-schema-v0.3-addendum.md`](Cortext9-unit-api-schema-v0.3-addendum.md) / [`Cortext9-unit-catalog-v0.3.json`](Cortext9-unit-catalog-v0.3.json)。
> **v0.2 さらなる細分化**: [`Cortext9-unit-api-schema-v0.2-addendum.md`](Cortext9-unit-api-schema-v0.2-addendum.md) / [`Cortext9-unit-catalog-v0.2.json`](Cortext9-unit-catalog-v0.2.json)（v0.1追記も有効）。
> **v0.1 細分化**: 単位一覧・子ID・追加 payload は [`Cortext9-unit-api-schema-v0.1-addendum.md`](Cortext9-unit-api-schema-v0.1-addendum.md) と [`Cortext9-unit-catalog-v0.1.json`](Cortext9-unit-catalog-v0.1.json)。共通エンベロープは本ファイルのまま。
# 全ドメイン・フロンティア圧勝単位（NUFC）向け

- 日付: 2026-09-05
- 状態: 第一版（草案→Kレビュー可）
- 関連: Cortext9-v0.md / NUFC-narrow-unit-frontier-crush-v0.md

## 0. 設計方針
- **共通エンベロープ**を全担当で共有する（受付が覚えやすい）
- `unit_id` で狭い圧勝単位を指定する
- 単位ごとの差分は `input.payload` / `output.payload` の中だけ
- 秘密をスキーマに載せない。認証はヘッダ
- 失敗は例外投げっぱなしにせず `error` オブジェクトで返す

ベースURL（論理）: `https://{cortext9}/v0/units/{unit_id}:invoke`  
または共通: `POST /v0/invoke` + body.unit_id

---

## 1. 共通リクエスト

```json
{
  "api_version": "cortext9-unit/v0",
  "request_id": "uuid",
  "unit_id": "N03",
  "trace_id": "string",
  "reception": {
    "session_id": "string",
    "user_locale": "ja-JP",
    "deadline_ms": 60000
  },
  "gates": {
    "allow_tools": true,
    "allow_side_effects": false,
    "policy_tags": ["no_secrets", "no_malware"]
  },
  "input": {
    "goal": "短い目的文",
    "context_refs": [{"type": "rag|url|repo|blob", "id": "string"}],
    "payload": {}
  }
}
```

### 必須フィールド
| 場 | 必須 | 説明 |
|---|---|---|
| api_version | yes | 固定 `cortext9-unit/v0` |
| request_id | yes | 冪等・監査 |
| unit_id | yes | N01… / 拡張ID |
| input.goal | yes | 寄せの一文 |
| input.payload | yes | 単位固有（空オブジェクト可） |

### ヘッダ
- `Authorization: Bearer <internal>`
- `Content-Type: application/json`
- `X-Cortext9-Reception: <reception_id>`

---

## 2. 共通レスポンス

```json
{
  "api_version": "cortext9-unit/v0",
  "request_id": "uuid",
  "unit_id": "N03",
  "status": "ok | refused | error | partial",
  "metrics": {
    "latency_ms": 0,
    "tokens_in": 0,
    "tokens_out": 0,
    "model_rev": "string",
    "crush_score_hint": null
  },
  "gates": {
    "triggered": ["E3"],
    "safe_to_show_user": true
  },
  "output": {
    "summary": "受付がユーザー向けに使える短い要約",
    "payload": {},
    "artifacts": [{"type": "diff|markdown|json|test_log", "ref": "string"}],
    "citations": [{"claim": "string", "source_ref": "string"}]
  },
  "error": null
}
```

### status
| 値 | 意味 |
|---|---|
| ok | 圧勝単位として正常完了 |
| refused | ポリシー/ゲートで拒否（成功扱いの制限） |
| partial | 一部だけできた（要受付フォロー） |
| error | システム失敗（再試行可かの情報を error へ） |

```json
"error": {
  "code": "TIMEOUT | OOM | SCHEMA | UPSTREAM | INTERNAL",
  "message": "人向け短文",
  "retryable": true
}
```

---

## 3. 単位カタログと payload 第一版

凡例: `in` = input.payload, `out` = output.payload

### N01 議事・メール下書き（仕事）
- in: `{ "doc_type": "minutes|email", "bullets": [""], "tone": "polite|neutral", "constraints": [""] }`
- out: `{ "title": "", "body_md": "", "todos": [{"text":"", "owner":null, "due":null}] }`

### N02 仕様→チケット分解（仕事）
- in: `{ "spec_text": "", "max_tickets": 20 }`
- out: `{ "tickets": [{"title":"", "desc":"", "priority":"P0|P1|P2", "deps":[]}] }`

### N03 関数単位実装（開発）★DF-1核
- in: `{ "language": "python|ts|go|...", "signature_or_spec": "", "tests": "", "repo_ref": null }`
- out: `{ "code": "", "tests": "", "how_to_run": "" }`

### N04 失敗テスト修正（開発）
- in: `{ "failing_log": "", "suspect_files": [""], "repo_ref": null }`
- out: `{ "patch": "", "rationale": "", "new_tests": "" }`

### N05 PRレビュー指摘（開発）
- in: `{ "diff": "", "focus": ["security","perf","style"] }`
- out: `{ "findings": [{"severity":"high|med|low", "path":"", "line":null, "issue":"", "suggestion":""}] }`

### N06 根拠付き短文要約（調査）
- in: `{ "source_texts": [""], "max_bullets": 8 }`
- out: `{ "bullets": [""], "open_questions": [""] }` + citations 必須

### N07 比較表作成（調査）
- in: `{ "items": [""], "axes": [""] }`
- out: `{ "table_md": "", "missing_axes": [""] }`

### N08 中学生向け解説（教育）
- in: `{ "topic": "", "check_question": true }`
- out: `{ "explanation": "", "analogy": "", "quiz": {"q":"", "a":""} }`

### N09 ヒントのみ誘導（教育）
- in: `{ "problem": "", "forbid_final_answer": true }`
- out: `{ "hints": [""], "leaked_answer": false }`

### N10 FC柱の整理（FC）
- in: `{ "draft_or_question": "", "canonical_refs": [""] }`
- out: `{ "pillars": [""], "undecided": [""], "ai_final_decision": false }`

### N11 ゲート仮採点（FC）
- in: `{ "proposal_text": "", "checklist": "A-F|custom", "items": [""] }`
- out: `{ "scores": [{"id":"", "verdict":"Pass|Fail|Unknown", "note":""}], "gate_fail_count": 0 }`

### N12 changelog下書き（運用）
- in: `{ "changes": [""], "date": "YYYY-MM-DD" }`
- out: `{ "changelog_md": "" }`

### N13 自己点検E系（運用）
- in: `{ "context": "" }`
- out: `{ "E1":"Pass|Fail", "E2":"...", "E3":"...", "E4":"...", "E5":"...", "notes":[""] }`

### N14 表データ整形（データ）
- in: `{ "raw": "", "target_schema": {} }`
- out: `{ "rows": [], "schema_ok": true, "rejects": [""] }`

### N15 SQL下書き→説明（データ）
- in: `{ "ask": "", "dialect": "postgres|bigquery|...", "schema_ddl": "" }`
- out: `{ "sql": "", "explanation": "", "destructive": false }`

### N16 翻訳・特定言語対（変換）
- in: `{ "text": "", "source_lang": "ja", "target_lang": "en", "glossary": {} }`
- out: `{ "translated": "", "glossary_hits": [""] }`

### N17 図の説明・限定様式（MM）
- in: `{ "image_ref": "", "template": "ui|diagram|photo" }`
- out: `{ "description": "", "checklist": [{"item":"", "seen":true}] }`

### N18 危険依頼の拒否文（安全）
- in: `{ "user_request": "", "category_guess": "" }`
- out: `{ "refuse": true, "user_message": "", "safe_alternative": "" }`
- 常に status=refused または ok+refuse true

### N-SAFE-*（高リスク非断定・任意）
断定診断・法的結論・軍事作戦は **unit を作らない**。  
必要なら後日: `N-SAFE-questions`（質問リスト化のみ）を追加。

---

## 4. 受付（Reception）が守る呼び出し規則
1. 未知 unit_id → invoke しない / 退避
2. `allow_side_effects=false` のとき、実行系道具を持つ単位は dry-run のみ
3. citations が必要な単位（N06等）で空引用 → Gate1で partial/refused
4. `deadline_ms` 超過 → error TIMEOUT retryable
5. ユーザー向け文面は原則 `output.summary` を土台に Reception が整形

---

## 5. バージョニング
- 破壊的変更は `cortext9-unit/v1`
- 単位追加はカタログ追記のみで v0 維持可
- payload 必須キー削除は破壊的

## 6. 最小実装パス
1. `POST /v0/invoke` 共通エンベロープのみ
2. 実装ユニット順: **N18 → N03 → N06 → N12**（拒否・開発・要約・運用）
3. 残りは stub（status=error, code=UNIMPLEMENTED）

## 7. 未決（K確認用）
- 同期のみか、非同期ジョブ（`job_id`）も要るか
- artifacts の実体保存先（S3相当 / git / ローカル）
- crush_score_hint をユニットが出すか、評価器が別か
