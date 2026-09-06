# Address Reference Runtime v0.1

依存ライブラリを使わず、`Addressable Concept Architecture v0.1` の最小安全不変条件を検査する参照実装である。

## 対象

- required field、型、最小のConcept / Dimension分離、系譜ハッシュ
- malformed inputの安全な拒否。境界検査は例外停止ではなく `INVALID` を返す。
- `world_id`、Memory / Capability scope、Evidence / Law contract、残差のabstain表現
- real worldでの公開・許可済みread/verify scope以外の拒否
- canonical JSONからの安定した `address_id` 再計算
- Evidence Contractの共通authority / generator / semantic law検出。path IDだけの相違は独立性と扱わない。
- Resolution Gateによる `READY_FOR_VERIFICATION` / `ABSTAIN` 判定。証拠不足、共通原因、鮮度切れ、矛盾ではValueを返さない。
- content-addressed Audit Log。Valueやassertion本文を保存せず、Address・証拠digest・判定を再検算可能にする。
- Replay Verifier。保存済み監査ログに対して同じAddress・Evidence・時刻でGateを再実行し、判断と系譜の完全一致を検証する。
- Protocol Claim Gate。凍結・未実行・監査未完了のProtocolから、実験結果又は能力を主張することを防ぐ。

## 非対象

- Valueの発見、現実の秘密・個人情報・未来値の取得
- Address Lawの自動発見、暗号又は認証の回避
- R6-Gの実装、実験、Holdoutの開封又は実行

## 実行

```text
python -m unittest discover -s address/reference-runtime-v0.1/tests -v
python address/reference-runtime-v0.1/address_runtime.py address/reference-runtime-v0.1/fixtures/valid_synthetic_address.json
```

結果は `VALID`、又は機械可読な `INVALID` と違反一覧で返す。
