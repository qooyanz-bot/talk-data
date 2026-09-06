# Physical AI Loop P0 デモ実装進捗 — 2026-09-07

- 文書種別: implementation progress / changelog
- 版: v0.1
- 状態: 実装事実の記録（「最後のドラえもん級完成」は主張しない）
- 正本: https://github.com/qooyanz-bot/talk-data
- 実装パス: `Documents/Codex/2026-09-07/https-herp-careers-v1-newmo-requisition/work/cortext9-physical-ai-loop`

## 1. 観測事実（実装）

1. `lib/loop/` に純関数の P0 ループを追加した:
   - `extractHazardSegments` / `selectPrimarySegment`
   - `applySafetyFilter` / `buildReplay`
   - `computeMetrics` / `compareMetrics`
   - `generateNextTasks`
   - `runImprovementLoop`
2. 合成失敗ログ 2 本（AMR human near-miss、vehicle clearance drop）を fixture 化した。いずれも `synthetic: true`。
3. `app/page.tsx` をデモ UI に置換: ログ選択、hazard 一覧、Filter OFF/ON、before/after 軌道と指標、next tasks、合成デモ disclaimer。
4. `tests/loop.test.ts` を追加。`npm test` で shipped 関数を直接実行し、OFF の違反数が ON より多いこと、ON の min clearance が OFF より大きいこと、next tasks が非空であることを assert。
5. README に「synthetic demo / not real-robot verified / not completed Doraemon-class product」を明記。

## 2. 非主張

- 実機検証完了ではない。
- Future Concept / H1 の最終確定ではない。
- 「最後のドラえもん級」完成を主張しない（本ゴールの gating は P0 デモ）。

## 3. 次

- P1: Data Quality Autopilot / Semantic Perception / Autonomy Debugger
- 専用 GitHub リポ分離（任意）
- 実ログ接続は別ゲート


## 4. Verification evidence (same day)

- `npm test` twice: 7/7 pass (scratch `loop-unit-tests.log`, `loop-unit-tests-rerun.log`).
- `npm run build` exit 0 (`build.log`).
- `npm run dev` first launch + stop/relaunch both HTTP 200 with Filter OFF/ON, log-select, before/after metrics present.
- No interactive headless browser MCP; used HTTP + source control presence fallback (`browser-unavailable.log`, `source-controls-check.log`).
- Local demo git commit `4214e51`. Private GitHub create via integration returned 403.

---
記録日: 2026-09-07 JST
記録者役割: AI Recorder / Implementer（Grok）
