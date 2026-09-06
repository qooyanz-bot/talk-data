import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import response_contract  # noqa: E402


class GoldenCliOutputTests(unittest.TestCase):
    def setUp(self):
        self.golden = json.loads((ROOT / "fixtures" / "golden_cli_output.json").read_text(encoding="utf-8"))
        address = json.loads((ROOT / "fixtures" / self.golden["inputs"]["address_fixture"]).read_text(encoding="utf-8"))
        address["address_id"] = address_runtime.canonical_id(address)
        evidence = json.loads((ROOT / "fixtures" / self.golden["inputs"]["evidence_fixture"]).read_text(encoding="utf-8"))
        self.result = address_cli.evaluate(address, evidence, self.golden["inputs"]["now"])

    def test_public_contract_keys_and_value_null(self):
        for key in self.golden["required_top_level_keys"]:
            self.assertIn(key, self.result)
        resolution = self.result["resolution"]
        for key in self.golden["resolution"]["required_keys"]:
            self.assertIn(key, resolution)
        self.assertIn(resolution["decision"], set(self.golden["resolution"]["decision_set"]))
        self.assertEqual(resolution["decision"], self.golden["resolution"]["expected_decision"])
        self.assertEqual(resolution["reason"], self.golden["resolution"]["expected_reason"])
        self.assertIsNone(resolution["value"])
        self.assertEqual(response_contract.validate(self.result), [])

    def test_generated_audit_public_shape(self):
        audit = self.result["generated_audit"]
        for key in self.golden["generated_audit"]["required_keys"]:
            self.assertIn(key, audit)
        self.assertEqual(audit["schema_version"], self.golden["generated_audit"]["schema_version"])
        self.assertEqual(audit["decision"], self.result["resolution"]["decision"])
        self.assertEqual(audit["reason"], self.result["resolution"]["reason"])
        self.assertTrue(str(audit["audit_id"]).startswith("audit:"))

    def test_public_contract_regression_fails_on_missing_decision(self):
        broken = dict(self.result)
        broken["resolution"] = dict(self.result["resolution"])
        del broken["resolution"]["decision"]
        self.assertTrue(response_contract.validate(broken))


if __name__ == "__main__":
    unittest.main()
