"""Replay an Address decision and bind it to its value-free audit record."""

from __future__ import annotations

from typing import Any

import audit_log
import resolution_gate

# Closed replay.status vocabulary (verify_replay emitters; response_contract single source).
REPLAY_STATUS_ALLOWED = frozenset(
    {"REPLAY_VERIFIED", "REPLAY_MISMATCH", "LINEAGE_MISMATCH", "INVALID_AUDIT"}
)


def _status_result(status: str, **fields: Any) -> dict[str, Any]:
    assert status in REPLAY_STATUS_ALLOWED, f"status not in REPLAY_STATUS_ALLOWED: {status!r}"
    return {"status": status, **fields}


def verify_replay(
    address: dict[str, Any],
    evidence: list[dict[str, Any]],
    record: dict[str, Any],
    independence_audit: Any = None,
) -> dict[str, Any]:
    """Re-run the gate at the recorded time and compare the complete audit record."""
    errors = audit_log.verify(record)
    if errors:
        return _status_result("INVALID_AUDIT", errors=errors)
    if record["address_id"] != address.get("address_id"):
        return _status_result(
            "LINEAGE_MISMATCH",
            errors=["record address_id differs from supplied Address"],
        )
    outcome = resolution_gate.resolve(
        address, evidence, record["evaluated_at"], independence_audit=independence_audit
    )
    expected = audit_log.create(address, evidence, outcome, record["evaluated_at"])
    if expected != record:
        mismatches = sorted(key for key in expected if expected[key] != record.get(key))
        return _status_result("REPLAY_MISMATCH", errors=mismatches)
    return _status_result(
        "REPLAY_VERIFIED",
        errors=[],
        decision=outcome["decision"],
        value=None,
    )
