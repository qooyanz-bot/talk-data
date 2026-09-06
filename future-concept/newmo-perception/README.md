# newmo Perception — talk-data canonicalization

- 目的: newmo Perception Engineer 面接・設計議論用の正本（talk-data）を一箇所に集約する
- ステータス: **K-approved 2026-09-06**
- 文字コード: UTF-8

## 文書一覧（A–D）

| ID | ファイル | 内容 | 版 / 承認 |
|---|---|---|---|
| A | `A-interview-pitch-1min.md` | 面接用1分ピッチ | v0.1 K承認 2026-09-06 |
| B-template | `B-failure-catalog-template.md` | 失敗条件カタログ雛形・スキーマ | v0.1 K承認 2026-09-06 |
| B-filled | `B-failure-catalog-F001-F010.md` | F-001〜F-010 記入済みシード | v0.1 K承認 2026-09-06 |
| C | `C-e2e-input-schema-draft.md` | E2E入力スキーマ草案 | v0.1 K承認 2026-09-06 |
| D | `D-interview-qa.md` | 面接Q&A（実経験差し込み版） | v0.1 K承認 2026-09-06 |

## 運用メモ

- 定量値・未検証の固有名詞は各ファイル内の 【要差し替え：Kが実数・固有名詞を記入】 を正とする
- 失敗条件の閾値は 【仮閾値・要実測】。特定雇用主での観測インシデント主張ではない
- H1内輪用語は使わず、「失敗条件」「入力契約」で統一

## 更新履歴

- 2026-09-06: A–D を K承認。B-filled（F-001〜010）と D-interview-qa を追加。本 README で正本化。
