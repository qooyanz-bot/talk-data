# Cortext9 圧勝単位 細分化追加 v0.2

親: `Cortext9-unit-api-schema-v0.md` / 前回細分: `Cortext9-unit-api-schema-v0.1-addendum.md`

単位数: **218**（v0.1から +116）

断定ユニット禁止: 医療診断・法律結論・軍事作戦はそのまま。N43–N46 系は非断定強制。

## 今回追加 ID

`N19a`, `N19b`, `N20a`, `N20b`, `N21a`, `N21b`, `N22a`, `N22b`, `N23a`, `N23b`, `N24a`, `N24b`, `N25a`, `N25b`, `N26a`, `N26b`, `N27a`, `N27b`, `N28a`, `N28b`, `N29a`, `N29b`, `N30a`, `N30b`, `N31a`, `N31b`, `N32a`, `N32b`, `N33a`, `N33b`, `N34a`, `N34b`, `N35a`, `N35b`, `N36a`, `N36b`, `N37a`, `N37b`, `N38a`, `N38b`, `N39a`, `N39b`, `N40a`, `N40b`, `N41a`, `N41b`, `N42a`, `N42b`, `N43a`, `N43b`, `N44a`, `N44b`, `N45a`, `N45b`, `N46a`, `N46b`, `N47a`, `N47b`, `N48a`, `N48b`, `N49a`, `N49b`, `N50a`, `N50b`, `N51`, `N51a`, `N51b`, `N52`, `N52a`, `N52b`, `N53`, `N54`, `N55`, `N55a`, `N55b`, `N56`, `N57`, `N58`, `N59`, `N60`, `N60a`, `N60b`, `N61`, `N62`, `N63`, `N64`, `N65`, `N66`, `N67`, `N68`, `N69`, `N70`, `N71`, `N72`, `N73`, `N74`, `N75`, `N76`, `N77`, `N78`, `N79`, `N80`, `N80a`, `N80b`, `N81`, `N82`, `N83`, `N84`, `N85`, `N86`, `N87`, `N88`, `N89`, `N90`, `N90a`, `N90b`

