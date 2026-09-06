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


def _unresolved_residuals(address: dict[str, Any]) -> list[str]:
    """Unknown slots stay residual through READY_FOR_VERIFICATION; never filled here."""
    unknown = address.get("unknown", [])
    if not isinstance(unknown, list):
        return []
    residuals: list[str] = []
    for item in unknown:
        if not isinstance(item, dict):
            continue
        slot = item.get("slot")
        label = slot if isinstance(slot, str) and slot else "<unknown>"
        status = item.get("status")
        # Pre-verification never resolves unknowns; abstain-required and open statuses remain residual.
        if item.get("abstain_if_unresolved") is True or status in {"NOT_DERIVABLE", "UNRESOLVED", "RESIDUAL"}:
            residuals.append(label)
    return residuals


def _result(decision: str, reason: str, details: list[Any], residual: list[str]) -> dict[str, Any]:
    # Typed binding: success stays READY_FOR_VERIFICATION with value=null; residuals stay unfilled.
    return {
        "decision": decision,
        "reason": reason,
        "details": details,
        "value": None,
        "residual": residual,
    }


def resolve(address: Any, evidence: Any, now: str) -> dict[str, Any]:
    """Decide whether verification may proceed; never returns a target Value."""
    address_errors = address_runtime.validate(address)
    residual = _unresolved_residuals(address) if isinstance(address, dict) else []
    if address_errors:
        return _result("ABSTAIN", "ADDRESS_INVALID", address_errors, residual)
    minimum = address["evidence_requirements"].get("minimum_sources", 2)
    contract = evidence_contract.assess(evidence, minimum)
    if not contract["accepted"]:
        return _result("ABSTAIN", "EVIDENCE_REJECTED", contract["reasons"], residual)
    max_age = _max_age(address["freshness_requirement"])
    if max_age is None:
        return _result("ABSTAIN", "FRESHNESS_REQUIREMENT_INVALID", [], residual)
    try:
        current = _parse_time(now)
        stale = [item["evidence_id"] for item in evidence if current - _parse_time(item["observed_at"]) > max_age]
    except (TypeError, ValueError):
        return _result("ABSTAIN", "EVIDENCE_TIME_INVALID", [], residual)
    if stale:
        return _result("ABSTAIN", "EVIDENCE_STALE", stale, residual)
    assertions: dict[str, set[str]] = {}
    for item in evidence:
        if "assertion_key" in item and "assertion_value" in item:
            assertions.setdefault(str(item["assertion_key"]), set()).add(str(item["assertion_value"]))
    conflicts = sorted(key for key, values in assertions.items() if len(values) > 1)
    if conflicts:
        return _result("ABSTAIN", "CONTRADICTION", conflicts, residual)
    return _result("READY_FOR_VERIFICATION", "CONTRACTED_EVIDENCE", contract["reasons"], residual)
