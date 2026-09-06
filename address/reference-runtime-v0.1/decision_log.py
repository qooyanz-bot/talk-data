"""Value-free Decision Log / auditor-handoff surface for Protocol Claim Gate.

Builds a machine-checkable handoff record from (manifest, claim_type, assess_claim
result). Claim-status and handoff fields only — never fills a Value, never
embeds secrets, and never asserts that a protocol ran.

Records are content-addressed: decision_log_id = "decision_log:" + sha256 of the
canonical payload without the id field (same digest style as audit_log.content_digest).
"""

from __future__ import annotations

from typing import Any

import audit_log
import protocol_claim_gate

SCHEMA_VERSION = "address-decision-log-v1"

# Fields copied from the protocol manifest into the decision log (state only).
# Closed enums: single source of truth in protocol_claim_gate.STATE_ENUMS.
_STATE_FIELDS = (
    "evidence_state",
    "experiment_state",
    "implementation_state",
    "independent_replay_state",
)

# auditor_handoff snapshot: decision + primary_run_authorized only (no secrets).
# Exact key set matches protocol_claim_gate.AUDITOR_HANDOFF_KEYS.
_HANDOFF_KEYS = ("decision", "primary_run_authorized")

# Required keys on a content-addressed decision_log record (includes id).
REQUIRED_KEYS = {
    "schema_version",
    "protocol_id",
    "claim_type",
    "claim_status",
    "claim_reason",
    "unmet",
    "auditor_handoff",
    "value",
    "evidence_state",
    "experiment_state",
    "implementation_state",
    "independent_replay_state",
    "decision_log_id",
}


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
    """Build a value-free, content-addressed decision-log record from assess_claim output.

    Always sets value=null. Attaches decision_log_id from the canonical payload
    hash (excluding the id field). Does not authorize runs or invent evidence.
    """
    if not isinstance(assessment, dict):
        # Gate-only reasons: non-dict assessment is treated as structural failure.
        assessment = {
            "status": "BLOCKED",
            "reason": "MANIFEST_INVALID",
            "unmet": ["assessment must be an object"],
        }
    protocol_id = None
    if isinstance(manifest, dict) and isinstance(manifest.get("protocol_id"), str):
        protocol_id = manifest["protocol_id"]
    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "protocol_id": protocol_id,
        "claim_type": claim_type if isinstance(claim_type, str) else "",
        "claim_status": assessment.get("status"),
        "claim_reason": assessment.get("reason"),
        # Always a list for machine-checkability (empty when assess_claim omits unmet).
        "unmet": list(assessment["unmet"]) if isinstance(assessment.get("unmet"), list) else [],
        "auditor_handoff": _handoff_snapshot(manifest),
        "value": None,
    }
    for field in _STATE_FIELDS:
        record[field] = manifest.get(field) if isinstance(manifest, dict) else None
    record["decision_log_id"] = "decision_log:" + audit_log.content_digest(record).removeprefix("sha256:")
    return record


# Alias mirroring audit_log.create naming for content-addressed builders.
create = build_decision_log


def verify(record: Any) -> list[str]:
    """Verify required shape, closed-enum states, handoff keys, and self-addressed integrity.

    claim_type must be in protocol_claim_gate.CLAIM_TYPE_ALLOWED.
    claim_reason when present (not None) must be in protocol_claim_gate.CLAIM_REASON_ALLOWED.
    State fields present (not None) must be in protocol_claim_gate closed sets.
    auditor_handoff.decision when not None must be PENDING|PASS.
    Handoff keys must be exactly {decision, primary_run_authorized}.
    """
    if not isinstance(record, dict):
        return ["decision_log must be an object"]
    missing = REQUIRED_KEYS - set(record)
    if missing:
        return ["missing required fields: " + ", ".join(sorted(missing))]
    if record["schema_version"] != SCHEMA_VERSION:
        return ["unsupported decision_log schema version"]
    errors: list[str] = []
    claim_type = record.get("claim_type")
    if not isinstance(claim_type, str) or claim_type not in protocol_claim_gate.CLAIM_TYPE_ALLOWED:
        errors.append(
            "claim_type must be one of "
            + protocol_claim_gate.format_allowed(protocol_claim_gate.CLAIM_TYPE_ALLOWED)
        )
    claim_reason = record.get("claim_reason")
    if claim_reason is not None and (
        not isinstance(claim_reason, str)
        or claim_reason not in protocol_claim_gate.CLAIM_REASON_ALLOWED
    ):
        errors.append(
            "claim_reason must be one of "
            + protocol_claim_gate.format_allowed(protocol_claim_gate.CLAIM_REASON_ALLOWED)
        )
    for field, allowed in protocol_claim_gate.STATE_ENUMS:
        value = record.get(field)
        if value is not None and (not isinstance(value, str) or value not in allowed):
            errors.append(f"{field} must be one of {protocol_claim_gate.format_allowed(allowed)}")
    handoff = record.get("auditor_handoff")
    if not isinstance(handoff, dict):
        errors.append("auditor_handoff must be an object")
    else:
        if set(handoff) != protocol_claim_gate.AUDITOR_HANDOFF_KEYS:
            errors.append(
                "auditor_handoff keys must be only decision, primary_run_authorized"
            )
        decision = handoff.get("decision")
        if decision is not None and (
            not isinstance(decision, str)
            or decision not in protocol_claim_gate.AUDITOR_HANDOFF_DECISION_ALLOWED
        ):
            errors.append(
                "auditor_handoff.decision must be one of "
                + protocol_claim_gate.format_allowed(
                    protocol_claim_gate.AUDITOR_HANDOFF_DECISION_ALLOWED
                )
            )
    payload = dict(record)
    actual = payload.pop("decision_log_id")
    expected = "decision_log:" + audit_log.content_digest(payload).removeprefix("sha256:")
    if actual != expected:
        errors.append("decision_log_id does not match canonical record hash")
    return errors
