#!/usr/bin/env python3
"""Rebuild READY / ABSTAIN / CONTRADICTION / EVIDENCE_STALE / SEMANTIC_INDEPENDENCE_UNMET contract goldens from evaluate().

Fixed Address + evidence + now inputs keep digests reproducible without hand edits.
Run from repository root:

  python address/reference-runtime-v0.1/tools/regenerate_contract_goldens.py

Or from this package directory:

  python tools/regenerate_contract_goldens.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import address_cli  # noqa: E402
import address_runtime  # noqa: E402

NOW = "2026-09-06T00:00:00Z"
FIXTURES = ROOT / "fixtures"
# Older than address freshness_requirement.max_age P30D relative to NOW.
STALE_OBSERVED_AT = "2026-07-01T00:00:00Z"


def _load_address() -> dict[str, Any]:
    address = json.loads((FIXTURES / "valid_synthetic_address.json").read_text(encoding="utf-8"))
    address["address_id"] = address_runtime.canonical_id(address)
    return address


def _evidence(index: int, assertion_value: str = "verified", **overrides: Any) -> dict[str, Any]:
    item: dict[str, Any] = {
        "evidence_id": f"e-{index}",
        "claim_hash": f"claim-{index}",
        "path_id": f"path-{index}",
        "authority_id": f"authority-{index}",
        "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z",
        "assertion_key": "target:sample",
        "assertion_value": assertion_value,
    }
    item.update(overrides)
    return item


def golden_specs() -> list[tuple[str, list[dict[str, Any]], str, str, str | None]]:
    """Return (filename, evidence, expected_decision, expected_reason, semantic_independence_or_None).

    None keeps the fixture Address (UNVERIFIED). AUDITED builds the
    SEMANTIC_INDEPENDENCE_UNMET golden: contracted evidence cannot satisfy an
    audited independence requirement.
    """
    return [
        (
            "golden_contract_ok_response.json",
            [_evidence(1), _evidence(2)],
            "READY_FOR_VERIFICATION",
            "CONTRACTED_EVIDENCE",
            None,
        ),
        (
            "golden_contract_abstain_response.json",
            [_evidence(1), _evidence(2, semantic_law_id="law-1")],
            "ABSTAIN",
            "EVIDENCE_REJECTED",
            None,
        ),
        (
            "golden_contract_contradiction_response.json",
            [_evidence(1), _evidence(2, assertion_value="rejected")],
            "ABSTAIN",
            "CONTRADICTION",
            None,
        ),
        (
            "golden_contract_stale_response.json",
            [
                _evidence(1, observed_at=STALE_OBSERVED_AT),
                _evidence(2, observed_at=STALE_OBSERVED_AT),
            ],
            "ABSTAIN",
            "EVIDENCE_STALE",
            None,
        ),
        (
            "golden_contract_semantic_independence_unmet_response.json",
            [_evidence(1), _evidence(2)],
            "ABSTAIN",
            "SEMANTIC_INDEPENDENCE_UNMET",
            "AUDITED",
        ),
    ]


def _address_for_spec(semantic_independence: str | None) -> dict[str, Any]:
    address = copy.deepcopy(_load_address())
    if semantic_independence is not None:
        address["evidence_requirements"]["semantic_independence"] = semantic_independence
        address["address_id"] = address_runtime.canonical_id(address)
    return address


def build_goldens() -> dict[str, dict[str, Any]]:
    built: dict[str, dict[str, Any]] = {}
    for filename, evidence, decision, reason, semantic_independence in golden_specs():
        address = _address_for_spec(semantic_independence)
        response = address_cli.evaluate(address, evidence, NOW)
        resolution = response["resolution"]
        if resolution["decision"] != decision or resolution["reason"] != reason:
            raise RuntimeError(
                f"{filename}: expected {decision}/{reason}, got "
                f"{resolution['decision']}/{resolution['reason']}"
            )
        if resolution["value"] is not None:
            raise RuntimeError(f"{filename}: value must be null")
        built[filename] = response
    return built


def write_goldens(built: dict[str, dict[str, Any]]) -> None:
    for filename, response in built.items():
        path = FIXTURES / filename
        path.write_text(
            json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {path.relative_to(ROOT.parent.parent) if ROOT.parent.parent.exists() else path}")


def main() -> int:
    built = build_goldens()
    write_goldens(built)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
