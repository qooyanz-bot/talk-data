"""Dependency-free safety validator for Addressable Concept Architecture v0.1."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = frozenset({
    "address_id", "concept", "goal", "unknown", "entities", "relations", "dimensions",
    "time_range", "world_id", "state_constraints", "evidence_requirements",
    "confidence_threshold", "contradiction_policy", "freshness_requirement", "memory_scope",
    "capability_scope", "target_value", "lineage",
})
DIMENSIONS = frozenset({
    "concept", "state", "goal", "binding", "relation", "context", "temporal", "owner",
    "dependency", "provenance"
})
# Schema-documentation subset for real-domain Addresses (architecture); this runtime
# rejects world:real:* at validate time (world_scope=SYNTHETIC_ONLY). Kept for docs only.
REAL_CAPABILITIES = frozenset({"read:declared-public-data", "read:declared-authorized-data", "verify:declared-schema"})
FORBIDDEN_CAPABILITY_TOKENS = frozenset({"secret", "credential", "password", "private_key", "decrypt", "bypass", "hidden_person", "future_direct"})
WORLD_SYNTHETIC_PREFIX = "world:synthetic-"
WORLD_REAL_PREFIX = "world:real:"
# Closed enum for Address.evidence_requirements.semantic_independence (validate rejects others).
SEMANTIC_INDEPENDENCE_ALLOWED = frozenset({"UNVERIFIED", "CONTRACTED", "AUDITED"})
# Closed enum for Address.contradiction_policy (validate rejects others).
CONTRADICTION_POLICY_ALLOWED = frozenset({"STOP_AND_REPORT_CONFLICT"})
# Closed enum for Address.unknown[].status (from architecture / resolution_gate residuals).
UNKNOWN_STATUS_ALLOWED = frozenset({"NOT_DERIVABLE", "UNRESOLVED", "RESIDUAL", "OPEN"})
# Canonical serialization for address_id: sorted keys, compact separators, UTF-8.
# Key order and insignificant whitespace in source JSON must not change address_id.
CANONICAL_JSON_SEPARATORS = (",", ":")


def canonical_dumps(payload: dict[str, Any]) -> str:
    """Serialize Address payload for hashing: sort_keys=True, separators=(',', ':').

    This is the sole canonical form used by canonical_id. Reordering object keys or
    changing whitespace outside string values must not change the digest.
    """
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=CANONICAL_JSON_SEPARATORS,
    )


def canonical_id(address: dict[str, Any]) -> str:
    """Return the content address with address_id blanked to avoid self-reference.

    Hash input is canonical_dumps over the Address with address_id set to null.
    """
    payload = dict(address)
    payload["address_id"] = None
    encoded = canonical_dumps(payload).encode("utf-8")
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
    world_id = address["world_id"]
    if not isinstance(world_id, str):
        errors.append("world_id must be a non-empty string starting with world:synthetic-")
    elif world_id.startswith(WORLD_REAL_PREFIX):
        errors.append(
            "world_id world:real:* is INVALID in this runtime "
            "(world_scope=SYNTHETIC_ONLY; real-domain Addresses are rejected at schema validation)"
        )
    elif not world_id.startswith(WORLD_SYNTHETIC_PREFIX):
        errors.append("world_id must start with world:synthetic-")
    elif not world_id[len(WORLD_SYNTHETIC_PREFIX):]:
        errors.append("world_id must include a non-empty suffix after world:synthetic-")
    if isinstance(address["confidence_threshold"], bool) or not isinstance(address["confidence_threshold"], (int, float)) or not 0 <= address["confidence_threshold"] <= 1:
        errors.append("confidence_threshold must be between 0 and 1")
    goal = address["goal"]
    if not isinstance(goal, dict):
        errors.append("goal requires non-empty string id and success_criteria list of non-empty strings")
    else:
        if not isinstance(goal.get("id"), str) or not goal["id"]:
            errors.append("goal.id must be a non-empty string")
        criteria = goal.get("success_criteria")
        if not isinstance(criteria, list) or not all(isinstance(item, str) and item for item in criteria):
            errors.append("goal.success_criteria must be a list of non-empty strings")
    entities = address["entities"]
    if not isinstance(entities, list) or not all(isinstance(item, dict) for item in entities):
        errors.append("entities must be a list of objects")
    else:
        for index, item in enumerate(entities):
            if not isinstance(item.get("id"), str) or not item["id"]:
                errors.append(f"entities[{index}].id must be a non-empty string")
            if not isinstance(item.get("type"), str) or not item["type"]:
                errors.append(f"entities[{index}].type must be a non-empty string")
            if "binding" in item and (not isinstance(item.get("binding"), str) or not item["binding"]):
                errors.append(f"entities[{index}].binding must be a non-empty string when present")
    relations = address["relations"]
    if not isinstance(relations, list) or not all(isinstance(item, dict) for item in relations):
        errors.append("relations must be a list of objects")
    else:
        for index, item in enumerate(relations):
            for key in ("predicate", "subject", "object"):
                if not isinstance(item.get(key), str) or not item[key]:
                    errors.append(f"relations[{index}].{key} must be a non-empty string")
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
    constraints = address["state_constraints"]
    if not isinstance(constraints, list) or not all(isinstance(item, str) and item for item in constraints):
        errors.append("state_constraints must be a list of non-empty strings")
    evidence = address["evidence_requirements"]
    if not isinstance(evidence, dict) or not isinstance(evidence.get("law_assumption"), str) or not evidence["law_assumption"]:
        errors.append("evidence_requirements.law_assumption must be explicit")
    if not isinstance(evidence, dict) or evidence.get("provenance_required") is not True:
        errors.append("evidence_requirements.provenance_required must be true")
    if isinstance(evidence, dict):
        si = evidence.get("semantic_independence")
        if not isinstance(si, str) or si not in SEMANTIC_INDEPENDENCE_ALLOWED:
            errors.append(
                "evidence_requirements.semantic_independence must be one of "
                "UNVERIFIED, CONTRACTED, AUDITED"
            )
        if "minimum_sources" in evidence:
            minimum_sources = evidence["minimum_sources"]
            if isinstance(minimum_sources, bool) or not isinstance(minimum_sources, int) or minimum_sources < 1:
                errors.append("evidence_requirements.minimum_sources must be an int >= 1 when present")
    policy = address.get("contradiction_policy")
    if not isinstance(policy, str) or policy not in CONTRADICTION_POLICY_ALLOWED:
        errors.append(
            f"contradiction_policy must be one of {', '.join(sorted(CONTRADICTION_POLICY_ALLOWED))}"
        )
    target = address["target_value"]
    if not isinstance(target, dict):
        errors.append("target_value must be a dict")
    else:
        if target.get("no_speculation") is not True:
            errors.append("target_value.no_speculation must be true")
        tv_type = target.get("type")
        if not isinstance(tv_type, str) or not tv_type:
            errors.append("target_value.type must be a non-empty string")
        if target.get("value") is not None:
            errors.append("target_value.value must be null")
        residual = target.get("residual")
        if residual is not None and not isinstance(residual, list):
            errors.append("target_value.residual must be null or a list")
        elif isinstance(residual, list):
            if not all(isinstance(item, str) and item for item in residual):
                errors.append("target_value.residual must be a list of non-empty strings")
            elif residual and target.get("value") is not None:
                errors.append("target_value.value must be null when residual is non-empty")
    unknown = address["unknown"]
    if not isinstance(unknown, list) or not all(isinstance(item, dict) for item in unknown):
        errors.append("unknown must be a list of objects")
    else:
        for index, item in enumerate(unknown):
            if item.get("abstain_if_unresolved") is not True:
                errors.append(f"unknown[{index}] must require abstention when unresolved")
            if not isinstance(item.get("slot"), str) or not item["slot"]:
                errors.append(f"unknown[{index}].slot must be a non-empty string")
            status = item.get("status")
            if not isinstance(status, str) or status not in UNKNOWN_STATUS_ALLOWED:
                errors.append(
                    f"unknown[{index}].status must be one of "
                    "NOT_DERIVABLE, UNRESOLVED, RESIDUAL, OPEN"
                )
    lineage = address["lineage"]
    if not isinstance(lineage, dict):
        errors.append("lineage requires input_hashes")
    else:
        if not isinstance(lineage.get("input_hashes"), list):
            errors.append("lineage requires input_hashes")
        elif not all(isinstance(item, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", item) for item in lineage["input_hashes"]):
            errors.append("lineage input_hashes must use sha256:<64 lowercase hex>")
        for key in ("protocol_sha", "schema_sha", "runtime_sha"):
            value = lineage.get(key)
            if value is not None and (not isinstance(value, str) or not value):
                errors.append(f"lineage.{key} must be null or a non-empty string")
        if lineage.get("result_sha") is not None:
            errors.append("lineage.result_sha must be null")
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
    if not isinstance(capabilities, list) or not all(isinstance(x, str) and x for x in capabilities):
        errors.append("capability_scope must be a list of non-empty strings")
    else:
        lowered = " ".join(capabilities).lower()
        if any(token in lowered for token in FORBIDDEN_CAPABILITY_TOKENS):
            errors.append("capability_scope contains a prohibited secret, bypass, or direct-future operation")
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
