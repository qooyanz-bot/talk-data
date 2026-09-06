"""Evidence-contract evaluator that refuses to equate path diversity with independence."""

from __future__ import annotations

from typing import Any

REQUIRED = {"evidence_id", "claim_hash", "path_id", "authority_id", "generator_id", "semantic_law_id", "observed_at"}
INDEPENDENCE_AXES = ("authority_id", "generator_id", "semantic_law_id")

# assess() may emit these independence verdicts only. Never INDEPENDENT / AUDITED:
# this runtime cannot grant semantic independence from path IDs or metadata alone.
INDEPENDENCE_COMMON_CAUSE_SUSPECT = "COMMON_CAUSE_SUSPECT"
INDEPENDENCE_CONTRACTED = "CONTRACTED"
INDEPENDENCE_UNVERIFIED = "UNVERIFIED"
_FORBIDDEN_INDEPENDENCE_CLAIMS = frozenset({"INDEPENDENT", "AUDITED"})


def _result(status: str, accepted: bool, independence: str, reasons: list[str]) -> dict[str, Any]:
    if independence in _FORBIDDEN_INDEPENDENCE_CLAIMS:
        raise AssertionError("assess() must never emit INDEPENDENT or AUDITED")
    return {
        "status": status,
        "accepted": accepted,
        "independence": independence,
        "reasons": reasons,
    }


def assess(evidence: Any, minimum_sources: int = 2) -> dict[str, Any]:
    """Return a conservative evidence decision with an explicit independence verdict.

    A distinct path alone never establishes independence. A usable contracted set
    requires unique claims and pairwise separation across authority, generator,
    and semantic-law axes. This establishes only CONTRACTED independence: an
    external audit is still required before claiming semantic independence.

    Independence field:
    - COMMON_CAUSE_SUSPECT: shared authority/generator/semantic_law (or similar
      duplicate identity) → accepted=False (status CONFLICT)
    - CONTRACTED: metadata separation passed; semantic independence unaudited
      → accepted=True; never upgraded to INDEPENDENT/AUDITED here
    - UNVERIFIED: insufficient or invalid evidence → accepted=False
    """
    if not isinstance(evidence, list) or len(evidence) < minimum_sources:
        return _result(
            "INSUFFICIENT",
            False,
            INDEPENDENCE_UNVERIFIED,
            ["fewer than minimum_sources evidence records"],
        )
    if any(not isinstance(item, dict) for item in evidence):
        return _result(
            "INVALID",
            False,
            INDEPENDENCE_UNVERIFIED,
            ["evidence records must be objects"],
        )
    missing = [
        item.get("evidence_id", "<unknown>") + ": missing " + ", ".join(sorted(REQUIRED - set(item)))
        for item in evidence
        if REQUIRED - set(item)
    ]
    if missing:
        return _result("INVALID", False, INDEPENDENCE_UNVERIFIED, missing)
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
        return _result("CONFLICT", False, INDEPENDENCE_COMMON_CAUSE_SUSPECT, reasons)
    return _result(
        "CONTRACTED",
        True,
        INDEPENDENCE_CONTRACTED,
        ["metadata separation passed; semantic independence remains unaudited"],
    )


def assertion_key_set(evidence: Any) -> set[str]:
    """Return assertion_key strings present on evidence records.

    These keys are for contradiction detection only. Matching an Address
    unknown.slot or residual label must never be treated as filling that slot.
    """
    keys: set[str] = set()
    if not isinstance(evidence, list):
        return keys
    for item in evidence:
        if isinstance(item, dict) and "assertion_key" in item:
            key = item["assertion_key"]
            if isinstance(key, str) and key:
                keys.add(key)
            else:
                keys.add(str(key))
    return keys
