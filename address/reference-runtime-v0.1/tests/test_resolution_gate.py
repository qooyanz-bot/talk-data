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


if __name__ == "__main__":
    unittest.main()
