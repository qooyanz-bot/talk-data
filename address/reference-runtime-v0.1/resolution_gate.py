"""Conservative pre-verification gate for an Address and its evidence bundle."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
from typing import Any

import address_runtime
import evidence_contract


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def _max_age(requirement: Any) -> timedelta | None:
    if not isinstance(requirement, dict) or not isinstance(requirement.get("max_age"), str):
        return None
    match = re.fullmatch(r"P(\d+)D", requirement["max_age"])
    return timedelta(days=int(match.group(1))) if match else None


def resolve(address: Any, evidence: Any, now: str) -> dict[str, Any]:
    """Decide whether verification may proceed; never returns a target Value."""
    address_errors = address_runtime.validate(address)
    if address_errors:
        return {"decision": "ABSTAIN", "reason": "ADDRESS_INVALID", "details": address_errors, "value": None}
    minimum = address["evidence_requirements"].get("minimum_sources", 2)
    contract = evidence_contract.assess(evidence, minimum)
    if not contract["accepted"]:
        return {"decision": "ABSTAIN", "reason": "EVIDENCE_REJECTED", "details": contract["reasons"], "value": None}
    max_age = _max_age(address["freshness_requirement"])
    if max_age is None:
        return {"decision": "ABSTAIN", "reason": "FRESHNESS_REQUIREMENT_INVALID", "details": [], "value": None}
    try:
        current = _parse_time(now)
        stale = [item["evidence_id"] for item in evidence if current - _parse_time(item["observed_at"]) > max_age]
    except (TypeError, ValueError):
        return {"decision": "ABSTAIN", "reason": "EVIDENCE_TIME_INVALID", "details": [], "value": None}
    if stale:
        return {"decision": "ABSTAIN", "reason": "EVIDENCE_STALE", "details": stale, "value": None}
    assertions: dict[str, set[str]] = {}
    for item in evidence:
        if "assertion_key" in item and "assertion_value" in item:
            assertions.setdefault(str(item["assertion_key"]), set()).add(str(item["assertion_value"]))
    conflicts = sorted(key for key, values in assertions.items() if len(values) > 1)
    if conflicts:
        return {"decision": "ABSTAIN", "reason": "CONTRADICTION", "details": conflicts, "value": None}
    return {
        "decision": "READY_FOR_VERIFICATION",
        "reason": "CONTRACTED_EVIDENCE",
        "details": contract["reasons"],
        "value": None,
    }
