# Changelog

## 2026-09-06 (Historical Raw Archive documentation)
- READMEに `archives/md-original/` の目的、利用上の正本性区分、安全な参照手順を追加。
- Raw Archiveを承認済み判断・再現可能なEvidence・未検証仮説と混同しないこと、秘密情報の再記録・復元をしないことを明記。

## 2026-09-06 (Address reference runtime v0.1)
- Address Runtimeの型・時間・scope境界を強化。malformed inputを例外停止せず `INVALID` として返し、時間逆転、真偽値threshold、非JSON値などを拒否する。
- Replay Verifierを追加。保存された監査ログを自己ハッシュだけでなく、同一Address・Evidence・時刻でGateを再実行して検証する。入力、系譜、判断の不一致を検出する。
- content-addressed Audit Logを追加。値とassertion本文を記録せず、Address ID、証拠digest、判定、時刻から再計算可能な監査IDを生成・検証する。
- Resolution Gateを追加。Address・Evidence Contract・鮮度・assertion矛盾を統合し、失敗時はすべて `ABSTAIN` と `value=null` を返す。
- Evidence Contract evaluatorを追加。authority、generator、semantic lawの共有を検出し、別pathでも独立性とは認定しない。metadata分離を通過しても `CONTRACTED` とし、semantic independenceの監査済み主張はしない。
- Addressable Concept Architecture v0.1 の最小安全不変条件を検査する依存なしの参照実装、fixture、unittestを `address/reference-runtime-v0.1/` に追加。秘密・認証回避・直接未来取得を含むscope、hash不整合、abstain不備を拒否する。

## 2026-09-06 (Addressable Concept Architecture v0.1)
- K承認により、検証可能なAddress SchemaとEvidence境界を `address/addressable-concept-architecture-v0.1.md` に追加。R6-G未実行、既存結果のsynthetic限定性、Law不確実時のabstain要件を明記。

## 2026-09-06 (ChatGPT export archive)
- 380会話・17,957メッセージの公開用会話アーカイブを `archives/2026-09-06/` に追加。秘密形式・メール・電話番号を不可逆に置換し、原本HTML・添付本体・セッションIDは含めない。分析は草案であり、会話内容を正本の決定として自動採用しない。
- 同じ会話を `archives/md-original/` に日付順・1会話1Markdownとして追加。会話内容由来の題名とし、公開安全の伏せ字以外の本文を保全する。

## 2026-09-05 (Cortext9 units v0.4)
- 圧勝単位をさらに細分化。v0.3の359から拡張（薄い安全系ドメインの子＋N151–N212）。カタログ `future-concept/Cortext9-unit-catalog-v0.4.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.4-addendum.md`。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05 (Cortext9 units v0.3)
- 圧勝単位をさらに細分化。v0.2の218から拡張（N51–N90の子＋N91–N150系、writing/life_safe/ml_ops運用単位）。カタログ `future-concept/Cortext9-unit-catalog-v0.3.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.3-addendum.md`。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05 (Cortext9 units v0.2)
- 圧勝単位をさらに細分化。v0.1の102から拡張（N19–N50の子ID＋N51–N90系）。カタログ `future-concept/Cortext9-unit-catalog-v0.2.json`、追記 `future-concept/Cortext9-unit-api-schema-v0.2-addendum.md`。ml_ops（振り分け・評価・拒否ゴールデン）追加。断定の医療・法律・軍事は引き続き禁止。

## 2026-09-05
- Cortext9 圧勝単位を細分化（N01–N18 の子ID＋N19–N50）。カタログ `future-concept/Cortext9-unit-catalog-v0.1.json`、追記スキーマ `future-concept/Cortext9-unit-api-schema-v0.1-addendum.md`。非断定の安全単位 N43–N46 を追加。断定の医療・法律・軍事は引き続き禁止。
