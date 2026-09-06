<!--
title: "Address runtime_manifest content-hash helper & conformance check_ids export"
date: "2026-09-06"
-->

# Address reference-runtime: runtime_manifest content-hash helper & conformance checks single-source

- `runtime_manifest.py`: 凍結ファイル一覧（12モジュール）のLF正規化SHA-256およびパッケージダイジェスト（`package_digest()` → `sha256:<64 hex>`）を生成・検証するヘルパーを実装。
- Address `lineage.runtime_sha` から引用可能な実装ダイジェストとして文書化（全Addressに強制せず、null許可は維持）。
- CLI `--runtime-manifest` フラグを追加（他standaloneモードと相互排他、exit 0）。
- `fixtures/runtime_manifest.json` および再生成ツール `tools/regenerate_runtime_manifest.py` を追加、`tools/regenerate_all_frozen_docs.py` へ統合。
- `conformance.py`: `CHECK_IDS_ALLOWED` および `CHECK_STATUSES_ALLOWED` 閉集合frozensetを単一正本としてexportし、テスト内ハードコードと統合。
- CIワークフローへ `--runtime-manifest` 実行を追加。
