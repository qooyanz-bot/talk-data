import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import response_contract  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}", "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z", "assertion_key": "target", "assertion_value": "verified",
    }


class ResponseContractTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.response = address_cli.evaluate(self.address, [evidence(1), evidence(2)], "2026-09-06T00:00:00Z")

    def test_cli_response_satisfies_contract(self):
        self.assertEqual(response_contract.validate(self.response), [])

    def test_non_null_value_is_rejected(self):
        self.response["resolution"]["value"] = "invented-value"
        self.assertIn("public resolution value must be null", response_contract.validate(self.response))

    def test_audit_reason_mismatch_is_rejected(self):
        self.response["generated_audit"]["reason"] = "OTHER"
        self.assertTrue(any("generated_audit" in error for error in response_contract.validate(self.response)))

    def test_invalid_protocol_claim_status_is_rejected(self):
        self.response["protocol_claim"] = {"status": "ALLOWED_AS_RESULT_FAKE"}
        self.assertIn("protocol_claim status is invalid", response_contract.validate(self.response))
