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

## 追加進捗

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/ac3f3dd`
- `learning/action_recognition.py` に、ラベル付き特徴からクラス別prototypeを学習し、confidence・距離・confusion・JSON persistenceを出す依存軽量baselineを追加。
- `EventSemanticsEngine` へ任意接続し、初回検出を含む `action:*` eventをtrack/timestamp evidence付きで出力。
- 検証: 全 200 テスト成功。これは動画モデルの実環境精度を意味せず、学習済みaction認識へ置換・評価するための測定可能な接続点である。

## 実 detector 接続

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/1318d8b`
- `OpenCVHOGPersonDetector` を追加。JPEG bytesをOpenCVでdecodeし、既成HOG person detectorから人物bbox・confidence・簡易ID継続を返す。
- 2D pixel bboxを3D metricとして偽装しないため、`geometry_valid=false` と NaN metric値を使用。既存の geometry/sync gate により train-eligible にはならない。
- OpenCVは任意依存で、backend境界に分離。fake moduleによる実経路テストを含む全 202 テスト成功。
- 未完成: multi-class learned detector、実機条件での精度評価、モデル重みlineage、遮蔽復帰。

## ONNX detector 実行境界

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/165037d`
- `OnnxWebcamDetectorBackend` を追加。JPEG decode、resize、RGB/CHW/float32正規化、ONNX session実行、明示parser、score thresholdを実装。
- モデルごとに異なる出力tensorを暗黙解釈せず、parser callbackを必須化。`model_id`・任意digest・入力サイズ・閾値をlineageとしてlive成果物へ出力。
- fake session/OpenCVを用いた実行経路テストを追加し、全 204 テスト成功。
- 未完成: 実ONNX重み、multi-class parserの実データ精度、OpenCV/ONNX Runtimeの実機測定。

## multi-class parser

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/0673437`
- YOLOv8-style raw tensor（`cx, cy, w, h, class scores`）のmulti-class parserを追加。
- 元画像への座標復元、score threshold、class-aware NMS、未知class vocabulary拒否を実装。
- 出力は2D bboxのみとし、未校正の3D geometryはNaN・invalidのまま保持。合成出力で重複抑制とclass分離を検証。
- 検証: 全 206 テスト成功。未完成: 実ONNX重みとの接続、実webcam条件の精度/速度評価、学習済みtracking。

## detector ID assignment

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/0d2581d`
- `BboxTrackAssigner` を追加し、multi-class bboxのclass一致・中心距離・bounded missed framesでフレーム間IDを再割当。
- YOLO parserの `yolo-pending-*` を downstream の temporal tracking に接続可能な安定IDへ変換。appearance re-IDや本格的遮蔽復帰は未実装。
- lineageへ `track_assigner=nearest_center_v0` を追加し、全 207 テスト成功。

## 遮蔽復帰 telemetry

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/b726fa9`
- bbox ID assigner が欠落後の同一ID復帰を `occluded=true` として出力し、`occlusion_recoveries`、`track_expirations`、`active_tracks` を health に記録。
- live source の health serializer を dataclass/dict両対応に修正し、実際のsession成果物まで回帰。
- 検証: 全 209 テスト成功。これはappearance re-IDや完全な遮蔽理解ではなく、距離ベース復帰のbaselineである。

## temporal action baseline

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/d8998e4`
- trackerのbounded historyから速度系列を公開し、平均・最大・初終差・age・missedをtemporal featureとしてaction recognizerへ接続。
- feature schemaを明示した場合だけ `EventSemanticsEngine` が時間窓を使用。従来の単フレーム動作は維持。
- 検証: 全 211 テスト成功。現状はprototype baselineであり、RGB clip encoderや実動画データでの一般化は未検証。

## RGB clip feature encoder

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/d6dee06`
- RGB frame sequenceから平均RGB、frame-to-frame motion energy、brightness deltaを抽出し、clip単位の evidence-aware action predictionへ接続。
- 同一shape検証、finite値検証、空clip拒否を実装。3D CNNや実動画モデルの精度とは区別する。
- 検証: 全 214 テスト成功。未完成: RGB clip encoderの実学習、長時間clip sampling、実webcam条件の精度評価。

## sliding clip sampler

- 追加コミット: `https://github.com/qooyanz-bot/perception-mvp/commit/6bb18ea`
- live/replay webcam streamから固定長 `clip_size` と `stride` の決定的なclip窓を生成。
- clip成果物にはwindow ID、frame IDs、開始/終了timestamp、sourceのみ保存し、raw payloadは保存しない。
- 検証: 全 215 テスト成功。未完成: 長時間clipのモデル推論、実webcam条件のsampling/latency評価。

## 現在の境界

- webcam画像からの本物のlearned detectorは未統合。`WebcamContractProcessor` は backend-neutral detector境界と health/latency/failureを提供するが、実運用モデルの精度を証明しない。
- learned multi-object association、遮蔽復帰、action/event classifierは未完成。
- 予測は線形baselineであり、calibrated learned forecastingではない。
- 長期記憶はboundedかつ明示consent前提。本人確認、暗号化、UI、削除の実運用統合は未完成。
- VLMはprotocol/backend seamまでで、外部モデル・tool/action adapterの実接続は未完成。
- raw webcam payloadを正本に保存しない。監査・replayに必要な最小成果物だけを保存する。

## 正本運用

この文書は実装状態の記録であり、Future ConceptやKの最終判断を単独で確定しない。新しい仕様は、提案→草案→E系/B5短点検→K承認→commit→changelog→版更新の順で扱う。秘密、未観測の確定偽証、AI単独のFuture Concept最終決定は記録しない。

