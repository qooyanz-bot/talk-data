# Physical AI Loop violation breakdown metrics — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（合成デモ。実機検証完了は主張しない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `8903a7a`

## 実装

- `LoopMetrics` に `violationBreakdown` を追加し、speed / clearance / human distance などの違反内訳を構造化。
- `MetricsComparison` に `violationReductionPct` と `clearanceImprovementPct` を追加。
- UIに `Violation breakdown OFF/ON` と `Causal improvement signal` panelを追加。
- Incident reportにも violation reduction / clearance improvement を追記。

## 検証

- `npm test`: 13/13 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `Violation breakdown OFF` / `Causal improvement signal` / `Violation reduction` が含まれることを確認

## 非主張

- 改善率は合成リプレイ上のデモ指標であり、実機安全保証ではない。

