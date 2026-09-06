import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402


class AddressRuntimeTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)

    def test_valid_synthetic_address(self):
        self.assertEqual(address_runtime.validate(self.address), [])

    def test_hash_tamper_is_rejected(self):
        self.address["goal"]["id"] = "goal:tampered"
        self.assertIn("address_id does not match canonical payload hash", address_runtime.validate(self.address))

    def test_real_secret_capability_is_rejected(self):
        self.address["world_id"] = "world:real:example"
        self.address["capability_scope"] = ["read:declared-public-data", "read:secret-vault"]
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        errors = address_runtime.validate(self.address)
        self.assertTrue(any("prohibited" in error for error in errors))
        self.assertTrue(any("real-world" in error for error in errors))

    def test_unknown_without_abstain_is_rejected(self):
        self.address["unknown"][0]["abstain_if_unresolved"] = False
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.assertTrue(any("unknown slot" in error for error in address_runtime.validate(self.address)))


if __name__ == "__main__":
    unittest.main()
