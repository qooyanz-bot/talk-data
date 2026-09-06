import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}", "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z", "assertion_key": "target", "assertion_value": "verified",
    }


class AddressCliTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.bundle = [evidence(1), evidence(2)]

    def test_evaluate_generates_value_free_audit(self):
        result = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["resolution"]["value"])
        self.assertTrue(result["generated_audit"]["audit_id"].startswith("audit:"))

    def test_evaluate_replays_supplied_audit(self):
        first = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        second = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z", first["generated_audit"])
        self.assertEqual(second["replay"]["status"], "REPLAY_VERIFIED")

    def test_cli_loads_json_files(self):
        with tempfile.TemporaryDirectory() as directory:
            address_path = Path(directory) / "address.json"
            evidence_path = Path(directory) / "evidence.json"
            address_path.write_text(json.dumps(self.address), encoding="utf-8")
            evidence_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            result = address_cli.evaluate(json.loads(address_path.read_text()), json.loads(evidence_path.read_text()), "2026-09-06T00:00:00Z")
            self.assertEqual(result["resolution"]["decision"], "READY_FOR_VERIFICATION")

    def test_evaluate_non_list_evidence_does_not_crash(self):
        result = address_cli.evaluate(self.address, {"not": "a list"}, "2026-09-06T00:00:00Z")
        self.assertEqual(result["resolution"]["decision"], "ABSTAIN")
        self.assertIsNone(result["resolution"]["value"])
        self.assertIsInstance(result["generated_audit"], dict)
        self.assertEqual(result["generated_audit"]["evidence_digests"], [])


if __name__ == "__main__":
    unittest.main()
