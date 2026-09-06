"""Single read-only CLI entrypoint for Address resolution and audit/replay verification."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import audit_log
import limitations
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
    independence_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a resolution plus a value-free generated audit record."""
    outcome = resolution_gate.resolve(
        address, evidence, now, independence_audit=independence_audit
    )
    generated_audit = audit_log.create(address, evidence, outcome, now) if isinstance(address, dict) and isinstance(outcome, dict) else None
    result: dict[str, Any] = {"resolution": outcome, "generated_audit": generated_audit}
    if audit is not None:
        result["replay"] = replay_verifier.verify_replay(
            address, evidence, audit, independence_audit=independence_audit
        )
    if protocol_manifest is not None or claim_type is not None:
        result["protocol_claim"] = protocol_claim_gate.assess_claim(protocol_manifest, claim_type if isinstance(claim_type, str) else "")
    errors = response_contract.validate(result)
    if errors:
        raise RuntimeError("response contract violation: " + "; ".join(errors))
    return result


def _load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def check_contract_only(response_path: str) -> dict[str, Any]:
    """Validate a saved public response JSON against response_contract without re-running the gate."""
    response = _load(response_path)
    errors = response_contract.validate(response)
    if errors:
        return {"status": "CONTRACT_INVALID", "errors": errors}
    return {"status": "CONTRACT_OK", "errors": []}


def _resolve_flag_conflicts(args: argparse.Namespace, exclusive_flag: str) -> list[str]:
    """Collect mutual-exclusion errors for standalone modes (no resolve inputs)."""
    conflicts: list[str] = []
    if exclusive_flag == "--limitations" and args.check_contract_only is not None:
        conflicts.append("--check-contract-only must not be supplied with --limitations")
    if exclusive_flag == "--check-contract-only" and args.limitations:
        conflicts.append("--limitations must not be supplied with --check-contract-only")
    if args.address is not None:
        conflicts.append(f"address positional must not be supplied with {exclusive_flag}")
    if args.evidence is not None:
        conflicts.append(f"evidence positional must not be supplied with {exclusive_flag}")
    if args.now is not None:
        conflicts.append(f"--now must not be supplied with {exclusive_flag}")
    if args.audit is not None:
        conflicts.append(f"--audit must not be supplied with {exclusive_flag}")
    if args.protocol_manifest is not None:
        conflicts.append(f"--protocol-manifest must not be supplied with {exclusive_flag}")
    if args.claim_type is not None:
        conflicts.append(f"--claim-type must not be supplied with {exclusive_flag}")
    if args.independence_audit is not None:
        conflicts.append(f"--independence-audit must not be supplied with {exclusive_flag}")
    return conflicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Address resolution and replay verifier")
    parser.add_argument(
        "--limitations",
        action="store_true",
        help="Print the synthetic-only LIMITATIONS / conformance document as JSON (no address/evidence)",
    )
    parser.add_argument(
        "--check-contract-only",
        metavar="RESPONSE.json",
        help="Validate a saved public response JSON against response_contract without re-running the gate",
    )
    parser.add_argument("address", nargs="?", help="Address JSON path")
    parser.add_argument("evidence", nargs="?", help="Evidence bundle JSON path")
    parser.add_argument("--now", help="Evaluation time in ISO-8601 UTC")
    parser.add_argument("--audit", help="Optional prior audit JSON to replay")
    parser.add_argument(
        "--independence-audit",
        help="Optional external semantic-independence audit JSON (required shape for AUDITED Addresses)",
    )
    parser.add_argument("--protocol-manifest", help="Optional protocol manifest JSON for claim gating")
    parser.add_argument("--claim-type", help="Claim type to assess against the protocol manifest")
    args = parser.parse_args(argv)

    if args.limitations:
        conflicts = _resolve_flag_conflicts(args, "--limitations")
        if conflicts:
            print(json.dumps({"status": "INVALID_INPUT", "errors": conflicts}, ensure_ascii=False, sort_keys=True))
            return 2
        print(json.dumps(limitations.limitations(), ensure_ascii=False, sort_keys=True))
        return 0

    if args.check_contract_only is not None:
        conflicts = _resolve_flag_conflicts(args, "--check-contract-only")
        if conflicts:
            print(json.dumps({"status": "INVALID_INPUT", "errors": conflicts}, ensure_ascii=False, sort_keys=True))
            return 2
        try:
            result = check_contract_only(args.check_contract_only)
        except (OSError, ValueError, json.JSONDecodeError, TypeError) as exc:
            print(json.dumps({"status": "INVALID_INPUT", "errors": [str(exc)]}, ensure_ascii=False, sort_keys=True))
            return 2
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "CONTRACT_OK" else 1

    if args.address is None or args.evidence is None or args.now is None:
        parser.error("address, evidence, and --now are required unless --limitations or --check-contract-only is set")

    try:
        result = evaluate(
            _load(args.address),
            _load(args.evidence),
            args.now,
            _load(args.audit) if args.audit else None,
            _load(args.protocol_manifest) if args.protocol_manifest else None,
            args.claim_type,
            _load(args.independence_audit) if args.independence_audit else None,
        )
    except (OSError, ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
