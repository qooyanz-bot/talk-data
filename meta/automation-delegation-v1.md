# 自動化委任条項 v1（K承認 2026-09-05）

K発言「全部自動でやって」に基づく §17.5 例外の委任範囲。

## 自動でよい（都度承認不要）
1. talk-data の読み取り・インベントリ・リンク点検
2. `changelog/` への運用ログ追記（同期・点検・ルーチン結果の要約）
3. `meta/` 配下の運用ファイル更新（inventory、automation-index、昇格候補リスト）
4. 失敗条件の**仮採点**結果を `address/scoring-drafts/` に草案保存
5. ゲート穴埋め**草案**を `gates/drafts/` に保存（APPROVAL署名欄は空のまま）
6. open-questions / BD-v0 のリマインド文面生成とKへの通知
7. Hard Reject / 旧解釈の自己点検ログを `meta/self-checks/` へ
8. GitHub上の talk-data のPR/Issue/push検知の通知
9. 会話結論の「昇格候補」追記（`meta/promotion-candidates.md`）

## 自動にしてはいけない（都度K承認）
- Future Concept・境界・救済優先・例外ありなしの**確定**
- 統一プロンプト本文の意味改訂（字数圧縮の再提案は可、採用は承認）
- `future-concept/FC-H1.0.md` の意味改訂の本番反映
- 秘密の取得・権限変更
- ファイルの破壊的削除（deprecateポインタなし）
- 他者へのメッセージ送信・課金

## トーン
ドラえもん調可。決めつけない。未決は未決のまま残す。
