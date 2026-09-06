"""Block capability claims that outrun a protocol's recorded evidence state."""

from __future__ import annotations

from typing import Any


def assess_claim(manifest: Any, claim_type: str) -> dict[str, Any]:
    """Assess a design description, experiment result, or capability claim.

    This gate is intentionally conservative. It does not authorize an experiment;
    it only prevents a later statement from claiming more than the supplied
    manifest can support.
    """
    if not isinstance(manifest, dict) or not isinstance(manifest.get("protocol_id"), str):
        return {"status": "BLOCKED", "reason": "MANIFEST_INVALID"}
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
