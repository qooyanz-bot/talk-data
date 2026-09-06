# Physical AI Loop replay inspector — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（合成デモ。実機検証完了は主張しない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `1da6c4f`

## 実装

- UIに `Replay inspector` panelを追加。
- 選択フレームごとに raw model action、shielded action、semantic state、risk、constraint violationsを表示できるようにした。
- 面談中に「この時刻で何を補正したか」を説明しやすい状態にした。

## 検証

- `npm test`: 13/13 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `Replay inspector` / `Raw model action` / `Shielded action` / `Frame decision` が含まれることを確認

## 非主張

- replay inspectorは合成リプレイの説明UIであり、実機ログの完全な物理再現を主張しない。

