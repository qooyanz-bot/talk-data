import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import evidence_contract  # noqa: E402


def record(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": "2026-09-06T00:00:00Z",
    }


class EvidenceContractTests(unittest.TestCase):
    def test_separated_metadata_is_contracted_not_audited(self):
        result = evidence_contract.assess([record(1), record(2)])
        self.assertEqual(result["status"], "CONTRACTED")
        self.assertTrue(result["accepted"])
        self.assertIn("unaudited", result["reasons"][0])

    def test_distinct_paths_with_shared_law_are_rejected(self):
        records = [record(1), record(2)]
        records[1]["semantic_law_id"] = records[0]["semantic_law_id"]
        result = evidence_contract.assess(records)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertTrue(any("semantic_law_id" in reason for reason in result["reasons"]))

    def test_shared_authority_is_rejected(self):
        records = [record(1), record(2)]
        records[1]["authority_id"] = records[0]["authority_id"]
        self.assertFalse(evidence_contract.assess(records)["accepted"])

    def test_duplicate_claim_is_rejected(self):
        records = [record(1), record(2)]
        records[1]["claim_hash"] = records[0]["claim_hash"]
        self.assertTrue(any("duplicate claim_hash" == reason for reason in evidence_contract.assess(records)["reasons"]))

    def test_assertion_key_set_extracts_keys_without_implying_fill(self):
        records = [record(1), record(2)]
        records[0]["assertion_key"] = "continuity"
        records[1]["assertion_key"] = "other"
        keys = evidence_contract.assertion_key_set(records)
        self.assertEqual(keys, {"continuity", "other"})
        # Helper documents keys for contradiction only; does not resolve slots.
        self.assertNotIn("filled", evidence_contract.assess(records))

