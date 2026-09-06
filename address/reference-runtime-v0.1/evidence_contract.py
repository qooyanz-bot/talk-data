"""Evidence-contract evaluator that refuses to equate path diversity with independence."""

from __future__ import annotations

from typing import Any

import audit_log

REQUIRED = {"evidence_id", "claim_hash", "path_id", "authority_id", "generator_id", "semantic_law_id", "observed_at"}
INDEPENDENCE_AXES = ("authority_id", "generator_id", "semantic_law_id")

# assess() may emit these independence verdicts only. Never INDEPENDENT / AUDITED:
# this runtime cannot grant semantic independence from path IDs or metadata alone.
INDEPENDENCE_COMMON_CAUSE_SUSPECT = "COMMON_CAUSE_SUSPECT"
INDEPENDENCE_CONTRACTED = "CONTRACTED"
INDEPENDENCE_UNVERIFIED = "UNVERIFIED"
# Closed independence vocabulary for assess() emitters (single source).
INDEPENDENCE_ASSESS_ALLOWED = frozenset(
    {
        INDEPENDENCE_COMMON_CAUSE_SUSPECT,
        INDEPENDENCE_CONTRACTED,
        INDEPENDENCE_UNVERIFIED,
    }
)
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
# Closed independence vocabulary for assess_audited_independence() emitters (single source).
INDEPENDENCE_AUDIT_ALLOWED = frozenset(
    {INDEPENDENCE_AUDITED, INDEPENDENCE_AUDIT_UNMET}
)


def _result(status: str, accepted: bool, independence: str, reasons: list[str]) -> dict[str, Any]:
    # Closed assess() independence only; never INDEPENDENT / AUDITED here.
    assert independence in INDEPENDENCE_ASSESS_ALLOWED, (
        f"independence not in INDEPENDENCE_ASSESS_ALLOWED: {independence!r}"
    )
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
            "evidence_digests: nonempty list of {evidence_id, digest} objects "
            "(exactly those two nonempty string keys; bare strings rejected)",
            "when evidence is supplied, evidence_digests must exactly match "
            "audit_log.evidence_digest_entries(evidence) (content-addressed; "
            "same evidence_id + digest pairs via content_digest)",
            "audited_at: nonempty ISO-8601 timestamp string",
            "assess() alone never returns AUDITED; path diversity never grants AUDITED",
        ],
    }


def _audit_result(
    status: str, accepted: bool, independence: str, reasons: list[str]
) -> dict[str, Any]:
    assert independence in INDEPENDENCE_AUDIT_ALLOWED, (
        f"independence not in INDEPENDENCE_AUDIT_ALLOWED: {independence!r}"
    )
    return {
        "status": status,
        "accepted": accepted,
        "independence": independence,
        "reasons": reasons,
    }


def _audit_unmet(reasons: list[str]) -> dict[str, Any]:
    return _audit_result("UNMET", False, INDEPENDENCE_AUDIT_UNMET, reasons)


def _digest_entry_ok(item: Any) -> bool:
    """True only for audit_log.evidence_digest_entries-shaped objects.

    Bare digest strings are always rejected for the AUDITED checklist.
    """
    if not isinstance(item, dict) or set(item) != {"evidence_id", "digest"}:
        return False
    evidence_id = item["evidence_id"]
    digest = item["digest"]
    return isinstance(evidence_id, str) and bool(evidence_id) and isinstance(digest, str) and bool(digest)


def _digest_pair(item: Any) -> tuple[str, str] | None:
    """Return (evidence_id, digest) for valid object entries; None otherwise."""
    if not _digest_entry_ok(item):
        return None
    return (item["evidence_id"], item["digest"])


def _evidence_digest_pair_set(evidence: Any) -> set[tuple[str, str]]:
    """Content-addressed (evidence_id, digest) set via shared audit_log helper."""
    return {
        (entry["evidence_id"], entry["digest"])
        for entry in audit_log.evidence_digest_entries(evidence)
    }


def _audit_digest_pair_set(digests: list[Any]) -> set[tuple[str, str]] | None:
    """Normalize typed evidence_digests to (evidence_id, digest) pairs.

    Every entry must already be a {evidence_id, digest} object (bare strings
    fail shape checks earlier). Returns None if any entry is non-bindable.
    """
    pairs: set[tuple[str, str]] = set()
    for item in digests:
        pair = _digest_pair(item)
        if pair is None:
            return None
        pairs.add(pair)
    return pairs


def assess_audited_independence(audit_record: Any, evidence: Any = None) -> dict[str, Any]:
    """Assess an external semantic-independence audit record against the frozen checklist.

    Returns independence=AUDITED only when the record passes every required field.
    ``evidence_digests`` must be typed ``{evidence_id, digest}`` objects (same
    shape as audit_log.evidence_digest_entries); bare strings are unmet. When
    ``evidence`` is supplied, those pairs must exactly match the
    content-addressed entries for that bundle. A PASS audit for a different set
    is unmet, not AUDITED. Never upgrades CONTRACTED evidence from assess()
    alone; forged or incomplete records are rejected.
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
            "evidence_digests entries must be {evidence_id, digest} objects "
            "with nonempty strings (bare digest strings are rejected)"
        )
    audited_at = audit_record.get("audited_at")
    if not isinstance(audited_at, str) or not audited_at:
        reasons.append("audited_at must be a nonempty string")
    if reasons:
        return _audit_unmet(reasons)
    # Content-addressed binding: audit digests must match the supplied evidence.
    if evidence is not None:
        expected = _evidence_digest_pair_set(evidence)
        actual = _audit_digest_pair_set(digests)
        if actual is None:
            return _audit_unmet(
                [
                    "evidence_digests must be {evidence_id, digest} objects "
                    "matching audit_log.evidence_digest_entries "
                    "(content-addressed)"
                ]
            )
        if actual != expected:
            return _audit_unmet(
                [
                    "evidence_digests do not match audit_log.evidence_digest_entries "
                    "for the supplied evidence bundle (evidence_id + digest); "
                    "a PASS audit for a different set cannot satisfy AUDITED"
                ]
            )
    return _audit_result(
        "AUDITED",
        True,
        INDEPENDENCE_AUDITED,
        [
            "external semantic-independence audit record passed frozen checklist"
            + (
                " and evidence_digests match the supplied evidence bundle"
                if evidence is not None
                else ""
            )
        ],
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
