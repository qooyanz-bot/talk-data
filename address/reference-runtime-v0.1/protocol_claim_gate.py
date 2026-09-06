"""Block capability claims that outrun a protocol's recorded evidence state."""

from __future__ import annotations

from typing import Any

# Closed enums from existing fixtures/tests vocabulary (expand only when needed).
# auditor_handoff.decision: PENDING | PASS only — FAIL does not appear on protocol
# manifests (independence_audit uses FAIL on a different surface).
EVIDENCE_STATE_ALLOWED = frozenset({"SPEC_ONLY", "DIAGNOSTIC_ONLY", "RESULT_BACKED"})
IMPLEMENTATION_STATE_ALLOWED = frozenset({"NOT_IMPLEMENTED", "IMPLEMENTED"})
EXPERIMENT_STATE_ALLOWED = frozenset({"NOT_RUN", "COMPLETED"})
INDEPENDENT_REPLAY_STATE_ALLOWED = frozenset({"NOT_RUN", "REPLICATED"})
AUDITOR_HANDOFF_DECISION_ALLOWED = frozenset({"PENDING", "PASS"})
AUDITOR_HANDOFF_KEYS = frozenset({"decision", "primary_run_authorized"})

_STATE_ENUMS = (
    ("evidence_state", EVIDENCE_STATE_ALLOWED),
    ("implementation_state", IMPLEMENTATION_STATE_ALLOWED),
    ("experiment_state", EXPERIMENT_STATE_ALLOWED),
    ("independent_replay_state", INDEPENDENT_REPLAY_STATE_ALLOWED),
)


def _one_of(allowed: frozenset[str]) -> str:
    return ", ".join(sorted(allowed))


def validate_manifest(manifest: Any) -> list[str]:
    """Return machine-checkable closed-enum / shape errors for a protocol manifest.

    Does not raise. Empty list means the manifest is structurally valid for the
    Protocol Claim Gate (enums + handoff shape). Does not authorize claims.
    """
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    errors: list[str] = []
    protocol_id = manifest.get("protocol_id")
    if not isinstance(protocol_id, str) or not protocol_id:
        errors.append("protocol_id must be a non-empty string")
    for field, allowed in _STATE_ENUMS:
        value = manifest.get(field)
        if not isinstance(value, str) or value not in allowed:
            errors.append(f"{field} must be one of {_one_of(allowed)}")
    if "auditor_handoff" in manifest:
        handoff = manifest["auditor_handoff"]
        if not isinstance(handoff, dict):
            errors.append("auditor_handoff must be an object when present")
        else:
            extra = set(handoff) - AUDITOR_HANDOFF_KEYS
            if extra:
                errors.append(
                    "auditor_handoff keys must be only decision, primary_run_authorized"
                )
            decision = handoff.get("decision")
            if not isinstance(decision, str) or decision not in AUDITOR_HANDOFF_DECISION_ALLOWED:
                errors.append(
                    "auditor_handoff.decision must be one of "
                    + _one_of(AUDITOR_HANDOFF_DECISION_ALLOWED)
                )
            authorized = handoff.get("primary_run_authorized")
            if authorized is not None and not isinstance(authorized, bool):
                errors.append("auditor_handoff.primary_run_authorized must be bool or null")
    return errors


def assess_claim(manifest: Any, claim_type: str) -> dict[str, Any]:
    """Assess a design description, experiment result, or capability claim.

    This gate is intentionally conservative. It does not authorize an experiment;
    it only prevents a later statement from claiming more than the supplied
    manifest can support. Invalid closed enums / handoff shape are BLOCKED as
    MANIFEST_INVALID for every claim_type (including DESIGN_DESCRIPTION).
    """
    errors = validate_manifest(manifest)
    if errors:
        return {"status": "BLOCKED", "reason": "MANIFEST_INVALID", "unmet": errors}
    if claim_type == "DESIGN_DESCRIPTION":
        return {"status": "ALLOWED_AS_DESIGN", "reason": "NO_RESULT_CLAIM"}
    if claim_type not in {"EXPERIMENT_RESULT", "CAPABILITY_CLAIM"}:
        return {"status": "BLOCKED", "reason": "CLAIM_TYPE_UNKNOWN"}
    gates = {
        "implementation_state": "IMPLEMENTED",
        "experiment_state": "COMPLETED",
        "independent_replay_state": "REPLICATED",
    }
    unmet = [f"{field}!={expected}" for field, expected in gates.items() if manifest.get(field) != expected]
    handoff = manifest.get("auditor_handoff")
    if not isinstance(handoff, dict) or handoff.get("decision") != "PASS":
        unmet.append("auditor_handoff.decision!=PASS")
    if not isinstance(handoff, dict) or handoff.get("primary_run_authorized") is not True:
        unmet.append("primary_run_authorized!=true")
    if unmet:
        return {"status": "BLOCKED", "reason": "EVIDENCE_GATES_UNMET", "unmet": unmet}
    if claim_type == "CAPABILITY_CLAIM" and manifest.get("evidence_state") != "RESULT_BACKED":
        return {"status": "BLOCKED", "reason": "CAPABILITY_EVIDENCE_NOT_RESULT_BACKED"}
    return {"status": "ALLOWED_AS_RESULT", "reason": "RECORDED_EVIDENCE_GATES_PASS"}
