# Benchmark Program Progress 03

Date: 2026-09-07 JST
Status: observed development progress; no official first-place claim

## Observed

- CADGenBench local smoke: 3 tests passed.
- PazaBench local synthetic smoke: 10 samples; CER 25.35% -> 0.00%, WER 100.00% -> 0.00%. This is synthetic development evidence, not an official leaderboard result.
- TabArena local runner help and prior local smoke artifacts remain available. The observed local selections are not official ranking evidence.
- MTEB Address package now has a working `mteb_address.encode` CLI entry point. Help, `compileall`, and Address extraction smoke checks passed. No official MTEB score has been produced.
- FFASR local proxy recheck remains: `openai/whisper-tiny`, one public LibriSpeech dummy utterance, seed 7, baseline average WER 535.29% and Address-routed average WER 67.65%; RTFx proxy 0.55 -> 2.35.
- A separate FFASR seed 13 process reached model initialization but terminated without writing a result JSON. It is not evidence of improvement or failure on the benchmark.

## Interpretation

Address routing is a plausible intervention for the local proxy, but the current evidence is too small and synthetic to support an official rank claim. The next gate is broader public-data validation, followed by an authenticated official submission only after K approves the exact payload and contact information.

## Reproduction pointers

- `work/ffasr_address/results/local_eval_recheck.json`
- `work/pazabench_address/results/smoke_recheck/latest_local.json`
- `work/cadgenbench_address/tests/test_smoke.py`
- `work/mteb_address/src/mteb_address/encode.py`
