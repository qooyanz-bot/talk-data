# Benchmark Program Conversation Record

- Date: 2026-09-07 JST
- Classification: Raw-derived handoff record and research status
- Canonical repository: https://github.com/qooyanz-bot/talk-data
- Scope: The benchmark-program conversation available in this Codex task

## User intent

The user first asked for ideas that combine Address theory, a Universe DB, and
other principles to target first place on Hugging Face benchmarks. The user
then clarified that the target did not need to be an LLM benchmark: any
Hugging Face benchmark where a combined principle could plausibly reach first
place was acceptable.

The selected program is a sequence of five non-LLM-focused tracks:

1. FFASR: far-field speech recognition.
2. TabArena: tabular machine learning.
3. CADGenBench: text/image to valid 3D CAD.
4. PazaBench: low-resource-language ASR.
5. MTEB: embedding evaluation on a named non-LLM task.

The operating objective became: develop each track in order and continue until
a first-place result is actually verified. A local score or a plausible design
is not first place.

## Benchmark research recorded in the conversation

### FFASR

The Hugging Face FFASR Space evaluates far-field ASR under near-field, measured
and simulated room, high/mid/low SNR, and moving-source conditions. It reports
WER per condition, average WER, RTFx, and parameter count. Its default ranking
uses the average of dry, high-SNR, mid-SNR, and low-SNR WER. The held-out audio
is private and submissions can provide a model ID and custom evaluation code.

Source: https://huggingface.co/spaces/treble-technologies/ffasr

### TabArena

TabArena ranks tabular ML systems using Elo and publishes per-dataset results.
It has pools for individual models, open systems, LLM systems, API systems,
and combinations of those categories. The public Space documents CSV artifacts
and JSON endpoints.

Source: https://huggingface.co/spaces/TabArena/leaderboard

### CADGenBench

CADGenBench evaluates whether a system can turn a textual or visual description
of a mechanical part into a valid, geometrically correct 3D model. The Space
accepts STEP/BREP candidates and runs automatic evaluation against a private
test set.

Source: https://huggingface.co/spaces/HuggingAI4Engineering/CADGenBench

### PazaBench

PazaBench is a low-resource ASR leaderboard covering 61 African languages in
the cited release. It reports CER, WER, and RTFx.

Source: https://huggingface.co/spaces/microsoft/paza-bench

### MTEB

MTEB evaluates embedding systems across retrieval, classification, clustering,
and similarity tasks, including text, image, audio, and video modalities. The
program targets a named Japanese or domain-specific task rather than claiming
an unverified overall rank.

Source: https://huggingface.co/spaces/mteb/leaderboard

## Implemented local artifacts

The following artifacts were created in the Codex worktree. They were not
automatically copied into this canonical repository in this change; the paths
are recorded so the next agent can package them into the appropriate project
repository after review.

- `work/ffasr_address/`: acoustic Address extraction, route selection, ASR
  inference wrapper, and submission hook.
- `work/tabarena_address/`: Dataset Address extraction and deterministic recipe
  router.
- `work/cadgenbench_address/`: constrained plate-like STEP generator and
  solid/volume verifier using CadQuery.
- `work/pazabench_address/`: conservative public-lexicon transcript correction
  with an audit log.
- `work/mteb_address/`: observable concept-address prefixing and a
  Transformers mean-pooling encoder.
- `work/BENCHMARK_PROGRAM.md`: benchmark order, evidence rules, and leakage
  boundaries.

## Verification evidence

- All available source files compiled with Python `compileall`.
- FFASR Address smoke test passed on synthetic NumPy audio.
- CAD prompt parser smoke test passed for dimensions and four holes.
- PazaBench correction smoke test passed with an auditable replacement log.
- MTEB Address extraction smoke test passed.
- TabArena Dataset Address smoke test passed on a small pandas frame.
- Python 3.12 and CPU PyTorch 2.14.0 were installed locally.

## Unresolved status

- No track has a verified Hugging Face first-place result.
- No HF authentication token was present in the environment.
- MTEB model inference encountered tokenizer incompatibility with the selected
  tiny checkpoint; this is an execution issue, not a benchmark result.
- The local prototypes are baselines and must not be described as leaderboard
  winners.

## Safe interpretation of the principles

Address means a measurable coordinate of an input, acoustic condition, dataset
regime, geometric constraint, language/entity context, or embedding task state.
Universe DB means a provenance-tracked store of public development data, prior
results, failure cases, validated transformations, and verification rules. It
must never contain private test data or be used to infer hidden test answers.

