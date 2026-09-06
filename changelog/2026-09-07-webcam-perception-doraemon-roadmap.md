# Webcam動画処理のDoraemon段階開発記録

日付: 2026-09-07 JST  
区分: 実装記録・引き継ぎ（Canonical Decisionではない）

## 対象

webcamからの動画入力を、単発フレーム処理から、時系列理解・予測・同意付き記憶・根拠付き対話へ順番に拡張する開発系列。Doraemon級は完成済みという意味ではなく、将来の知覚・対話・行動系へ拡張可能な段階を指す作業目標である。

## 実装本体

- リポジトリ: https://github.com/qooyanz-bot/perception-mvp
- 保存コミット: `58646bd` (`feat: extend webcam perception toward Doraemon roadmap`)
- 検証: Python 3.13 / `pytest` 198 passed
- `numpy` は速度ベースラインの開発依存として導入した。OpenCVは任意依存で、未導入時も純Pythonの契約・replay経路は利用可能。

## これまでの系列

1. Phase 0-4: 契約、geometry gate、failure catalog、dual ledger/replay、監査とK-reviewの基盤。
2. Phase 5-12: 実データadapter、F-004〜F-010のmicro-loop、ops dashboard、public mini sample ingest。
3. Phase 13-19: critic review、regression harness、週次Markdown report、performance/speed baseline、公開データ取込の検証。
4. Stage 20: bounded webcam queue、drop-oldest、JSONL録画/replay、source→contract processor→session bridge、FPS/jitter/gap/out-of-order health、frame brightness/contrast/sharpness quality。
5. Stage 21: canonical temporal tracker、continuity、bounded history、replay可能なtrack snapshot。
6. Stage 22: moving/stationary、entering/leaving、near relation等のevidence付きscene event。
7. Stage 23: constant-velocity短期予測、TTC、単体risk、pairwise closest approach、geometry/sync不良時のuncertainty。
8. Stage 24: 明示的consentを要求するbounded memory、subject検索・summary・revoke消去・JSONL persistence・audit。
9. Stage 25: evidence-grounded assistant response、proactive attention cue、permission gate、session artifactからの質問応答、VLM backend protocol。

## 現在の境界

- webcam画像からの本物のlearned detectorは未統合。`WebcamContractProcessor` は backend-neutral detector境界と health/latency/failureを提供するが、実運用モデルの精度を証明しない。
- learned multi-object association、遮蔽復帰、action/event classifierは未完成。
- 予測は線形baselineであり、calibrated learned forecastingではない。
- 長期記憶はboundedかつ明示consent前提。本人確認、暗号化、UI、削除の実運用統合は未完成。
- VLMはprotocol/backend seamまでで、外部モデル・tool/action adapterの実接続は未完成。
- raw webcam payloadを正本に保存しない。監査・replayに必要な最小成果物だけを保存する。

## 正本運用

この文書は実装状態の記録であり、Future ConceptやKの最終判断を単独で確定しない。新しい仕様は、提案→草案→E系/B5短点検→K承認→commit→changelog→版更新の順で扱う。秘密、未観測の確定偽証、AI単独のFuture Concept最終決定は記録しない。

