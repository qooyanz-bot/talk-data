# Address reference-runtime 引き継ぎ — Codex Desktop（2026-09-06 続続）

- 作成: 2026-09-06（前回 handoff `2026-09-06-address-reference-runtime-codex-handoff.md` の続編）
- 依頼者: K（承認者 / Future Concept Designer）
- 正本: https://github.com/qooyanz-bot/talk-data
- 現行 HEAD（確認済み・push済み）: `3d8068225092e6735cf64a3e071c64b6461c51de`
- 現行 commit: `feat(address): contradiction_policy closed enum & evidence_contract frozensets`
- CI 対象ワークフロー: `.github/workflows/address-reference-runtime.yml`
- ローカル clone（Windows）: `C:\Users\qooya\Documents\Codex\2026-09-06\2-address-text-address-theory-addressable\work\talk-data`
- Python: `C:\Users\qooya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- git identity（repo-local）: `qooyanz-bot <qooyanz@gmail.com>`

## 役割

- K = 承認者 / Future Concept Designer（最終 Future Concept 決定は K）
- 実装者 = Adviser / Researcher / Critic / Calculator / Recorder / Verifier
- 単独で Future Concept 最終決定をしない

## 絶対禁止（技術事実として書かない / 実装しない / 主張しない）

- 宇宙全体がデータベースである
- 任意の現実の秘密値を読み取れる / 実在人物の隠れた情報を確定できる
- 宇宙や別次元からの介入
- 未来の結果を直接取得できる
- Address理論が暗号や認証を破れる
- R6-G を実行したと主張する / Holdout を開封・実行する
- value を埋めて成功扱いにする（成功しても `value=null`、`READY_FOR_VERIFICATION`）
- force-push
- 推測で過去会話や repo を再構成する

## 現状（GitHub で直接確認済み）

- repo: `qooyanz-bot/talk-data` branch `main`
- HEAD: `3d80682`
- tests at HEAD: **281** 件 OK（`python -m unittest discover -s address/reference-runtime-v0.1/tests -v`）
- `address_cli.py --conformance` → `status: CONFORMANT`（exit 0）
- `address_cli.py --runtime-manifest` → `status: RUNTIME_MANIFEST`（exit 0）
- `tools/regenerate_all_frozen_docs.py --check` → limitations / conformance / runtime_manifest 全て ok（exit 0）
- working tree clean（push済み）

### 実装済み runtime（`address/reference-runtime-v0.1/`）

| 面 | 要点 |
|---|---|
| address_runtime | schema/types、SYNTHETIC_ONLY（`world:real:` 拒否）、canonical_dumps、`CONTRADICTION_POLICY_ALLOWED` 閉集合、frozenset 定数 |
| evidence_contract | 共通原因、independence 閉集合、AUDITED は外部 audit、`REQUIRED_FIELDS`/`INDEPENDENCE_AXES` frozenset |
| resolution_gate | ABSTAIN / READY、residual、REASON_ALLOWED / DECISION_ALLOWED 閉集合 |
| audit_log | value-free content-addressed、`SCHEMA_VERSION`/`REQUIRED_KEYS` export、decision/reason 閉集合 verify |
| replay_verifier | REPLAY_STATUS_ALLOWED 閉集合 |
| protocol_claim_gate | validate_manifest 閉集合、claim_type/reason/status 閉集合 |
| decision_log | content-addressed decision_log_id、`REQUIRED_KEYS` export |
| response_contract | 公開契約、value=null、`DECISION_LOG_REQUIRED_KEYS` を decision_log から単一正本化 |
| limitations | SYNTHETIC_ONLY / NOT_RUN / FORBIDDEN 面 |
| conformance | LIMITATIONS + synthetic battery + R6-G NOT_RUN 集約、`CHECK_IDS_ALLOWED`/`CHECK_STATUSES_ALLOWED` 閉集合 export |
| runtime_manifest | 凍結ファイル一覧 + `package_digest()` → sha256、`--runtime-manifest` CLI、fixtures/regenerator/CI 統合 |
| CLI | resolve / `--check-contract-only` / `--verify-decision-log` / `--verify-audit-log` / `--validate-protocol-manifest` / `--conformance` / `--runtime-manifest` |
| tools | regenerate limitations/conformance/contract goldens/runtime_manifest、`--check` drift |

## 最近のコミット履歴（昇順）

```text
cb00261 feat(address): runtime_manifest content-hash helper & conformance checks single-source
3fd61f2 feat(address): audit_log closed enum verification & CLI --verify-audit-log
3d80682 feat(address): contradiction_policy closed enum & evidence_contract frozensets
```

## 完了している増分

1. **RUNTIME_MANIFEST content-hash helper**（`runtime_manifest.py` 新規、`package_digest()`、CLI `--runtime-manifest`、fixtures/regenerator/CI）
2. **conformance.CHECK_IDS_ALLOWED / CHECK_STATUSES_ALLOWED** を `conformance.py` から export（tests と単一ソース）
3. **audit_log 閉集合検証**（`SCHEMA_VERSION`/`REQUIRED_KEYS` export、decision/reason 閉集合 verify）＋ CLI `--verify-audit-log`
4. **`response_contract.DECISION_LOG_REQUIRED_KEYS`** を `decision_log.REQUIRED_KEYS` から単一正本参照
5. **`address_runtime.CONTRADICTION_POLICY_ALLOWED`** 閉集合 enum を export し `validate()` で適用
6. **frozenset 定数硬化**: address_runtime の `REQUIRED_FIELDS`/`DIMENSIONS`/`REAL_CAPABILITIES`/`FORBIDDEN_CAPABILITY_TOKENS`、evidence_contract の `REQUIRED_FIELDS`/`INDEPENDENCE_AXES`

## 次に推奨される増分（この順で自律継続可）

各増分: 不変条件→unittest 全緑→changelog→commit→push→CI 確認→次へ。ゴール完了扱いで止めない。ただし Future Concept 最終は K 待ち。

1. **`decision_log.REQUIRED_KEYS` など残存ハードコードの単一正本化**（response_contract は済。他 module の `{}` set→frozenset 定数 export の残りを洗い出す）
2. **`resolution_gate` の decision/reason 語彙と response_contract の実一致テスト強化**（既にエイリアス。共有同一性 `is` を単一の module で全チェック）
3. **CLI のエラー詳細・終了コードの統一**（例: `--verify-audit-log` など standalone の組み合わせを一覧テストで固定）
4. **frozen API サーフェス**（公開関数・定数・CLI フラグのスナップショット）を共通の列出力として凍結する helper（`conformance.py` と同系の解説・検証 runner）
5. **構成ドキュメントの一括同期**: 実装済み項目を `address/reference-runtime-v0.1/README.md` / root `README.md` / `CHANGELOG.md` で過不足なく反映

実装前に必ず `git pull --rebase origin main` してから確認し、remote が進んでいたら rebase。

## 検証コマンド（各増分の最後に必ず実行）

```text
git fetch origin
git checkout main
git pull --rebase origin main
git rev-parse HEAD
python -m unittest discover -s address/reference-runtime-v0.1/tests -v
python address/reference-runtime-v0.1/address_cli.py --conformance
python address/reference-runtime-v0.1/address_cli.py --runtime-manifest
python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check
```

Windows では storefront python ではなく上記 Codex runtime python を使う。

## 自己点検

- E系: 外部接続・秘密・認証回避・個人の隠れた情報・未来値取得を実装しない
- B5: Future Concept の最終決定は行わない