# 2026-09-06 Address reference runtime CI

## 追加

- `address/reference-runtime-v0.1/` とCI定義の変更時に、Python 3.12で全unittestを実行するGitHub Actions workflowを追加。

## 自己点検

- E系: CIは公開リポジトリ内の依存なしテストだけを実行し、秘密・外部実データ・認証情報には触れない。
- B5: Future Concept又は外部世界についての最終決定を行わない。既承認の参照実装に対する回帰検査である。
