import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402
import resolution_gate  # noqa: E402


def evidence(index: int, observed_at: str = "2026-09-05T00:00:00Z") -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": observed_at,
        "assertion_key": "target:sample", "assertion_value": "verified",
    }


class ResolutionGateTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.bundle = [evidence(1), evidence(2)]

    def test_contracted_fresh_evidence_is_ready_but_value_is_null(self):
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])

    def test_stale_evidence_abstains(self):
        result = resolution_gate.resolve(self.address, self.bundle, "2026-10-07T00:00:00Z")
        self.assertEqual(result["reason"], "EVIDENCE_STALE")

    def test_contradictory_assertion_abstains(self):
        self.bundle[1]["assertion_value"] = "rejected"
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["reason"], "CONTRADICTION")

    def test_shared_law_abstains_before_verification(self):
        self.bundle[1]["semantic_law_id"] = self.bundle[0]["semantic_law_id"]
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["reason"], "EVIDENCE_REJECTED")

    def test_ready_keeps_unknown_slots_as_residual_and_value_null(self):
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])
        # Typed binding must not invent a filled slot payload.
        self.assertNotIn("filled", result)

    def test_ready_exposes_unknown_when_target_value_residual_is_null(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = None
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])

    def test_target_value_residual_labels_appear_in_resolution_residual(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["extra-slot", "continuity"]
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        # Union: unknown slots plus target_value.residual labels; never invent a filled value.
        self.assertIn("continuity", result["residual"])
        self.assertIn("extra-slot", result["residual"])
        for label in address["target_value"]["residual"]:
            self.assertIn(label, result["residual"])
        self.assertNotIn("filled", result)
        self.assertNotIn("value_filled", result)

    def test_target_value_residual_never_fills_value(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["open-slot"]
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertIsNone(result["value"])
        self.assertIn("open-slot", result["residual"])
        # Residual labels must not be treated as resolved payloads.
        self.assertNotEqual(result.get("value"), "open-slot")


if __name__ == "__main__":
    unittest.main()
