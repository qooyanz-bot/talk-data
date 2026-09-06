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
    """Union of unresolved unknown slots and target_value.residual labels.

    Invariant (pre-verification):
    - Unresolved Address.unknown slots (abstain_if_unresolved / NOT_DERIVABLE /
      UNRESOLVED / RESIDUAL) always appear in resolution.residual.
    - If target_value.residual is a non-empty list, those labels are also listed
      (union). target_value.residual is therefore a subset of resolution.residual
      when both are lists of strings; never invent a filled value from either.
    - If target_value.residual is null, unknown labels still appear on READY.
    """
    seen: set[str] = set()
    residuals: list[str] = []

    def _add(label: str) -> None:
        if label not in seen:
            seen.add(label)
            residuals.append(label)

    unknown = address.get("unknown", [])
    if isinstance(unknown, list):
        for item in unknown:
            if not isinstance(item, dict):
                continue
            slot = item.get("slot")
            label = slot if isinstance(slot, str) and slot else "<unknown>"
            status = item.get("status")
            # Pre-verification never resolves unknowns; abstain-required and open statuses remain residual.
            if item.get("abstain_if_unresolved") is True or status in {"NOT_DERIVABLE", "UNRESOLVED", "RESIDUAL"}:
                _add(label)

    target = address.get("target_value")
    if isinstance(target, dict):
        tv_residual = target.get("residual")
        if isinstance(tv_residual, list):
            for item in tv_residual:
                if isinstance(item, str) and item:
                    _add(item)
        # target_value.residual never supplies a filled value in this runtime.
    return residuals



def _residual_ignoring_assertion_collisions(residual: list[str], evidence: Any) -> list[str]:
    """Return residual unchanged; assertion_key name collisions never fill slots.

    Evidence may assert the same string as an unknown.slot / residual label.
    That collision is never treated as resolving the slot: residual stays listed,
    and assertion_value is never bound into resolution.value.
    """
    # Touch the collision set so callers/tests can rely on the helper existing,
    # while deliberately not removing any labels.
    _ = evidence_contract.assertion_key_set(evidence) & set(residual)
    return list(residual)


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
    """Decide whether verification may proceed; never returns a target Value.

    READY_FOR_VERIFICATION requires evidence independence == CONTRACTED (metadata
    separation only). This gate never upgrades past CONTRACTED and never claims
    semantic independence / AUDITED / INDEPENDENT from path IDs alone.
    """
    address_errors = address_runtime.validate(address)
    residual = _unresolved_residuals(address) if isinstance(address, dict) else []
    if address_errors:
        return _result("ABSTAIN", "ADDRESS_INVALID", address_errors, residual)
    minimum = address["evidence_requirements"].get("minimum_sources", 2)
    contract = evidence_contract.assess(evidence, minimum)
    if not contract["accepted"]:
        return _result("ABSTAIN", "EVIDENCE_REJECTED", contract["reasons"], residual)
    # accepted=True from this runtime means independence is CONTRACTED only.
    if contract.get("independence") != evidence_contract.INDEPENDENCE_CONTRACTED:
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
        if isinstance(item, dict) and "assertion_key" in item and "assertion_value" in item:
            assertions.setdefault(str(item["assertion_key"]), set()).add(str(item["assertion_value"]))
    conflicts = sorted(key for key, values in assertions.items() if len(values) > 1)
    if conflicts:
        return _result("ABSTAIN", "CONTRADICTION", conflicts, residual)
    # Address may require AUDITED semantic independence; this runtime cannot grant it.
    required_independence = address["evidence_requirements"].get("semantic_independence")
    if required_independence == "AUDITED":
        return _result(
            "ABSTAIN",
            "SEMANTIC_INDEPENDENCE_UNMET",
            [
                "Address.evidence_requirements.semantic_independence is AUDITED but "
                "evidence independence is only CONTRACTED; audited independence unmet",
                "independence=CONTRACTED",
            ],
            residual,
        )
    # Residual is Address-derived only; assertion_key collisions never fill slots.
    residual = _residual_ignoring_assertion_collisions(residual, evidence)
    # UNVERIFIED or CONTRACTED requirement + CONTRACTED evidence → READY; value stays null.
    return _result("READY_FOR_VERIFICATION", "CONTRACTED_EVIDENCE", contract["reasons"], residual)
