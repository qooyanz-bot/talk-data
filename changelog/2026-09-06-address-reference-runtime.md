# 2026-09-06 Address reference runtime v0.1

## 追加

- `address/reference-runtime-v0.1/` に、Address Schemaの最小安全不変条件を検査する依存なし参照実装と4件のunittestを追加。
- synthetic fixture、canonical hash検証、unknownのabstain、real world scope制限を対象にした。
- Evidence Contractを追加し、path IDだけでなくauthority・generator・semantic lawの共通原因を検出する。metadata分離は `CONTRACTED` に留め、監査済みsemantic independenceとは扱わない。
- Resolution Gateを追加。Address、Evidence Contract、鮮度、assertion矛盾を統合し、未達時は必ず `ABSTAIN` / `value=null` とする。
- content-addressed Audit Logを追加。Valueとassertion本文を保存せず、Address・evidence digest・判定・時刻を再計算できるaudit IDとして記録する。
- Replay Verifierを追加。同じAddress・Evidence・時刻でGateを再実行し、監査ログの自己hashだけでなく、判断と系譜も照合する。
- malformed inputの型・時間・scope境界検査を強化。入力不備による例外停止を避け、`INVALID` として明示的に拒否する。
- Protocol Claim Gateを追加。R6-Gの直接確認済みmanifest状態を基準に、凍結・未実行・監査未完了のProtocolから結果又は能力を主張しないようブロックする。
- read-only Address CLIを追加。Address JSONとEvidence JSONからResolution、value-free Audit Log、任意のReplay検証までを一貫して実行する。Value導出、外部接続、ファイル書込みは実装しない。
- Response Contractを追加。公開CLI出力の`value=null`、既知の判定状態、Auditとの判断一致を検証し、出力回帰を拒否する。
- Memory scopeをauthorized/versioned/revocableへ固定し、Lineageの入力参照をSHA-256形式に制限。未許可・追跡不能な記憶／入力参照を拒否する。
- Audit Logのevidence digest項目が壊れている場合にも、例外停止せず明示的に拒否するよう修正。
- Audit Logの`create`が、非list evidenceや欠落／非文字列`evidence_id`でも例外停止せず、digest省略で明示拒否するよう硬化。CLIも同様に落ちないよう整合。
- Address CLIに`--protocol-manifest`と`--claim-type`を接続。SPEC_ONLY/R6-G凍結manifestではEXPERIMENT_RESULTとCAPABILITY_CLAIMをALLOWED_AS_RESULTにできない。Response Contractも任意の`protocol_claim`状態を検証する。
- CLI公開出力のgolden fixture（`fixtures/golden_cli_output.json`）を追加。必須キー・`value=null`・decision集合の構造検査で契約回帰を検出する。
- Resolution GateとResponse Contractで、READY_FOR_VERIFICATIONでもunknown slotをresidualのまま残し`value=null`を強制。typed bindingで未解決slotを埋めない。
- Address runtimeのtyped `target_value`検査を硬化。dict・非空type・value=null・residualはnull/list・no_speculation=trueを機械検証し、事前検証入力の`lineage.result_sha`非nullを拒否。Value発見は行わない。

## 自己点検

- E系: 外部接続、秘密読取り、認証回避、個人の隠れた情報、未来値取得を実装していない。
- B5: Future Conceptの最終決定は行わない。これは既承認Schemaの実装・検証に限る。
