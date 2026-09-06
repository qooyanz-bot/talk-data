# 次担当エージェント向けプロンプト（継続実装）

あなたは Address Theory / Addressable Concept Architecture の実装担当です。
K（亀田紀明）が承認者。AIは単独で Future Concept 最終決定をしない。
正本: https://github.com/qooyanz-bot/talk-data

### 開始前に必ず直接確認

1. `git fetch && git checkout main && git pull --rebase origin main`
2. `git rev-parse HEAD`（引き継ぎ時点: `3d80682`。最後の実装 commit: `3d80682`）
3. tests: `python -m unittest discover -s address/reference-runtime-v0.1/tests -v`
4. `python address/reference-runtime-v0.1/address_cli.py --conformance`
5. `python address/reference-runtime-v0.1/address_cli.py --runtime-manifest`
6. `python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check`

Windows clone:
`C:\Users\qooya\Documents\Codex\2026-09-06\2-address-text-address-theory-addressable\work\talk-data`

Python:
`C:\Users\qooya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

git identity: `qooyanz-bot <qooyanz@gmail.com>`

force-push 禁止。main が進んでいたら rebase。

### 絶対禁止

- 宇宙DB/秘密値/介入/未来直接取得/暗号破りを技術事実として書かない
- R6-G 実行・Holdout 開封を主張しない。value を埋めて成功にしない（成功でも value=null）
- 推測で過去会話や repo を再構成しない

### 既に main にあるもの（再実装しない）

`address/reference-runtime-v0.1/` 一式。詳細は `address/handoffs/2026-09-06-address-reference-runtime-codex-handoff-continuation.md` 参照。

### 推奨の次増分（順不同・選んで進行）

1. `decision_log` など残存 set 定数の frozenset 化と単一正本 export
2. `resolution_gate` decision/reason と response_contract エイリアスの実一致テスト強化
3. CLI standalone モード組み合わせの一覧テスト固定
4. frozen API サーフェス（公開関数・定数・CLI フラグ）の共通列出力 helper と凍結
5. 構成ドキュメントの一括同期（README/CHANGELOG）

各増分: 不変条件→unittest全緑→changelog→commit→push→CI確認→次へ。
ゴール完了扱いで止めない。ただし Future Concept 最終は K 待ち。