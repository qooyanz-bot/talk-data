# Benchmark Program Progress 02

- Date: 2026-09-07 JST
- Classification: Research evidence summary; not a canonical victory claim
- Related record: `archives/2026-09-07/benchmark-program-conversation.md`

## Observed local evidence

- FFASR public proxy, `openai/whisper-tiny`, one public dummy utterance:
  - fixed baseline Avg WER: 535.2941 percent
  - Address-routed Avg WER: 67.6471 percent
  - fixed baseline proxy RTFx: 0.5458
  - Address-routed proxy RTFx: 2.3514
  - this is synthetic/public development evidence and is not an official
    FFASR score.
- TabArena public `breast_cancer` smoke evaluation:
  - selected candidate: LightGBM
  - local ROC-AUC: 0.9944569
  - three-fold run had no recorded errors
  - this is not a remote TabArena Elo result.
- CADGenBench local test suite:
  - 3 tests passed
  - generated STEP candidates were verified for non-empty, positive-volume
    solids using the local faceted STEP backend.
- PazaBench synthetic lexicon smoke evaluation:
  - 10 samples across `swa`, `kik`, and `luo`
  - CER: 25.3521 percent before correction, 0 after correction
  - WER: 100 percent before correction, 0 after correction
  - synthetic aliases only; not an official PazaBench result.

## Current official comparison

The locally saved FFASR leaderboard snapshot lists `zhifeixie/Mega-ASR` at rank
1 with Avg WER 13.38 percent and `Qwen/Qwen3-ASR-1.7B` at rank 2 with Avg WER
13.41 percent. The local proxy numbers above are not comparable to this private
test result.

Source: https://huggingface.co/spaces/treble-technologies/ffasr

## Submission state

The FFASR submission helper passed dry-run validation for
`Qwen/Qwen3-ASR-1.7B` and a 9,828-character custom evaluator. A live submission
was not made because no `HF_TOKEN` was available in the environment. No
first-place claim is made.

