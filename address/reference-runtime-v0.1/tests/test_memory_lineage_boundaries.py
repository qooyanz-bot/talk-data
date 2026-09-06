import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402


class MemoryLineageBoundaryTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)

    def test_unrevocable_memory_scope_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["memory_scope"] = "authorized, versioned"
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(any("memory_scope" in error for error in address_runtime.validate(address)))

    def test_non_hash_lineage_reference_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["lineage"]["input_hashes"] = ["file:unverified-source"]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(any("input_hashes" in error for error in address_runtime.validate(address)))

    def test_sha256_lineage_reference_is_accepted(self):
        address = copy.deepcopy(self.address)
        address["lineage"]["input_hashes"] = ["sha256:" + "a" * 64]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])
