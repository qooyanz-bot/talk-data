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

# External semantic-independence audit record (AUDITED path). Frozen machine-checkable
# checklist. assess() never consults this; only assess_audited_independence() may
# return independence=AUDITED, and only when every field below is satisfied.
AUDITED_INDEPENDENCE_REQUIRED_FIELDS = frozenset(
    {"auditor_id", "decision", "method", "evidence_digests", "audited_at"}
)
AUDITED_INDEPENDENCE_DECISION_PASS = "PASS"
INDEPENDENCE_AUDITED = "AUDITED"
INDEPENDENCE_AUDIT_UNMET = "UNMET"


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


def audited_independence_checklist() -> dict[str, Any]:
    """Return the frozen checklist documenting required AUDITED audit-record fields.

    Machine-checkable shape only. Satisfying this checklist does not invent a
    Value and does not imply assess() returned AUDITED.
    """
    return {
        "required_fields": sorted(AUDITED_INDEPENDENCE_REQUIRED_FIELDS),
        "decision_must_be": AUDITED_INDEPENDENCE_DECISION_PASS,
        "notes": [
            "auditor_id: nonempty string identifying the external auditor",
            "decision: must be exactly PASS",
            "method: nonempty string naming the audit method",
            "evidence_digests: nonempty list of nonempty digest strings "
            "or {evidence_id, digest} objects with nonempty strings",
            "audited_at: nonempty ISO-8601 timestamp string",
            "assess() alone never returns AUDITED; path diversity never grants AUDITED",
        ],
    }


def _audit_unmet(reasons: list[str]) -> dict[str, Any]:
    return {
        "status": "UNMET",
        "accepted": False,
        "independence": INDEPENDENCE_AUDIT_UNMET,
        "reasons": reasons,
    }


def _digest_entry_ok(item: Any) -> bool:
    if isinstance(item, str) and item:
        return True
    if isinstance(item, dict):
        evidence_id = item.get("evidence_id")
        digest = item.get("digest")
        return isinstance(evidence_id, str) and bool(evidence_id) and isinstance(digest, str) and bool(digest)
    return False


def assess_audited_independence(audit_record: Any) -> dict[str, Any]:
    """Assess an external semantic-independence audit record against the frozen checklist.

    Returns independence=AUDITED only when the record passes every required field.
    Otherwise returns unmet reasons. Never upgrades CONTRACTED evidence from
    assess() alone; forged or incomplete records are rejected.
    """
    if audit_record is None:
        return _audit_unmet(["independence_audit record is missing"])
    if not isinstance(audit_record, dict):
        return _audit_unmet(["independence_audit must be an object"])
    missing = AUDITED_INDEPENDENCE_REQUIRED_FIELDS - set(audit_record)
    if missing:
        return _audit_unmet(
            ["missing required fields: " + ", ".join(sorted(missing))]
        )
    reasons: list[str] = []
    auditor_id = audit_record.get("auditor_id")
    if not isinstance(auditor_id, str) or not auditor_id:
        reasons.append("auditor_id must be a nonempty string")
    if audit_record.get("decision") != AUDITED_INDEPENDENCE_DECISION_PASS:
        reasons.append("decision must be PASS")
    method = audit_record.get("method")
    if not isinstance(method, str) or not method:
        reasons.append("method must be a nonempty string")
    digests = audit_record.get("evidence_digests")
    if not isinstance(digests, list) or not digests:
        reasons.append("evidence_digests must be a nonempty list")
    elif any(not _digest_entry_ok(item) for item in digests):
        reasons.append(
            "evidence_digests entries must be nonempty strings or "
            "{evidence_id, digest} objects with nonempty strings"
        )
    audited_at = audit_record.get("audited_at")
    if not isinstance(audited_at, str) or not audited_at:
        reasons.append("audited_at must be a nonempty string")
    if reasons:
        return _audit_unmet(reasons)
    return {
        "status": "AUDITED",
        "accepted": True,
        "independence": INDEPENDENCE_AUDITED,
        "reasons": [
            "external semantic-independence audit record passed frozen checklist"
        ],
    }


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
