"""Validate the public, value-free response contract of the Address CLI."""

from __future__ import annotations

from typing import Any

import audit_log

DECISIONS = {"ABSTAIN", "READY_FOR_VERIFICATION"}
REPLAY_STATUSES = {"REPLAY_VERIFIED", "REPLAY_MISMATCH", "LINEAGE_MISMATCH", "INVALID_AUDIT"}


def validate(response: Any) -> list[str]:
    """Return contract violations; the public response must never contain a Value."""
    if not isinstance(response, dict):
        return ["response must be an object"]
    resolution = response.get("resolution")
    if not isinstance(resolution, dict):
        return ["resolution must be an object"]
    required = {"decision", "reason", "details", "value"}
    if required - set(resolution):
        return ["resolution missing required fields"]
    errors: list[str] = []
    if resolution["decision"] not in DECISIONS:
        errors.append("resolution decision is unknown")
    if resolution["value"] is not None:
        errors.append("public resolution value must be null")
    audit = response.get("generated_audit")
    if not isinstance(audit, dict):
        errors.append("generated_audit must be an object")
    else:
        errors.extend("generated_audit: " + error for error in audit_log.verify(audit))
        if audit.get("decision") != resolution["decision"] or audit.get("reason") != resolution["reason"]:
            errors.append("generated_audit decision or reason differs from resolution")
    if "replay" in response:
        replay = response["replay"]
        if not isinstance(replay, dict) or replay.get("status") not in REPLAY_STATUSES:
            errors.append("replay status is invalid")
        elif replay.get("value") is not None:
            errors.append("public replay value must be null")
    return errors
