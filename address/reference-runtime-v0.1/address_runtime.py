"""Dependency-free safety validator for Addressable Concept Architecture v0.1."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "address_id", "concept", "goal", "unknown", "entities", "relations", "dimensions",
    "time_range", "world_id", "state_constraints", "evidence_requirements",
    "confidence_threshold", "contradiction_policy", "freshness_requirement", "memory_scope",
    "capability_scope", "target_value", "lineage",
}
DIMENSIONS = {"concept", "state", "goal", "binding", "relation", "context", "temporal", "owner", "dependency", "provenance"}
REAL_CAPABILITIES = {"read:declared-public-data", "read:declared-authorized-data", "verify:declared-schema"}
FORBIDDEN_CAPABILITY_TOKENS = {"secret", "credential", "password", "private_key", "decrypt", "bypass", "hidden_person", "future_direct"}


def canonical_id(address: dict[str, Any]) -> str:
    """Return the content address with address_id blanked to avoid self-reference."""
    payload = dict(address)
    payload["address_id"] = None
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "addr:sha256:" + hashlib.sha256(encoded).hexdigest()


def validate(address: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(address, dict):
        return ["address must be a JSON object"]
    missing = REQUIRED_FIELDS - set(address)
    if missing:
        errors.append("missing required fields: " + ", ".join(sorted(missing)))
        return errors
    dimensions = address["dimensions"]
    if not isinstance(dimensions, dict) or set(dimensions) != DIMENSIONS:
        errors.append("dimensions must contain exactly the ten declared computation axes")
    elif not all(isinstance(value, str) and value for value in dimensions.values()):
        errors.append("dimension values must be non-empty strings")
    concept = address["concept"]
    if not isinstance(concept, dict) or not all(isinstance(concept.get(k), str) and concept[k] for k in ("id", "version", "definition_ref")):
        errors.append("concept requires non-empty id, version, and definition_ref")
    if not isinstance(address["world_id"], str) or not address["world_id"].startswith(("world:synthetic-", "world:real:")):
        errors.append("world_id must start with world:synthetic- or world:real:")
    if isinstance(address["confidence_threshold"], bool) or not isinstance(address["confidence_threshold"], (int, float)) or not 0 <= address["confidence_threshold"] <= 1:
        errors.append("confidence_threshold must be between 0 and 1")
    goal = address["goal"]
    if not isinstance(goal, dict) or not isinstance(goal.get("id"), str) or not isinstance(goal.get("success_criteria"), list):
        errors.append("goal requires string id and success_criteria list")
    if not isinstance(address["entities"], list) or not all(isinstance(item, dict) for item in address["entities"]):
        errors.append("entities must be a list of objects")
    if not isinstance(address["relations"], list) or not all(isinstance(item, dict) for item in address["relations"]):
        errors.append("relations must be a list of objects")
    time_range = address["time_range"]
    try:
        if not isinstance(time_range, dict) or not isinstance(time_range.get("start"), str) or not isinstance(time_range.get("end"), str):
            raise ValueError
        start = datetime.fromisoformat(time_range["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(time_range["end"].replace("Z", "+00:00"))
        if start > end:
            errors.append("time_range start must not be after end")
    except ValueError:
        errors.append("time_range requires ISO-8601 start and end")
    if not isinstance(address["state_constraints"], list) or not all(isinstance(item, str) for item in address["state_constraints"]):
        errors.append("state_constraints must be a list of strings")
    evidence = address["evidence_requirements"]
    if not isinstance(evidence, dict) or not isinstance(evidence.get("law_assumption"), str) or not evidence["law_assumption"]:
        errors.append("evidence_requirements.law_assumption must be explicit")
    if not isinstance(evidence, dict) or evidence.get("provenance_required") is not True:
        errors.append("evidence_requirements.provenance_required must be true")
    if address["contradiction_policy"] != "STOP_AND_REPORT_CONFLICT":
        errors.append("contradiction_policy must stop and report conflict")
    target = address["target_value"]
    if not isinstance(target, dict) or target.get("no_speculation") is not True:
        errors.append("target_value.no_speculation must be true")
    unknown = address["unknown"]
    if not isinstance(unknown, list) or any(not isinstance(item, dict) or item.get("abstain_if_unresolved") is not True for item in unknown):
        errors.append("every unknown slot must require abstention when unresolved")
    lineage = address["lineage"]
    if not isinstance(lineage, dict) or not isinstance(lineage.get("input_hashes"), list):
        errors.append("lineage requires input_hashes")
    elif not all(isinstance(item, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", item) for item in lineage["input_hashes"]):
        errors.append("lineage input_hashes must use sha256:<64 lowercase hex>")
    memory_scope = address["memory_scope"]
    if not isinstance(memory_scope, str):
        errors.append("memory_scope must be a non-empty string")
    else:
        memory_terms = {term.strip() for term in memory_scope.split(",") if term.strip()}
        if not {"authorized", "versioned", "revocable"}.issubset(memory_terms):
            errors.append("memory_scope must include authorized, versioned, and revocable")
    freshness = address["freshness_requirement"]
    if not isinstance(freshness, dict) or not isinstance(freshness.get("max_age"), str) or not re.fullmatch(r"P\d+D", freshness["max_age"]):
        errors.append("freshness_requirement.max_age must use P<n>D")
    capabilities = address["capability_scope"]
    if not isinstance(capabilities, list) or not all(isinstance(x, str) for x in capabilities):
        errors.append("capability_scope must be a list of strings")
    else:
        lowered = " ".join(capabilities).lower()
        if any(token in lowered for token in FORBIDDEN_CAPABILITY_TOKENS):
            errors.append("capability_scope contains a prohibited secret, bypass, or direct-future operation")
        if address["world_id"].startswith("world:real:") and not set(capabilities).issubset(REAL_CAPABILITIES):
            errors.append("real-world Address may use only declared public/authorized read and verify capabilities")
    try:
        if not isinstance(address["address_id"], str) or address["address_id"] != canonical_id(address):
            errors.append("address_id does not match canonical payload hash")
    except (TypeError, ValueError):
        errors.append("address must contain JSON-serializable values")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: address_runtime.py ADDRESS.json")
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "INVALID", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    errors = validate(data)
    print(json.dumps({"status": "VALID" if not errors else "INVALID", "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