## 全カタログ

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
| N19a | 日報の事実のみ抽出 | work | N19 |
| N19b | 週報のハイライト3点 | work | N19 |
| N20a | 提案の課題定義のみ | work | N20 |
| N20b | 提案の効果仮説のみ | work | N20 |
| N21a | FAQの質問候補生成 | work | N21 |
| N21b | FAQ回答の根拠注記 | work | N21 |
| N22a | リクエスト例のみ | dev | N22 |
| N22b | エラーレスポンス定義 | dev | N22 |
| N23a | 正規表現の分解説明 | dev | N23 |
| N23b | マッチ失敗ケース列挙 | dev | N23 |
| N24a | 破壊的変更の有無チェック | dev | N24 |
| N24b | ロールバック手順メモ | dev | N24 |
| N25a | トレードオフ採点表 | dev | N25 |
| N25b | 採用しない案の理由 | dev | N25 |
| N26a | 知識の確度ラベル付け | research | N26 |
| N26b | 要出典箇所のマーキング | research | N26 |
| N27a | 反証実験の設計案 | research | N27 |
| N27b | 前提の洗い出し | research | N27 |
| N28a | 引用形式の整形 | research | N28 |
| N28b | 存在未確認文献の除去 | research | N28 |
| N29a | 週ごとの到達目標のみ | edu | N29 |
| N29b | 前提知識チェックリスト | edu | N29 |
| N30a | 誤概念の対比表 | edu | N30 |
| N30b | 正しい手順のミニ例 | edu | N30 |
| N31a | proxy候補の列挙 | fc | N31 |
| N31b | 閾値案の1行 | fc | N31 |
| N32a | 失敗シナリオのトリガー条件 | fc | N32 |
| N32b | 回避レバーの列挙 | fc | N32 |
| N33a | 時間×単価の表整形 | ops | N33 |
| N33b | 無駄遣い候補の指摘 | ops | N33 |
| N34a | 異常のみ1段落 | ops | N34 |
| N34b | 変化なし宣言文 | ops | N34 |
| N35a | エラー行のみ抽出 | data | N35 |
| N35b | タイムゾーン注記付き時系列 | data | N35 |
| N36a | 分子・分母の定義 | data | N36 |
| N36b | 除外条件の明示 | data | N36 |
| N37a | 用語ゆれの統一表 | transform | N37 |
| N37b | 文字数制約付きラベル | transform | N37 |
| N38a | 固有名詞保護の校正 | transform | N38 |
| N38b | 半角全角の正規化 | transform | N38 |
| N39a | 操作の前提条件リスト | mm | N39 |
| N39b | 失敗時の戻り手順 | mm | N39 |
| N40a | キャプション短/長2案 | mm | N40 |
| N40b | altテキスト案 | mm | N40 |
| N41a | メール・電話のマスキング | safety | N41 |
| N41b | 住所・IDのマスキング | safety | N41 |
| N42a | APIキーらしき文字列検出 | safety | N42 |
| N42b | パスフレーズらしき検出 | safety | N42 |
| N43a | 症状の時系列整理（非診断） | care_safe | N43 |
| N43b | 持参情報チェックリスト（非診断） | care_safe | N43 |
| N44a | 定義語の洗い出し（非断定） | legal_safe | N44 |
| N44b | 曖昧条項の質問リスト（非断定） | legal_safe | N44 |
| N45a | 金利・複利の仕組み図説（非助言） | finance_safe | N45 |
| N45b | 手数料の見え方整理（非助言） | finance_safe | N45 |
| N46a | 事実確認の質問リスト | crisis_safe | N46 |
| N46b | 関係者向け短文テンプレ | crisis_safe | N46 |
| N47a | キーボード操作のみ改善 | product | N47 |
| N47b | コントラスト・テキスト改善 | product | N47 |
| N48a | ユーザーストーリーの受入条件 | product | N48 |
| N48b | 非機能要求の1行 | product | N48 |
| N49a | デモ用サンプルデータ案 | product | N49 |
| N49b | デモ失敗時のフォールバック | product | N49 |
| N50a | タイムライン骨子のみ | ops | N50 |
| N50b | 再発防止の仮説リスト | ops | N50 |
| N51 | 会議の決定 vs 議論の分離 | work | - |
| N51a | 決定だけ箇条書き | work | N51 |
| N51b | 未決だけ箇条書き | work | N51 |
| N52 | ステークホルダー向け要約 | work | - |
| N52a | 経営向け3行 | work | N52 |
| N52b | 現場向け手順中心 | work | N52 |
| N53 | オンボーディングチェックリスト | work | - |
| N54 | 面接質問の構造化（非評価断定） | work | - |
| N55 | CI失敗ログの最短切り分け | dev | - |
| N55a | 失敗ジョブの特定 | dev | N55 |
| N55b | フレーク疑いフラグ | dev | N55 |
| N56 | Dockerfile最小改善案 | dev | - |
| N57 | 環境変数一覧の文書化 | dev | - |
| N58 | マイグレーション下書き（破壊なし注記） | dev | - |
| N59 | ベンチマーク手順書 | dev | - |
| N60 | 仮説→検証手順カード | research | - |
| N60a | 成功判定の明示 | research | N60 |
| N60b | 失敗時の次の一手 | research | N60 |
| N61 | 用語のドメイン間対応表 | research | - |
| N62 | 調査メモの出典スロット埋め | research | - |
| N63 | 口頭発表の1分ピッチ | edu | - |
| N64 | 練習問題の難易度ラダー | edu | - |
| N65 | 誤答からの学習ポイント | edu | - |
| N66 | ConceptとDimensionの混同チェック | fc | - |
| N67 | CLEAR条件の自己点検質問 | fc | - |
| N68 | Addressスコア表の欠損埋め | fc | - |
| N69 | 正本昇格チェックリスト | ops | - |
| N70 | ルーチン失敗の原因候補 | ops | - |
| N71 | バックアップ確認手順 | ops | - |
| N72 | スキーマ差分の人間向け説明 | data | - |
| N73 | 重複行の判定ルール案 | data | - |
| N74 | 単位・通貨の正規化ルール | data | - |
| N75 | 議事録→英語サマリ | transform | - |
| N76 | 口語→書き言葉変換 | transform | - |
| N77 | 動画のチャプター案（非視聴断定） | mm | - |
| N78 | ワイヤーの画面遷移リスト | mm | - |
| N79 | 権限昇格リスクのチェックリスト | safety | - |
| N80 | 外部送信前の最終点検 | safety | - |
| N80a | 宛先・CCの確認文言 | safety | N80 |
| N80b | 添付の過不足チェック | safety | N80 |
| N81 | アクセシビリティ手動テスト手順 | product | - |
| N82 | リリースノート顧客向け | product | - |
| N83 | サポート返信の共感＋手順 | product | - |
| N84 | KPI定義の一文化 | product | - |
| N85 | A/Bテスト仮説カード（非統計断定） | product | - |
| N86 | プロンプトの失敗例カタログ化 | ml_ops | - |
| N87 | 評価セットの項目設計 | ml_ops | - |
| N88 | 拒否ケースのゴールデン例 | ml_ops | - |
| N89 | 単位間ハンドオフ仕様の1行 | ml_ops | - |
| N90 | Reception振り分けルール案 | ml_ops | - |
| N90a | 曖昧入力の確認質問 | ml_ops | N90 |
| N90b | 複数単位候補の並べ方 | ml_ops | N90 |

