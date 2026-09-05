# Cortext9 圧勝単位 細分化追加 v0.1
親スキーマ: `Cortext9-unit-api-schema-v0.md`（共通エンベロープは変更なし）
単位数: **102**（N01–N18＋細分＋新規）
断定ユニット禁止: 医療診断・法律結論・軍事作戦はそのまま。

## カタログ
| ID | 名前 | ドメイン | parent |
|---|---|---|---|
| N01 | 議事録下書き | work | - |
| N01a | 会議アジェンダ作成 | work | N01 |
| N01b | 決定事項→ToDo化 | work | N01 |
| N01c | お詫び・丁寧メール | work | N01 |
| N01d | 催促・リマインドメール | work | N01 |
| N02 | 仕様→チケット分解 | work | - |
| N02a | 受け入れ条件(AC)作成 | work | N02 |
| N02b | 見積もり用タスク粒度分割 | work | N02 |
| N02c | リスク・依存の洗い出し | work | N02 |
| N03 | 関数単位実装 | dev | - |
| N03a | 型定義・インターフェース作成 | dev | N03 |
| N03b | 単体テスト生成 | dev | N03 |
| N03c | リファクタ（挙動維持） | dev | N03 |
| N03d | コメント・docstring整備 | dev | N03 |
| N04 | 失敗テスト修正 | dev | - |
| N04a | エラーログ切り分け手順 | dev | N04 |
| N04b | フレークテスト安定化案 | dev | N04 |
| N04c | 最小再現コード作成 | dev | N04 |
| N05 | PRレビュー指摘 | dev | - |
| N05a | セキュリティ観点レビュー | dev | N05 |
| N05b | パフォーマンス観点レビュー | dev | N05 |
| N05c | PR説明文生成 | dev | N05 |
| N05d | 破壊的変更のチェックリスト | dev | N05 |
| N06 | 根拠付き短文要約 | research | - |
| N06a | 未決・未確認の抽出 | research | N06 |
| N06b | 主張と証拠の対応表 | research | N06 |
| N06c | 要約の長さ別リライト | research | N06 |
| N07 | 比較表作成 | research | - |
| N07a | 評価軸の提案 | research | N07 |
| N07b | 競合・代替の列挙 | research | N07 |
| N07c | Pros/Consのみ | research | N07 |
| N08 | 中学生向け解説 | edu | - |
| N08a | 例え話のみ生成 | edu | N08 |
| N08b | 確認問題のみ生成 | edu | N08 |
| N08c | 用語集（短） | edu | N08 |
| N09 | ヒントのみ誘導 | edu | - |
| N09a | 段階ヒント（1つずつ） | edu | N09 |
| N09b | 誤答パターン指摘（答えなし） | edu | N09 |
| N10 | FC柱の整理 | fc | - |
| N10a | 未決リスト化 | fc | N10 |
| N10b | H1用語の短定義 | fc | N10 |
| N10c | 旧解釈退行チェック | fc | N10 |
| N11 | ゲート仮採点 | fc | - |
| N11a | Hard Reject(E系)のみ採点 | fc | N11 |
| N11b | 開始ゲート6条件チェック | fc | N11 |
| N12 | changelog下書き | ops | - |
| N12a | コミットメッセージ案 | ops | N12 |
| N12b | 昇格候補1行追加案 | ops | N12 |
| N13 | 自己点検E系 | ops | - |
| N13a | インベントリ差分要約 | ops | N13 |
| N13b | 週次ダイジェスト見出し | ops | N13 |
| N14 | 表データ整形 | data | - |
| N14a | CSVヘッダ正規化 | data | N14 |
| N14b | 欠損・異常値フラグ | data | N14 |
| N14c | JSON↔表変換 | data | N14 |
| N15 | SQL下書き | data | - |
| N15a | SELECTのみ（破壊なし保証） | data | N15 |
| N15b | 実行計画の読み方コメント | data | N15 |
| N15c | インデックス案（非適用） | data | N15 |
| N16 | 翻訳 | transform | - |
| N16a | 用語集固定翻訳 | transform | N16 |
| N16b | 敬体・常体のトーン変換 | transform | N16 |
| N16c | 箇条書き↔段落変換 | transform | N16 |
| N17 | 図の説明 | mm | - |
| N17a | UI画面の要素一覧 | mm | N17 |
| N17b | フロー図の步骤列挙 | mm | N17 |
| N17c | スライド1枚の要約 | mm | N17 |
| N18 | 危険依頼拒否 | safety | - |
| N18a | 拒否＋安全な代替提案 | safety | N18 |
| N18b | ポリシー根拠の短い説明 | safety | N18 |
| N19 | 週報・日報テンプレ記入 | work | - |
| N20 | 1枚提案構成のみ | work | - |
| N21 | FAQ下書き（社内） | work | - |
| N22 | OpenAPI断片生成 | dev | - |
| N23 | 正規表現の説明とテスト例 | dev | - |
| N24 | 依存アップデート注意点リスト | dev | - |
| N25 | 設計トレードオフ3択 | dev | - |
| N26 | 論文ではない一般知識の限界注記付き解説 | research | - |
| N27 | 反証観点の列挙 | research | - |
| N28 | 参考文献ルール（偽引用防止） | research | - |
| N29 | 学習ロードマップ（週単位） | edu | - |
| N30 | 誤概念の訂正（優しく） | edu | - |
| N31 | Address表の1行追加案 | fc | - |
| N32 | Future Concept失敗シナリオ短編 | fc | - |
| N33 | RunPod費用メモ整形 | ops | - |
| N34 | ルーチン結果の1段落要約 | ops | - |
| N35 | ログから時系列タイムライン | data | - |
| N36 | メトリクス定義の明確化 | data | - |
| N37 | 英日UIラベル統一 | transform | - |
| N38 | 誤字脱字・表記ゆれ修正 | transform | - |
| N39 | スクリーンショットの操作手順化 | mm | - |
| N40 | 図表キャプション案 | mm | - |
| N41 | 個人情報のマスキング案 | safety | - |
| N42 | 秘密が混入していないか点検 | safety | - |
| N43 | 受診前の質問リスト化（非診断） | care_safe | - |
| N44 | 契約の読み方チェックリスト（非断定） | legal_safe | - |
| N45 | 家計・投資の仕組み説明（非助言） | finance_safe | - |
| N46 | 危機時コミュニケーション草稿（一般） | crisis_safe | - |
| N47 | アクセシビリティ改善提案 | product | - |
| N48 | ユーザーストーリー1本 | product | - |
| N49 | 受け入れデモ手順 | product | - |
| N50 | インシデント事後レビュー骨子 | ops | - |

