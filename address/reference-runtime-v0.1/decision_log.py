"""Value-free Decision Log / auditor-handoff surface for Protocol Claim Gate.

Builds a machine-checkable handoff record from (manifest, claim_type, assess_claim
result). Claim-status and handoff fields only — never fills a Value, never
embeds secrets, and never asserts that a protocol ran.
"""

from __future__ import annotations

from typing import Any

SCHEMA_VERSION = "address-decision-log-v1"

# Fields copied from the protocol manifest into the decision log (state only).
_STATE_FIELDS = (
    "evidence_state",
    "experiment_state",
    "implementation_state",
    "independent_replay_state",
)

# auditor_handoff snapshot: decision + primary_run_authorized only (no secrets).
_HANDOFF_KEYS = ("decision", "primary_run_authorized")


def _handoff_snapshot(manifest: Any) -> dict[str, Any]:
    """Return a secret-free auditor_handoff snapshot."""
    handoff = manifest.get("auditor_handoff") if isinstance(manifest, dict) else None
    if not isinstance(handoff, dict):
        return {"decision": None, "primary_run_authorized": None}
    return {key: handoff.get(key) for key in _HANDOFF_KEYS}


def build_decision_log(
    manifest: Any,
    claim_type: str,
    assessment: dict[str, Any],
) -> dict[str, Any]:
    """Build a value-free decision-log record from assess_claim output.

    Always sets value=null. Does not authorize runs or invent evidence.
    """
    if not isinstance(assessment, dict):
        assessment = {"status": "BLOCKED", "reason": "ASSESSMENT_INVALID"}
    protocol_id = None
    if isinstance(manifest, dict) and isinstance(manifest.get("protocol_id"), str):
        protocol_id = manifest["protocol_id"]
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "protocol_id": protocol_id,
        "claim_type": claim_type if isinstance(claim_type, str) else "",
        "claim_status": assessment.get("status"),
        "claim_reason": assessment.get("reason"),
        "unmet": assessment.get("unmet") if isinstance(assessment.get("unmet"), list) else None,
        "auditor_handoff": _handoff_snapshot(manifest),
        "value": None,
    }
    for field in _STATE_FIELDS:
        record[field] = manifest.get(field) if isinstance(manifest, dict) else None
    return record
