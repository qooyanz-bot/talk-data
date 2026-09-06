"""Validate the public, value-free response contract of the Address CLI."""

from __future__ import annotations

from typing import Any

import audit_log
import decision_log
import protocol_claim_gate
import replay_verifier
import resolution_gate

# Single source: resolution_gate.DECISION_ALLOWED
DECISIONS = resolution_gate.DECISION_ALLOWED
# Single source: resolution_gate.REASON_ALLOWED
REASONS = resolution_gate.REASON_ALLOWED
# Single source: replay_verifier.REPLAY_STATUS_ALLOWED
REPLAY_STATUSES = replay_verifier.REPLAY_STATUS_ALLOWED
# Single source: protocol_claim_gate.CLAIM_STATUS_ALLOWED
PROTOCOL_CLAIM_STATUSES = protocol_claim_gate.CLAIM_STATUS_ALLOWED

# Single source: decision_log.REQUIRED_KEYS
DECISION_LOG_REQUIRED_KEYS = decision_log.REQUIRED_KEYS
# Single source: protocol_claim_gate.AUDITOR_HANDOFF_KEYS
DECISION_LOG_HANDOFF_KEYS = protocol_claim_gate.AUDITOR_HANDOFF_KEYS


def _nested_result_sha_errors(node: Any, path: str = "") -> list[str]:
    """Reject any nested lineage.result_sha that is not null in the public response."""
    errors: list[str] = []
    if isinstance(node, dict):
        lineage = node.get("lineage")
        if isinstance(lineage, dict) and lineage.get("result_sha") is not None:
            where = f"{path}.lineage" if path else "lineage"
            errors.append(f"{where}.result_sha must be null in pre-verification response")
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            errors.extend(_nested_result_sha_errors(value, child))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            errors.extend(_nested_result_sha_errors(item, f"{path}[{index}]"))
    return errors


def validate(response: Any) -> list[str]:
    """Return contract violations; the public response must never contain a Value."""
    if not isinstance(response, dict):
        return ["response must be an object"]
    resolution = response.get("resolution")
    if not isinstance(resolution, dict):
        return ["resolution must be an object"]
    required = {"decision", "reason", "details", "value", "residual"}
    if required - set(resolution):
        return ["resolution missing required fields"]
    errors: list[str] = []
    if resolution["decision"] not in DECISIONS:
        errors.append("resolution decision is unknown")
    if resolution["reason"] not in REASONS:
        errors.append("resolution reason is unknown")
    if resolution["value"] is not None:
        errors.append("public resolution value must be null")
    residual = resolution.get("residual")
    if not isinstance(residual, list):
        errors.append("resolution residual must be a list")
    elif not all(isinstance(item, str) and item for item in residual):
        errors.append("resolution residual must be a list of non-empty strings")
    elif residual and resolution["value"] is not None:
        errors.append("unresolved residual forbids a filled value")
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
    if "protocol_claim" in response:
        claim = response["protocol_claim"]
        if not isinstance(claim, dict) or claim.get("status") not in PROTOCOL_CLAIM_STATUSES:
            errors.append("protocol_claim status is invalid")
        elif claim.get("value") is not None:
            errors.append("public protocol_claim value must be null")
    if "decision_log" in response:
        log = response["decision_log"]
        if not isinstance(log, dict):
            errors.append("decision_log must be an object")
        else:
            if DECISION_LOG_REQUIRED_KEYS - set(log):
                errors.append("decision_log missing required fields")
            errors.extend("decision_log: " + error for error in decision_log.verify(log))
            if log.get("schema_version") != decision_log.SCHEMA_VERSION:
                errors.append("decision_log schema_version is invalid")
            if log.get("value") is not None:
                errors.append("public decision_log value must be null")
            if log.get("claim_status") not in PROTOCOL_CLAIM_STATUSES:
                errors.append("decision_log claim_status is invalid")
            handoff = log.get("auditor_handoff")
            if not isinstance(handoff, dict):
                errors.append("decision_log auditor_handoff must be an object")
            elif set(handoff) != DECISION_LOG_HANDOFF_KEYS:
                errors.append("decision_log auditor_handoff keys are invalid")
            unmet = log.get("unmet")
            if unmet is not None and (
                not isinstance(unmet, list) or not all(isinstance(item, str) for item in unmet)
            ):
                errors.append("decision_log unmet must be null or a list of strings")
            claim = response.get("protocol_claim")
            if isinstance(claim, dict) and claim.get("status") in PROTOCOL_CLAIM_STATUSES:
                if log.get("claim_status") != claim.get("status"):
                    errors.append("decision_log claim_status contradicts protocol_claim.status")
                if "reason" in claim and log.get("claim_reason") != claim.get("reason"):
                    errors.append("decision_log claim_reason contradicts protocol_claim.reason")
                if "unmet" in claim:
                    claim_unmet = claim.get("unmet")
                    log_unmet = log.get("unmet")
                    if not (
                        isinstance(claim_unmet, list)
                        and isinstance(log_unmet, list)
                        and sorted(claim_unmet) == sorted(log_unmet)
                    ):
                        errors.append("decision_log unmet contradicts protocol_claim.unmet")
    # Shape-based: forbid stamping lineage.result_sha anywhere in the public object.
    errors.extend(_nested_result_sha_errors(response))
    return errors
