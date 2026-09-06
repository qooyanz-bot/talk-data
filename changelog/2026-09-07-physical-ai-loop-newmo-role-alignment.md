# Physical AI Loop newmo role alignment matrix — 2026-09-07

- 文書種別: implementation progress / changelog
- 状態: 実装事実の記録（公開求人からの推定。newmo内部確定要件ではない）
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`
- 実装コミット: `69bc46c`

## 実装

- `buildNewmoRoleAlignment` を追加。
- E2E/VLA autonomy、Perception、Closed-loop simulation、Control/safety、Data platform、Field integration の6領域に対し、score / demo evidence / reusable Cortext9 function を構造化。
- UIに `Role alignment` panelを追加し、newmo fitの理由を職種能力別に表示。
- Interview briefにも `Role alignment matrix` を追加。
- READMEに public-job inferred role alignment matrix を追記。

## 検証

- `npm test`: 15/15 pass
- `npm run build`: exit 0
- 既存 dev server `http://localhost:4173` で HTTP 200
- HTML応答内に `Role alignment` / `Public-job inferred fit` / `End-to-End / VLA autonomy` が含まれることを確認

## 非主張

- Role alignment は公開求人読解からの戦略推定であり、newmo内部の確定評価ではない。

