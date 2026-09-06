# Physical AI Loop newmo fit / CSV / export 拡張 — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（合成デモ。実機検証完了は主張しない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `f7537cf`

## 実装

- `parseRobotLogCsv` を追加し、CSV貼り付けからRobotLogへ変換できるようにした。
- `scoreNewmoFit` を追加し、E2E/VLA補正、Closed-Loop replay、perception semantics、data-centric field feedback、field integration readiness の5信号でnewmo fitを算出するようにした。
- UIに `newmo fit` panel を追加し、求人寄せの根拠を定量表示するようにした。
- UIに `Robot class comparison` panel を追加し、AMR / vehicle など複数サンプルログを同じ改善ループで比較できるようにした。
- Markdown incident report の `Download` button を追加した。

## 検証

- `npm test`: 11/11 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `newmo fit` / `Robot class comparison` / `Download` / `JSON/CSV` が含まれることを確認

## 非主張

- newmo内部要件の確定評価ではなく、公開求人からの戦略推定に基づくfit scoreである。
- CSV parser はデモ用の軽量パーサであり、全ログ形式対応を主張しない。