## 追加単位の payload 要旨（差分のみ）

| ID | in.payload 要旨 | out.payload 要旨 |
|---|---|---|
| N01a | `{ "topics":[], "duration_min":30 }` | `{ "agenda_md":"" }` |
| N01b | `{ "decisions":[] }` | `{ "todos":[] }` |
| N01c | `{ "situation":"", "audience":"" }` | `{ "email_md":"" }` |
| N01d | `{ "what":"", "due":"" }` | `{ "email_md":"" }` |
| N02a | `{ "feature":"" }` | `{ "acceptance_criteria":[] }` |
| N02b | `{ "epic":"", "max_hours_each":8 }` | `{ "tasks":[] }` |
| N02c | `{ "plan":"" }` | `{ "risks":[], "deps":[] }` |
| N03a | `{ "language":"", "behavior":"" }` | `{ "types_code":"" }` |
| N03b | `{ "code":"", "language":"" }` | `{ "tests":"" }` |
| N03c | `{ "code":"", "preserve_behavior":true }` | `{ "refactored":"", "notes":"" }` |
| N03d | `{ "code":"" }` | `{ "documented":"" }` |
| N04a | `{ "log":"" }` | `{ "steps":[] }` |
| N04b | `{ "test_name":"", "symptoms":"" }` | `{ "ideas":[] }` |
| N04c | `{ "bug_report":"" }` | `{ "repro_code":"" }` |
| N05a | `{ "diff":"" }` | `{ "findings":[] }` |
| N05b | `{ "diff":"" }` | `{ "findings":[] }` |
| N05c | `{ "diff":"", "motivation":"" }` | `{ "pr_md":"" }` |
| N05d | `{ "change_summary":"" }` | `{ "checklist":[] }` |
| N06a | `{ "text":"" }` | `{ "undecided":[] }` |
| N06b | `{ "text":"" }` | `{ "rows":[{"claim":"","evidence":""}] }` |
| N06c | `{ "text":"", "target_len":"short|mid" }` | `{ "rewrite":"" }` |
| N07a | `{ "decision":"" }` | `{ "axes":[] }` |
| N07b | `{ "topic":"" }` | `{ "alternatives":[] }` |
| N07c | `{ "item":"" }` | `{ "pros":[], "cons":[] }` |
| N08a | `{ "topic":"" }` | `{ "analogy":"" }` |
| N08b | `{ "topic":"" }` | `{ "quiz":{"q":"","a":""} }` |
| N08c | `{ "topic":"" }` | `{ "glossary":[] }` |
| N09a | `{ "problem":"", "level":1 }` | `{ "hint":"", "leaked_answer":false }` |
| N09b | `{ "problem":"", "wrong_approach":"" }` | `{ "feedback":"", "leaked_answer":false }` |
| N10a | `{ "text":"" }` | `{ "undecided":[] }` |
| N10b | `{ "terms":[] }` | `{ "definitions":[] }` |
| N10c | `{ "text":"" }` | `{ "regressions_found":[] }` |
| N11a | `{ "proposal":"" }` | `{ "E1":"","E2":"","E3":"","E4":"","E5":"" }` |
| N11b | `{ "proposal":"" }` | `{ "six_gates":[] }` |
| N12a | `{ "diff_stat":"" }` | `{ "message":"" }` |
| N12b | `{ "item":"" }` | `{ "row_md":"" }` |
| N13a | `{ "before":[], "after":[] }` | `{ "summary_md":"" }` |
| N13b | `{ "period":"" }` | `{ "headings":[] }` |
| N14a | `{ "csv":"" }` | `{ "headers":[], "csv_out":"" }` |
| N14b | `{ "rows":[] }` | `{ "flags":[] }` |
| N14c | `{ "json_or_csv":"", "direction":"to_table|to_json" }` | `{ "result":"" }` |
| N15a | `{ "ask":"", "schema_ddl":"" }` | `{ "sql":"", "destructive":false }` |
| N15b | `{ "explain_output":"" }` | `{ "comments":[] }` |
| N15c | `{ "slow_query":"" }` | `{ "index_ideas":[], "applied":false }` |
| N16a | `{ "text":"", "glossary":{} }` | `{ "translated":"" }` |
| N16b | `{ "text":"", "tone":"desu|dearu" }` | `{ "rewritten":"" }` |
| N16c | `{ "text":"", "direction":"bullets|prose" }` | `{ "rewritten":"" }` |
| N17a | `{ "image_ref":"" }` | `{ "elements":[] }` |
| N17b | `{ "image_ref":"" }` | `{ "steps":[] }` |
| N17c | `{ "image_ref":"" }` | `{ "caption_summary":"" }` |
| N18a | `{ "user_request":"" }` | `{ "refuse":true, "user_message":"", "safe_alternative":"" }` |
| N18b | `{ "user_request":"" }` | `{ "policy_reason":"" }` |
| N19 | `{ "facts":[] }` | `{ "report_md":"" }` |
| N20 | `{ "problem":"", "proposal":"" }` | `{ "outline":[] }` |
| N21 | `{ "topic":"", "audience":"internal" }` | `{ "faq":[] }` |
| N22 | `{ "endpoint":"", "method":"GET" }` | `{ "openapi_yaml":"" }` |
| N23 | `{ "intent":"" }` | `{ "regex":"", "examples":[] }` |
| N24 | `{ "package":"", "from":"", "to":"" }` | `{ "cautions":[] }` |
| N25 | `{ "problem":"" }` | `{ "options":[{"name":"","pros":[],"cons":[]}] }` |
| N26 | `{ "topic":"" }` | `{ "explanation":"", "limits":[] }` |
| N27 | `{ "claim":"" }` | `{ "counterpoints":[] }` |
| N28 | `{ "draft":"" }` | `{ "rules":[], "fake_citations_found":false }` |
| N29 | `{ "goal":"", "weeks":4 }` | `{ "plan":[] }` |
| N30 | `{ "misconception":"" }` | `{ "correction":"" }` |
| N31 | `{ "fail_id":"", "dimension":"", "proxy":"" }` | `{ "row_md":"" }` |
| N32 | `{ "pillar":"" }` | `{ "failure_story":"" }` |
| N33 | `{ "usage_lines":[] }` | `{ "cost_memo_md":"" }` |
| N34 | `{ "routine_log":"" }` | `{ "paragraph":"" }` |
| N35 | `{ "log_text":"" }` | `{ "timeline":[] }` |
| N36 | `{ "fuzzy_metric":"" }` | `{ "definition":"", "formula":"" }` |
| N37 | `{ "labels":[] }` | `{ "unified":[] }` |
| N38 | `{ "text":"" }` | `{ "corrected":"", "changes":[] }` |
| N39 | `{ "image_ref":"" }` | `{ "howto_steps":[] }` |
| N40 | `{ "figure_desc":"" }` | `{ "caption":"" }` |
| N41 | `{ "text":"" }` | `{ "masked":"", "entities":[] }` |
| N42 | `{ "text":"" }` | `{ "secret_like_spans":[], "clean":true }` |
| N43 | `{ "situation":"" }` | `{ "questions_for_clinician":[], "diagnosis":null }` |
| N44 | `{ "contract_excerpt":"" }` | `{ "checklist":[], "legal_conclusion":null }` |
| N45 | `{ "topic":"" }` | `{ "mechanism":"", "advice":null }` |
| N46 | `{ "event":"" }` | `{ "draft_md":"", "operational_orders":null }` |
| N47 | `{ "ui_desc":"" }` | `{ "a11y_suggestions":[] }` |
| N48 | `{ "feature":"" }` | `{ "story":"" }` |
| N49 | `{ "feature":"" }` | `{ "demo_steps":[] }` |
| N50 | `{ "incident":"" }` | `{ "postmortem_outline":[] }` |

## 分類機へのヒント
- 子ID（N03a 等）を優先。無いときだけ親 N03 へフォールバック
- N43–N46 は **非断定** をスキーマで強制（diagnosis/legal_conclusion/advice/operational_orders は null 固定）
- 最小実装の推奨順は引き続き N18系 → N03系 → N06系 → N12系、細分は需要で追加
