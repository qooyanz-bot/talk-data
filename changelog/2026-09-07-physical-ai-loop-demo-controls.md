# Physical AI Loop デモ操作拡張 — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（合成デモ。実機検証完了は主張しない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `9a38cb3`

## 実装

- `Safety Filter / Intent Shield` の strictness を `runImprovementLoop` 入力に追加。
- UIに `Constraint strictness` slider と success proxy を追加。
- `parseRobotLogJson` を追加し、ブラウザ内で RobotLog JSON を貼り付け解析できるようにした。
- `buildIncidentReport` を追加し、選択ログ/セグメントのMarkdownインシデントレポートを生成できるようにした。
- UIに `Local log parser` と `Incident report` panel を追加。

## 検証

- `npm test`: 10/10 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `Constraint strictness` / `Local log parser` / `Incident report` が含まれることを確認

## 非主張

- 実機データの安全保証ではない。
- strictness / success proxy はデモ用の制約評価であり、認証済み安全指標ではない。

