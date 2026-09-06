import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402
import audit_log  # noqa: E402
import resolution_gate  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": "2026-09-05T00:00:00Z",
        "assertion_key": "target", "assertion_value": "not logged",
    }


class AuditLogTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.evidence = [evidence(1), evidence(2)]
        self.outcome = resolution_gate.resolve(self.address, self.evidence, "2026-09-06T00:00:00Z")

    def test_audit_record_verifies(self):
        record = audit_log.create(self.address, self.evidence, self.outcome, "2026-09-06T00:00:00Z")
        self.assertEqual(audit_log.verify(record), [])
        self.assertNotIn("not logged", json.dumps(record))
        self.assertIsNone(self.outcome["value"])

    def test_evidence_order_does_not_change_audit_id(self):
        forward = audit_log.create(self.address, self.evidence, self.outcome, "2026-09-06T00:00:00Z")
        reverse = audit_log.create(self.address, list(reversed(self.evidence)), self.outcome, "2026-09-06T00:00:00Z")
        self.assertEqual(forward["audit_id"], reverse["audit_id"])

    def test_tampering_is_detected(self):
        record = audit_log.create(self.address, self.evidence, self.outcome, "2026-09-06T00:00:00Z")
        record["reason"] = "TAMPERED"
        self.assertIn("audit_id does not match", audit_log.verify(record)[0])

    def test_malformed_digest_item_is_rejected_without_raising(self):
        record = audit_log.create(self.address, self.evidence, self.outcome, "2026-09-06T00:00:00Z")
        record["evidence_digests"] = ["not-an-object"]
        self.assertEqual(audit_log.verify(record), ["invalid evidence digest list"])

    def test_create_skips_missing_evidence_id_without_raising(self):
        malformed = [self.evidence[0], {"claim_hash": "orphan", "path_id": "p"}, self.evidence[1]]
        record = audit_log.create(self.address, malformed, self.outcome, "2026-09-06T00:00:00Z")
        self.assertEqual(audit_log.verify(record), [])
        self.assertEqual([item["evidence_id"] for item in record["evidence_digests"]], ["e-1", "e-2"])

    def test_create_treats_non_list_evidence_as_empty(self):
        record = audit_log.create(self.address, {"not": "a list"}, self.outcome, "2026-09-06T00:00:00Z")
        self.assertEqual(audit_log.verify(record), [])
        self.assertEqual(record["evidence_digests"], [])

    def test_create_skips_non_dict_and_non_str_evidence_id(self):
        malformed = [self.evidence[0], "string-item", {"evidence_id": 7, "claim_hash": "x"}, None]
        record = audit_log.create(self.address, malformed, self.outcome, "2026-09-06T00:00:00Z")
        self.assertEqual(audit_log.verify(record), [])
        self.assertEqual([item["evidence_id"] for item in record["evidence_digests"]], ["e-1"])


if __name__ == "__main__":
    unittest.main()
