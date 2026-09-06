# Address reference-runtime 引き継ぎ — Codex Desktop

- 作成: 2026-09-06
- 依頼者: K（承認者 / Future Concept Designer）
- 正本: https://github.com/qooyanz-bot/talk-data
- 起点 HEAD（確認済み）: `468ca9b91da6f9cc3d5b4172bb68ec2d5a40abe8`
- 起点 commit: `feat(address): evidence_contract status closed enum single-source`
- 起点 CI: success — https://github.com/qooyanz-bot/talk-data/actions/runs/34021313012
- ローカル clone（Windows）: `C:\Users\qooya\Documents\Codex\2026-09-06\2-address-text-address-theory-addressable\work\talk-data`
- Python: `C:\Users\qooya\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- git identity（repo-local）: `qooyanz-bot <qooyanz@gmail.com>`

## 役割

- K = 承認者 / Future Concept Designer（最終 Future Concept 決定は K）
- 実装者 = Adviser / Researcher / Critic / Calculator / Recorder / Verifier
- 単独で Future Concept 最終決定をしない
- この作業は Address reference-runtime の実装検証ループとして継続してよい

## 絶対禁止（技術事実として書かない / 実装しない）

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

### 正本

- repo: `qooyanz-bot/talk-data` branch `main`
- HEAD: `468ca9b`
- tests at HEAD: **260** OK（unittest discover）
- CI workflow: `.github/workflows/address-reference-runtime.yml`
  - unittest
  - `python address/reference-runtime-v0.1/address_cli.py --conformance`
  - `python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check`

### 実装済み runtime（`address/reference-runtime-v0.1/`）

| 面 | 要点 |
|---|---|
| address_runtime | schema/hash/types、SYNTHETIC_ONLY（`world:real:` 拒否）、canonical_dumps |
| evidence_contract | 共通原因、independence 閉集合、status 閉集合、AUDITED は外部 audit |
| resolution_gate | ABSTAIN / READY、residual、REASON_ALLOWED / DECISION_ALLOWED |
| audit_log | value-free content-addressed、malformed reject、digest 共有 |
| replay_verifier | REPLAY_STATUS_ALLOWED |
| protocol_claim_gate | validate_manifest 閉集合、claim_type/reason/status 閉集合 |
| decision_log | content-addressed decision_log_id、語彙 Mirror |
| response_contract | 公開契約、value=null、語彙 alias |
| limitations | SYNTHETIC_ONLY / NOT_RUN / FORBIDDEN 面 |
| conformance | LIMITATIONS + synthetic battery + R6-G NOT_RUN 集約 |
| CLI | resolve / --check-contract-only / --limitations / --validate-protocol-manifest / --verify-decision-log / --conformance |
| tools | regenerate limitations/conformance/contract goldens、`--check` drift |

### 関連確認対象（再推測禁止。git show / blob / tests を直接見る）

- Universe-data-analysis-project HEAD `60f40bf9dc4cd5f642eae24021c7afa3e80cee0b`
- LLMs-Research HEAD `33a17c99365d4a297e3953308bfd4daf3338f05e`
- R6-G: protocol frozen、experiment NOT_RUN、auditor pending、primary run unauthorized。Spec-only
- diagnostic address-identifiability-20260830-k7m2: DIAGNOSTIC_ONLY（path diversity ≠ semantic independence FALSIFIED）

## 未着手 / 次にやる増分（この順を推奨）

1. **RUNTIME_MANIFEST content-hash helper**（着手予定だったが未 push）
   - `runtime_manifest.py`: 凍結ファイル一覧 + `package_digest()` → `sha256:<hex>`
   - `lineage.runtime_sha` が引用可能な digest を文書化（全 Address に強制しない。null 許可は維持）
   - optional: `fixtures/runtime_manifest.json` + `--runtime-manifest` CLI + regenerator/`--check`
2. **conformance.CHECK_IDS_ALLOWED** を `conformance.py` から export（tests 内 REQUIRED_CHECK_IDS と単一ソース化）
3. 必要なら CI に `--runtime-manifest` 固定、または fixture equality

Future Concept 版管理・K 最終承認はコード増分ではなく K 判断。勝手に FC を確定しない。

## 完了条件（各増分）

1. 不変条件をコードに入れる
2. `python -m unittest discover -s address/reference-runtime-v0.1/tests -v` 全緑
3. changelog 更新（`changelog/2026-09-06-*.md` および必要なら root CHANGELOG / package README）
4. 意味のある commit message
5. `origin/main` へ push（force 禁止。remote が進んでいたら rebase）
6. GitHub Actions 再確認（unittest + conformance + regenerator --check）
7. 次の実検証可能な増分へ継続（ゴール完了扱いで止めない。ただし FC 最終は K）

## 検証コマンド

```text
git fetch origin
git checkout main
git pull --rebase origin main
git rev-parse HEAD
python -m unittest discover -s address/reference-runtime-v0.1/tests -v
python address/reference-runtime-v0.1/address_cli.py --conformance
python address/reference-runtime-v0.1/tools/regenerate_all_frozen_docs.py --check
```

Windows では storefront python ではなく上記 Codex runtime python を使う。

## 作業開始手順（Codex）

1. 上記 clone で `git pull --rebase origin main` し、HEAD が `468ca9b` かそれより新しいことを確認
2. もし `runtime_manifest.py` が既に main にあれば、重複実装せず次増分へ
3. 無ければ「未着手 1. RUNTIME_MANIFEST」から実装
4. テスト緑 → changelog → commit → push → CI 確認 → 次へ

## 自己点検

- E系: 外部接続・秘密・認証回避・個人の隠れた情報・未来値取得を実装しない
- B5: Future Concept の最終決定は行わない
