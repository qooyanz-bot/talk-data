"""Content-addressed, value-free audit records for Address resolution decisions."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _evidence_digest_entries(evidence: Any) -> list[dict[str, str]]:
    """Build sorted digest entries; malformed evidence never raises."""
    if not isinstance(evidence, list):
        return []
    entries: list[dict[str, str]] = []
    for item in evidence:
        if not isinstance(item, dict):
            continue
        evidence_id = item.get("evidence_id")
        if not isinstance(evidence_id, str):
            continue
        entries.append({"evidence_id": evidence_id, "digest": _digest(item)})
    return sorted(entries, key=lambda item: (item["evidence_id"], item["digest"]))


def create(address: dict[str, Any], evidence: list[dict[str, Any]], outcome: dict[str, Any], evaluated_at: str) -> dict[str, Any]:
    """Create a reproducible audit record without storing target or assertion values.

    Malformed evidence (non-list, non-dict items, missing/non-str evidence_id) is
    rejected by omission rather than raising KeyError/TypeError.
    """
    evidence_digests = _evidence_digest_entries(evidence)
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
    if not isinstance(record["evidence_digests"], list) or any(
        not isinstance(item, dict) or set(item) != {"evidence_id", "digest"}
        for item in record["evidence_digests"]
    ):
        return ["invalid evidence digest list"]
    payload = dict(record)
    actual = payload.pop("audit_id")
    expected = "audit:" + _digest(payload).removeprefix("sha256:")
    return [] if actual == expected else ["audit_id does not match canonical record hash"]
