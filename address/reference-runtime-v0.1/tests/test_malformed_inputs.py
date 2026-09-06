import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402


class MalformedInputTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.valid = json.loads(fixture.read_text(encoding="utf-8"))
        self.valid["address_id"] = address_runtime.canonical_id(self.valid)

    def test_malformed_fields_return_errors_without_raising(self):
        cases = [
            ("dimensions", 7),
            ("time_range", {"start": "not-a-time", "end": "also-not-a-time"}),
            ("capability_scope", None),
            ("confidence_threshold", True),
            ("entities", {"not": "a list"}),
        ]
        for field, value in cases:
            with self.subTest(field=field):
                address = copy.deepcopy(self.valid)
                address[field] = value
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)

    def test_reversed_time_range_is_rejected(self):
        address = copy.deepcopy(self.valid)
        address["time_range"] = {"start": "2026-02-01T00:00:00Z", "end": "2026-01-01T00:00:00Z"}
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertIn("time_range start must not be after end", address_runtime.validate(address))
