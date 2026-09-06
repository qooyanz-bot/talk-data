"""Evidence-contract evaluator that refuses to equate path diversity with independence."""

from __future__ import annotations

from typing import Any

REQUIRED = {"evidence_id", "claim_hash", "path_id", "authority_id", "generator_id", "semantic_law_id", "observed_at"}
INDEPENDENCE_AXES = ("authority_id", "generator_id", "semantic_law_id")


def assess(evidence: Any, minimum_sources: int = 2) -> dict[str, Any]:
    """Return a conservative evidence decision.

    A distinct path alone never establishes independence. A usable contracted set
    requires unique claims and pairwise separation across authority, generator,
    and semantic-law axes. This establishes only CONTRACTED independence: an
    external audit is still required before claiming semantic independence.
    """
    if not isinstance(evidence, list) or len(evidence) < minimum_sources:
        return {"status": "INSUFFICIENT", "accepted": False, "reasons": ["fewer than minimum_sources evidence records"]}
    if any(not isinstance(item, dict) for item in evidence):
        return {"status": "INVALID", "accepted": False, "reasons": ["evidence records must be objects"]}
    missing = [item.get("evidence_id", "<unknown>") + ": missing " + ", ".join(sorted(REQUIRED - set(item))) for item in evidence if REQUIRED - set(item)]
    if missing:
        return {"status": "INVALID", "accepted": False, "reasons": missing}
    reasons: list[str] = []
    for field in ("evidence_id", "claim_hash", "path_id"):
        values = [item[field] for item in evidence]
        if len(values) != len(set(values)):
            reasons.append(f"duplicate {field}")
    for axis in INDEPENDENCE_AXES:
        values = [item[axis] for item in evidence]
        if len(values) != len(set(values)):
            reasons.append(f"shared {axis}: path diversity is not semantic independence")
    if reasons:
        return {"status": "CONFLICT", "accepted": False, "reasons": reasons}
    return {
        "status": "CONTRACTED",
        "accepted": True,
        "reasons": ["metadata separation passed; semantic independence remains unaudited"],
    }