## 追加単位の payload 要旨（v0.2 新規のみ）

| ID | in要旨 | out要旨 |
|---|---|---|
| N19a | `facts_raw` | `facts_only[]` |
| N19b | `week_notes` | `highlights[3]` |
| N20a | `context` | `problem_def` |
| N20b | `proposal` | `effect_hypotheses[]` |
| N21a | `topic` | `question_candidates[]` |
| N21b | `faq_draft` | `answers_with_sources[]` |
| N22a | `endpoint` | `request_examples[]` |
| N22b | `endpoint` | `error_schemas[]` |
| N23a | `regex` | `piecewise_explain` |
| N23b | `regex` | `non_match_cases[]` |
| N24a | `changelog` | `breaking:bool + notes` |
| N24b | `change` | `rollback_steps[]` |
| N25a | `options` | `score_table` |
| N25b | `chosen` | `rejected_reasons[]` |
| N26a | `text` | `spans[{text,confidence}]` |
| N26b | `text` | `needs_citation[]` |
| N27a | `claim` | `experiment_design` |
| N27b | `claim` | `assumptions[]` |
| N28a | `refs` | `formatted[]` |
| N28b | `draft` | `removed_fake_cites[]` |
| N29a | `goal,weeks` | `weekly_goals[]` |
| N29b | `goal` | `prereq_checklist[]` |
| N30a | `misconception` | `contrast_table` |
| N30b | `topic` | `mini_example` |
| N31a | `fail_id` | `proxy_candidates[]` |
| N31b | `proxy` | `threshold_oneline` |
| N32a | `pillar` | `trigger_conditions[]` |
| N32b | `scenario` | `levers[]` |
| N33a | `usage_lines` | `cost_table` |
| N33b | `usage_lines` | `waste_candidates[]` |
| N34a | `routine_log` | `anomaly_paragraph` |
| N34b | `routine_log` | `no_change_sentence` |
| N35a | `log_text` | `error_lines[]` |
| N35b | `log_text,tz` | `timeline_tz[]` |
| N36a | `metric` | `numerator,denominator` |
| N36b | `metric` | `exclusions[]` |
| N37a | `labels` | `unify_table` |
| N37b | `labels,max_len` | `labels_out[]` |
| N38a | `text,protect[]` | `corrected` |
| N38b | `text` | `normalized` |
| N39a | `image_ref` | `prerequisites[]` |
| N39b | `image_ref` | `undo_steps[]` |
| N40a | `figure_desc` | `caption_short,caption_long` |
| N40b | `figure_desc` | `alt_text` |
| N41a | `text` | `masked` |
| N41b | `text` | `masked` |
| N42a | `text` | `api_key_like[]` |
| N42b | `text` | `passphrase_like[]` |
| N43a | `situation` | `symptom_timeline[]; diagnosis:null` |
| N43b | `situation` | `bring_list[]; diagnosis:null` |
| N44a | `excerpt` | `defined_terms[]; legal_conclusion:null` |
| N44b | `excerpt` | `ambiguity_questions[]; legal_conclusion:null` |
| N45a | `topic` | `mechanism; advice:null` |
| N45b | `topic` | `fee_visibility; advice:null` |
| N46a | `event` | `fact_check_qs[]; operational_orders:null` |
| N46b | `event,audience` | `short_template; operational_orders:null` |
| N47a | `ui_desc` | `keyboard_a11y[]` |
| N47b | `ui_desc` | `contrast_text[]` |
| N48a | `story` | `acceptance[]` |
| N48b | `feature` | `nfr_oneline` |
| N49a | `feature` | `sample_data` |
| N49b | `feature` | `fallback_steps[]` |
| N50a | `incident` | `timeline_outline[]` |
| N50b | `incident` | `prevention_hypotheses[]` |
| N51 | `notes` | `decisions[],discussions[]` |
| N51a | `notes` | `decisions_only[]` |
| N51b | `notes` | `undecided_only[]` |
| N52 | `doc,audience` | `summary` |
| N52a | `doc` | `exec_3lines` |
| N52b | `doc` | `field_howto` |
| N53 | `role` | `checklist[]` |
| N54 | `role` | `structured_qs[]; evaluation:null` |
| N55 | `ci_log` | `shortest_triage` |
| N55a | `ci_log` | `failed_job` |
| N55b | `ci_log` | `flake_suspect:bool` |
| N56 | `dockerfile` | `minimal_improvements[]` |
| N57 | `code_or_env` | `env_doc[]` |
| N58 | `change` | `migration_sql; destructive_notes` |
| N59 | `target` | `bench_steps[]` |
| N60 | `hypothesis` | `verify_card` |
| N60a | `hypothesis` | `success_criteria` |
| N60b | `hypothesis` | `next_if_fail` |
| N61 | `terms,domains` | `mapping_table` |
| N62 | `memo` | `slots_with_sources` |
| N63 | `topic` | `one_min_pitch` |
| N64 | `topic` | `difficulty_ladder[]` |
| N65 | `wrong,correct` | `learning_points[]` |
| N66 | `text` | `confusion_hits[]` |
| N67 | `state` | `self_check_qs[]` |
| N68 | `address_table` | `filled_gaps[]` |
| N69 | `candidate` | `promotion_checklist[]` |
| N70 | `routine_fail` | `cause_candidates[]` |
| N71 | `system` | `backup_verify_steps[]` |
| N72 | `schema_diff` | `human_explain` |
| N73 | `sample_rows` | `dedupe_rules` |
| N74 | `columns` | `normalize_rules` |
| N75 | `minutes_ja` | `summary_en` |
| N76 | `colloquial` | `written` |
| N77 | `transcript_or_outline` | `chapters[]; watched:false` |
| N78 | `wire_desc` | `screen_flows[]` |
| N79 | `change` | `priv_escalation_checklist[]` |
| N80 | `outbound_draft` | `final_checks[]` |
| N80a | `draft` | `recipient_confirm_text` |
| N80b | `draft,attachments` | `attach_check` |
| N81 | `ui` | `manual_a11y_steps[]` |
| N82 | `changes` | `customer_release_notes` |
| N83 | `ticket` | `empathy_plus_steps` |
| N84 | `fuzzy_kpi` | `one_sentence_def` |
| N85 | `idea` | `ab_card; statistical_claim:null` |
| N86 | `prompt_logs` | `failure_catalog[]` |
| N87 | `capability` | `eval_items[]` |
| N88 | `policy` | `golden_refuse_cases[]` |
| N89 | `from_unit,to_unit` | `handoff_oneline` |
| N90 | `utterance` | `route_rules_draft` |
| N90a | `ambiguous` | `clarify_qs[]` |
| N90b | `candidates` | `ranked_units[]` |

## 分類ヒント（v0.2）

- 子ID優先 → 親フォールバック（従来どおり）
- `ml_ops`（N86–N90）は Cortext9 自体の運用・評価・振り分け用
- N54/N85 等は **評価断定・統計断定を null 固定**
- 最小実装推奨順は不変: N18系 → N03系 → N06系 → N12系。細分は需要で載せる
