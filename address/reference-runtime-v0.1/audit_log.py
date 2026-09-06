"""Content-addressed, value-free audit records for Address resolution decisions."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def create(address: dict[str, Any], evidence: list[dict[str, Any]], outcome: dict[str, Any], evaluated_at: str) -> dict[str, Any]:
    """Create a reproducible audit record without storing target or assertion values."""
    evidence_digests = sorted(
        ({"evidence_id": item["evidence_id"], "digest": _digest(item)} for item in evidence),
        key=lambda item: (item["evidence_id"], item["digest"]),
    )
    record = {
        "schema_version": "ADDRESS-AUDIT-1.0",
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
    """Verify the record's required shape and self-addressed integrity."""
    if not isinstance(record, dict):
        return ["audit record must be an object"]
    required = {"schema_version", "address_id", "evaluated_at", "decision", "reason", "detail_digest", "evidence_digests", "audit_id"}
    missing = required - set(record)
    if missing:
        return ["missing required fields: " + ", ".join(sorted(missing))]
    if record["schema_version"] != "ADDRESS-AUDIT-1.0":
        return ["unsupported audit schema version"]
    if not isinstance(record["evidence_digests"], list) or any(set(item) != {"evidence_id", "digest"} for item in record["evidence_digests"]):
        return ["invalid evidence digest list"]
    payload = dict(record)
    actual = payload.pop("audit_id")
    expected = "audit:" + _digest(payload).removeprefix("sha256:")
    return [] if actual == expected else ["audit_id does not match canonical record hash"]
