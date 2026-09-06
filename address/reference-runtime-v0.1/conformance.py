"""Machine-readable conformance runner for the Address reference runtime.

Aggregates LIMITATIONS, a synthetic validate/evaluate battery, and R6-G protocol
manifest / experiment-claim gating into one report. Does not run R6-G, discover
Values, or reinterpret LIMITATIONS as PASS capability.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import address_cli
import address_runtime
import limitations
import protocol_claim_gate

SCHEMA_VERSION = "address-conformance-v1"

# Aggregate vocabulary: CONFORMANT when required checks succeed while the
# LIMITATIONS section remains explicitly LIMITATIONS (never PASS).
_CONFORMANT = "CONFORMANT"
_FAIL = "FAIL"
_PASS = "PASS"
_LIMITATIONS = "LIMITATIONS"
_NOT_RUN = "NOT_RUN"
_BLOCKED = "BLOCKED"
_MANIFEST_VALID = "MANIFEST_VALID"

# Closed enums for conformance checks and their allowed statuses.
CHECK_IDS_ALLOWED: frozenset[str] = frozenset({
    "limitations_document",
    "synthetic_address_validate",
    "synthetic_evaluate_ready",
    "synthetic_evaluate_abstain",
    "r6g_protocol_manifest",
    "r6g_experiment_result_claim",
})

CHECK_STATUSES_ALLOWED: frozenset[str] = frozenset({
    _PASS,
    _FAIL,
    _NOT_RUN,
    _LIMITATIONS,
    _BLOCKED,
})

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VALID_ADDRESS = FIXTURES / "valid_synthetic_address.json"
VALID_EVIDENCE = FIXTURES / "valid_evidence_bundle.json"
R6G_MANIFEST = FIXTURES / "r6g_frozen_protocol_manifest.json"
EVAL_NOW = "2026-09-06T00:00:00Z"


def _check(check_id: str, status: str, detail: Any) -> dict[str, Any]:
    assert check_id in CHECK_IDS_ALLOWED, f"unknown check_id: {check_id}"
    assert status in CHECK_STATUSES_ALLOWED, f"unknown check status: {status}"
    return {"id": check_id, "status": status, "detail": detail}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _limitations_check() -> dict[str, Any]:
    doc = limitations.limitations()
    # Never reinterpret LIMITATIONS as PASS / capability. Embed the document
    # under status LIMITATIONS even when the aggregate report is CONFORMANT.
    return _check(
        "limitations_document",
        _LIMITATIONS,
        {
            "schema_version": doc.get("schema_version"),
            "status": doc.get("status"),
            "document": doc,
        },
    )


def _synthetic_validate_check() -> dict[str, Any]:
    address = _load_json(VALID_ADDRESS)
    errors = address_runtime.validate(address)
    valid = errors == []
    return _check(
        "synthetic_address_validate",
        _PASS if valid else _FAIL,
        {
            "fixture": VALID_ADDRESS.name,
            "validate_status": "VALID" if valid else "INVALID",
            "errors": errors,
        },
    )


def _synthetic_ready_check() -> dict[str, Any]:
    address = _load_json(VALID_ADDRESS)
    address["address_id"] = address_runtime.canonical_id(address)
    evidence = _load_json(VALID_EVIDENCE)
    result = address_cli.evaluate(address, evidence, EVAL_NOW)
    resolution = result.get("resolution") if isinstance(result, dict) else None
    decision = resolution.get("decision") if isinstance(resolution, dict) else None
    value = resolution.get("value") if isinstance(resolution, dict) else "MISSING"
    ok = decision == "READY_FOR_VERIFICATION" and value is None
    return _check(
        "synthetic_evaluate_ready",
        _PASS if ok else _FAIL,
        {
            "decision": decision,
            "reason": resolution.get("reason") if isinstance(resolution, dict) else None,
            "value": value,
        },
    )


def _synthetic_abstain_check() -> dict[str, Any]:
    """At least one ABSTAIN path (shared-law common-cause) with value=null."""
    address = _load_json(VALID_ADDRESS)
    address["address_id"] = address_runtime.canonical_id(address)
    evidence = copy.deepcopy(_load_json(VALID_EVIDENCE))
    if not isinstance(evidence, list) or len(evidence) < 2:
        return _check(
            "synthetic_evaluate_abstain",
            _FAIL,
            {"error": "valid_evidence_bundle must have at least two entries"},
        )
    evidence[1]["semantic_law_id"] = evidence[0]["semantic_law_id"]
    result = address_cli.evaluate(address, evidence, EVAL_NOW)
    resolution = result.get("resolution") if isinstance(result, dict) else None
    decision = resolution.get("decision") if isinstance(resolution, dict) else None
    value = resolution.get("value") if isinstance(resolution, dict) else "MISSING"
    reason = resolution.get("reason") if isinstance(resolution, dict) else None
    ok = decision == "ABSTAIN" and value is None
    return _check(
        "synthetic_evaluate_abstain",
        _PASS if ok else _FAIL,
        {
            "path": "shared_law",
            "decision": decision,
            "reason": reason,
            "value": value,
        },
    )


def _r6g_manifest_check() -> dict[str, Any]:
    manifest = _load_json(R6G_MANIFEST)
    errors = protocol_claim_gate.validate_manifest(manifest)
    ok = errors == []
    return _check(
        "r6g_protocol_manifest",
        _PASS if ok else _FAIL,
        {
            "fixture": R6G_MANIFEST.name,
            "manifest_status": _MANIFEST_VALID if ok else "MANIFEST_INVALID",
            "errors": errors,
            "experiment_state": manifest.get("experiment_state") if isinstance(manifest, dict) else None,
        },
    )


def _r6g_experiment_claim_check() -> dict[str, Any]:
    """Record R6-G EXPERIMENT_RESULT as BLOCKED / NOT_RUN — never executed."""
    manifest = _load_json(R6G_MANIFEST)
    assessment = protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")
    claim_status = assessment.get("status") if isinstance(assessment, dict) else None
    lim = limitations.limitations()
    lim_r6g = lim.get("r6g_experiment")
    # Prefer NOT_RUN when limitations declare it; also accept BLOCKED from gate.
    # Never PASS / EXECUTED / COMPLETED / ALLOWED_AS_RESULT.
    if claim_status == "BLOCKED" and lim_r6g == _NOT_RUN:
        status = _NOT_RUN
    elif claim_status == "BLOCKED":
        status = _BLOCKED
    elif lim_r6g == _NOT_RUN:
        status = _NOT_RUN
    else:
        status = _FAIL
    claiming = limitations.is_claiming_status(claim_status) or claim_status in {
        "ALLOWED_AS_RESULT",
        "EXECUTED",
        "RUN",
        "COMPLETED",
    }
    if claiming or lim_r6g in {"COMPLETED", "EXECUTED", "RUN"}:
        status = _FAIL
    return _check(
        "r6g_experiment_result_claim",
        status,
        {
            "claim_type": "EXPERIMENT_RESULT",
            "claim_status": claim_status,
            "claim_reason": assessment.get("reason") if isinstance(assessment, dict) else None,
            "limitations_r6g_experiment": lim_r6g,
            "executed": False,
        },
    )


def run_conformance() -> dict[str, Any]:
    """Return a stable conformance report dict.

    Schema:
      schema_version: address-conformance-v1
      status: CONFORMANT | FAIL
      checks: [{id, status, detail}, ...]

    Check statuses use PASS / FAIL / NOT_RUN / LIMITATIONS / BLOCKED carefully.
    The LIMITATIONS check is always status LIMITATIONS (never PASS).
    R6-G experiment claim is NOT_RUN or BLOCKED (never claimed executed).
    """
    checks = [
        _limitations_check(),
        _synthetic_validate_check(),
        _synthetic_ready_check(),
        _synthetic_abstain_check(),
        _r6g_manifest_check(),
        _r6g_experiment_claim_check(),
    ]
    # Required for CONFORMANT: no FAIL; LIMITATIONS present; R6-G not executed.
    has_fail = any(c["status"] == _FAIL for c in checks)
    has_limitations = any(
        c["id"] == "limitations_document" and c["status"] == _LIMITATIONS for c in checks
    )
    r6g = next((c for c in checks if c["id"] == "r6g_experiment_result_claim"), None)
    r6g_ok = r6g is not None and r6g["status"] in {_NOT_RUN, _BLOCKED}
    overall = _CONFORMANT if (not has_fail and has_limitations and r6g_ok) else _FAIL
    return {
        "schema_version": SCHEMA_VERSION,
        "status": overall,
        "checks": checks,
    }
