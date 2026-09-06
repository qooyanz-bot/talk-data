import copy
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

    def test_filled_target_value_is_rejected_without_raising(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["value"] = "discovered"
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(errors)
        self.assertTrue(any("target_value.value must be null" in error for error in errors))

    def test_missing_or_empty_target_value_type_is_rejected(self):
        for bad_type in ("", None, 12):
            with self.subTest(bad_type=bad_type):
                address = copy.deepcopy(self.address)
                if bad_type is None and "type" in address["target_value"]:
                    del address["target_value"]["type"]
                else:
                    address["target_value"]["type"] = bad_type
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)
                self.assertTrue(any("target_value.type" in error for error in errors))

    def test_non_null_lineage_result_sha_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["lineage"]["result_sha"] = "sha256:" + "b" * 64
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(errors)
        self.assertTrue(any("lineage.result_sha must be null" in error for error in errors))

    def test_valid_fixture_keeps_value_null_and_residual_unfilled(self):
        errors = address_runtime.validate(self.address)
        self.assertEqual(errors, [])
        self.assertIsNone(self.address["target_value"]["value"])
        residual = self.address["target_value"]["residual"]
        self.assertTrue(residual is None or residual == [])
        self.assertIsNone(self.address["lineage"]["result_sha"])

    def test_non_list_target_value_residual_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = "not-a-list"
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(any("target_value.residual" in error for error in errors))

    def test_nonempty_residual_with_null_value_is_accepted(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["continuity"]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])


if __name__ == "__main__":
    unittest.main()
