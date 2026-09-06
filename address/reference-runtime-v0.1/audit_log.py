"""Content-addressed, value-free audit records for Address resolution decisions."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import resolution_gate

SCHEMA_VERSION = "ADDRESS-AUDIT-1.0"

REQUIRED_KEYS = frozenset({
    "schema_version",
    "address_id",
    "evaluated_at",
    "decision",
    "reason",
    "detail_digest",
    "evidence_digests",
    "audit_id",
})


def content_digest(value: Any) -> str:
    """Canonical content-addressed digest (sha256 of sorted-key JSON).

    Shared by Audit Log records and independence_audit evidence binding so
    digests never diverge across modules.
    """
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


# Backward-compatible private alias (same algorithm).
_digest = content_digest


def evidence_digest_entries(evidence: Any) -> list[dict[str, str]]:
    """Build sorted {evidence_id, digest} entries; malformed evidence never raises.

    Digests use content_digest() over each full evidence object. Used by Audit
    Log create() and independence_audit binding in evidence_contract.
    """
    if not isinstance(evidence, list):
        return []
    entries: list[dict[str, str]] = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str):
            continue
        entries.append({"evidence_id": evidence_id, "digest": content_digest(item)})
    return sorted(entries, key=lambda item: (item["evidence_id"], item["digest"]))


# Backward-compatible private alias.
_evidence_digest_entries = evidence_digest_entries


def create(address: dict[str, Any], evidence: list[dict[str, Any]], outcome: dict[str, Any], evaluated_at: str) -> dict[str, Any]:
    """Create a reproducible audit record without storing target or assertion values.

    Malformed evidence (non-list, non-dict items, missing/non-str evidence_id) is
    rejected by omission rather than raising KeyError/TypeError.
    """
    evidence_digests = _evidence_digest_entries(evidence)
    record = {
        "schema_version": SCHEMA_VERSION,
        "address_id": address["address_id"],
        "evaluated_at": evaluated_at,
        "decision": outcome["decision"],
        "reason": outcome["reason"],
        "detail_digest": _digest(outcome.get("details", [])),
        "evidence_digests": evidence_digests,
    }
    record["audit_id"] = "audit:" + _digest(record).removeprefix("sha256:")
    return record


def verify(record: Any) -> list[str]:
    """Verify the record's required shape, closed enums, and self-addressed integrity."""
    if not isinstance(record, dict):
        return ["audit record must be an object"]
    missing = REQUIRED_KEYS - set(record)
    if missing:
        return ["missing required fields: " + ", ".join(sorted(missing))]
    if record["schema_version"] != SCHEMA_VERSION:
        return ["unsupported audit schema version"]
    errors: list[str] = []
    decision = record.get("decision")
    if not isinstance(decision, str) or decision not in resolution_gate.DECISION_ALLOWED:
        errors.append(
            f"decision must be one of {', '.join(sorted(resolution_gate.DECISION_ALLOWED))}"
        )
    reason = record.get("reason")
    if not isinstance(reason, str) or reason not in resolution_gate.REASON_ALLOWED:
        errors.append(
            f"reason must be one of {', '.join(sorted(resolution_gate.REASON_ALLOWED))}"
        )
    if not isinstance(record["evidence_digests"], list) or any(
        not isinstance(item, dict) or set(item) != {"evidence_id", "digest"}
        for item in record["evidence_digests"]
    ):
        errors.append("invalid evidence digest list")
    payload = dict(record)
    actual = payload.pop("audit_id")
    expected = "audit:" + _digest(payload).removeprefix("sha256:")
    if actual != expected:
        errors.append("audit_id does not match canonical record hash")
    return errors
