# 2026-09-06 Address reference runtime v0.1

## 追加

- `address/reference-runtime-v0.1/` に、Address Schemaの最小安全不変条件を検査する依存なし参照実装と4件のunittestを追加。
- synthetic fixture、canonical hash検証、unknownのabstain、real world scope制限を対象にした。
- Evidence Contractを追加し、path IDだけでなくauthority・generator・semantic lawの共通原因を検出する。metadata分離は `CONTRACTED` に留め、監査済みsemantic independenceとは扱わない。
- Resolution Gateを追加。Address、Evidence Contract、鮮度、assertion矛盾を統合し、未達時は必ず `ABSTAIN` / `value=null` とする。
- content-addressed Audit Logを追加。Valueとassertion本文を保存せず、Address・evidence digest・判定・時刻を再計算できるaudit IDとして記録する。

## 自己点検

- E系: 外部接続、秘密読取り、認証回避、個人の隠れた情報、未来値取得を実装していない。
- B5: Future Conceptの最終決定は行わない。これは既承認Schemaの実装・検証に限る。
