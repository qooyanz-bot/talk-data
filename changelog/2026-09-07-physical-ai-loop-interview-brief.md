# Physical AI Loop interview brief export — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（合成デモ。実機検証完了は主張しない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `ed1acf6`

## 実装

- `buildDemoBrief` を追加し、全サンプルログ横断の提出/面談用Markdown briefを生成できるようにした。
- brief には positioning、newmo fitの理由、AMR / vehicle / arm-mobile横断表、aggregate、6-step demo script、disclaimer を含める。
- UIに `Interview brief` panel と download button を追加した。

## 検証

- `npm test`: 13/13 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `Interview brief` / `cortext9-physical-ai-demo-brief.md` が含まれることを確認

## 非主張

- brief は採用面談/提出補助用であり、newmo内部の承認や評価を示すものではない。

