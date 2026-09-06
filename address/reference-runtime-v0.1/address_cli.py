"""Single read-only CLI entrypoint for Address resolution and audit/replay verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import audit_log
import protocol_claim_gate
import replay_verifier
import response_contract
import resolution_gate


def evaluate(
    address: dict[str, Any],
    evidence: list[dict[str, Any]],
    now: str,
    audit: dict[str, Any] | None = None,
    protocol_manifest: dict[str, Any] | None = None,
    claim_type: str | None = None,
) -> dict[str, Any]:
    """Return a resolution plus a value-free generated audit record."""
    outcome = resolution_gate.resolve(address, evidence, now)
    generated_audit = audit_log.create(address, evidence, outcome, now) if isinstance(address, dict) and isinstance(outcome, dict) else None
    result: dict[str, Any] = {"resolution": outcome, "generated_audit": generated_audit}
    if audit is not None:
        result["replay"] = replay_verifier.verify_replay(address, evidence, audit)
    if protocol_manifest is not None or claim_type is not None:
        result["protocol_claim"] = protocol_claim_gate.assess_claim(protocol_manifest, claim_type if isinstance(claim_type, str) else "")
    errors = response_contract.validate(result)
    if errors:
        raise RuntimeError("response contract violation: " + "; ".join(errors))
    return result


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Address resolution and replay verifier")
    parser.add_argument("address", help="Address JSON path")
    parser.add_argument("evidence", help="Evidence bundle JSON path")
    parser.add_argument("--now", required=True, help="Evaluation time in ISO-8601 UTC")
    parser.add_argument("--audit", help="Optional prior audit JSON to replay")
    parser.add_argument("--protocol-manifest", help="Optional protocol manifest JSON for claim gating")
    parser.add_argument("--claim-type", help="Claim type to assess against the protocol manifest")
    args = parser.parse_args()
    try:
        result = evaluate(
            _load(args.address),
            _load(args.evidence),
            args.now,
            _load(args.audit) if args.audit else None,
            _load(args.protocol_manifest) if args.protocol_manifest else None,
            args.claim_type,
        )
    except (OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
