"""Replay an Address decision and bind it to its value-free audit record."""

from __future__ import annotations

from typing import Any

import audit_log
import resolution_gate


def verify_replay(
    address: dict[str, Any],
    evidence: list[dict[str, Any]],
    record: dict[str, Any],
    independence_audit: Any = None,
) -> dict[str, Any]:
    """Re-run the gate at the recorded time and compare the complete audit record."""
    errors = audit_log.verify(record)
    if errors:
        return {"status": "INVALID_AUDIT", "errors": errors}
    if record["address_id"] != address.get("address_id"):
        return {"status": "LINEAGE_MISMATCH", "errors": ["record address_id differs from supplied Address"]}
    outcome = resolution_gate.resolve(
        address, evidence, record["evaluated_at"], independence_audit=independence_audit
    )
    expected = audit_log.create(address, evidence, outcome, record["evaluated_at"])
    if expected != record:
        mismatches = sorted(key for key in expected if expected[key] != record.get(key))
        return {"status": "REPLAY_MISMATCH", "errors": mismatches}
    return {"status": "REPLAY_VERIFIED", "errors": [], "decision": outcome["decision"], "value": None}
