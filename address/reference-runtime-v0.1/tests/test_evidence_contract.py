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
        self.assertEqual(result["independence"], "CONTRACTED")
        self.assertTrue(result["accepted"])
        self.assertIn("unaudited", result["reasons"][0])
        self.assertNotIn(result["independence"], ("INDEPENDENT", "AUDITED"))

    def test_distinct_paths_with_shared_law_are_common_cause_suspect(self):
        records = [record(1), record(2)]
        records[1]["semantic_law_id"] = records[0]["semantic_law_id"]
        result = evidence_contract.assess(records)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["independence"], "COMMON_CAUSE_SUSPECT")
        self.assertFalse(result["accepted"])
        self.assertTrue(any("semantic_law_id" in reason for reason in result["reasons"]))

    def test_shared_authority_is_rejected(self):
        records = [record(1), record(2)]
        records[1]["authority_id"] = records[0]["authority_id"]
        result = evidence_contract.assess(records)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "COMMON_CAUSE_SUSPECT")

    def test_shared_generator_is_common_cause_suspect(self):
        records = [record(1), record(2)]
        records[1]["generator_id"] = records[0]["generator_id"]
        result = evidence_contract.assess(records)
        self.assertEqual(result["status"], "CONFLICT")
        self.assertEqual(result["independence"], "COMMON_CAUSE_SUSPECT")
        self.assertFalse(result["accepted"])

    def test_duplicate_claim_is_rejected(self):
        records = [record(1), record(2)]
        records[1]["claim_hash"] = records[0]["claim_hash"]
        result = evidence_contract.assess(records)
        self.assertTrue(any("duplicate claim_hash" == reason for reason in result["reasons"]))
        self.assertEqual(result["independence"], "COMMON_CAUSE_SUSPECT")
        self.assertFalse(result["accepted"])

    def test_insufficient_evidence_is_unverified(self):
        result = evidence_contract.assess([record(1)], minimum_sources=2)
        self.assertEqual(result["status"], "INSUFFICIENT")
        self.assertEqual(result["independence"], "UNVERIFIED")
        self.assertFalse(result["accepted"])

    def test_invalid_evidence_is_unverified(self):
        result = evidence_contract.assess(["not-an-object", "also-bad"])
        self.assertEqual(result["status"], "INVALID")
        self.assertEqual(result["independence"], "UNVERIFIED")
        self.assertFalse(result["accepted"])

    def test_assess_never_emits_independent_or_audited(self):
        samples = [
            evidence_contract.assess([record(1), record(2)]),
            evidence_contract.assess([record(1)]),
            evidence_contract.assess("bad"),
        ]
        shared = [record(1), record(2)]
        shared[1]["authority_id"] = shared[0]["authority_id"]
        samples.append(evidence_contract.assess(shared))
        for result in samples:
            self.assertNotIn(result["independence"], ("INDEPENDENT", "AUDITED"))
            self.assertIn(
                result["independence"],
                ("COMMON_CAUSE_SUSPECT", "CONTRACTED", "UNVERIFIED"),
            )

    def test_assertion_key_set_extracts_keys_without_implying_fill(self):
        records = [record(1), record(2)]
        records[0]["assertion_key"] = "continuity"
        records[1]["assertion_key"] = "other"
        keys = evidence_contract.assertion_key_set(records)
        self.assertEqual(keys, {"continuity", "other"})
        # Helper documents keys for contradiction only; does not resolve slots.
        self.assertNotIn("filled", evidence_contract.assess(records))
