"""Dependency-free safety validator for Addressable Concept Architecture v0.1."""

from __future__ import annotations

import hashlib
import json
import sys
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
    if set(address["dimensions"]) != DIMENSIONS:
        errors.append("dimensions must contain exactly the ten declared computation axes")
    concept = address["concept"]
    if not isinstance(concept, dict) or not all(isinstance(concept.get(k), str) and concept[k] for k in ("id", "version", "definition_ref")):
        errors.append("concept requires non-empty id, version, and definition_ref")
    if not isinstance(address["world_id"], str) or not address["world_id"].startswith(("world:synthetic-", "world:real:")):
        errors.append("world_id must start with world:synthetic- or world:real:")
    if not isinstance(address["confidence_threshold"], (int, float)) or not 0 <= address["confidence_threshold"] <= 1:
        errors.append("confidence_threshold must be between 0 and 1")
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
    capabilities = address["capability_scope"]
    if not isinstance(capabilities, list) or not all(isinstance(x, str) for x in capabilities):
        errors.append("capability_scope must be a list of strings")
    else:
        lowered = " ".join(capabilities).lower()
        if any(token in lowered for token in FORBIDDEN_CAPABILITY_TOKENS):
            errors.append("capability_scope contains a prohibited secret, bypass, or direct-future operation")
        if address["world_id"].startswith("world:real:") and not set(capabilities).issubset(REAL_CAPABILITIES):
            errors.append("real-world Address may use only declared public/authorized read and verify capabilities")
    if address["address_id"] != canonical_id(address):
        errors.append("address_id does not match canonical payload hash")
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
