import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402
import audit_log  # noqa: E402
import replay_verifier  # noqa: E402
import resolution_gate  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": "2026-09-05T00:00:00Z",
        "assertion_key": "target", "assertion_value": "verified",
    }


class ReplayVerifierTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.evidence = [evidence(1), evidence(2)]
        self.at = "2026-09-06T00:00:00Z"
        outcome = resolution_gate.resolve(self.address, self.evidence, self.at)
        self.record = audit_log.create(self.address, self.evidence, outcome, self.at)

    def test_exact_replay_verifies(self):
        result = replay_verifier.verify_replay(self.address, self.evidence, self.record)
        self.assertEqual(result["status"], "REPLAY_VERIFIED")
        self.assertIsNone(result["value"])

    def test_changed_evidence_is_a_replay_mismatch(self):
        self.evidence[1]["assertion_value"] = "contradicted"
        result = replay_verifier.verify_replay(self.address, self.evidence, self.record)
        self.assertEqual(result["status"], "REPLAY_MISMATCH")

    def test_other_address_is_a_lineage_mismatch(self):
        other = dict(self.address)
        other["goal"] = {"id": "goal:other", "success_criteria": []}
        other["address_id"] = address_runtime.canonical_id(other)
        result = replay_verifier.verify_replay(other, self.evidence, self.record)
        self.assertEqual(result["status"], "LINEAGE_MISMATCH")


    def test_invalid_audit_status(self):
        broken = dict(self.record)
        broken["audit_id"] = "tampered"
        result = replay_verifier.verify_replay(self.address, self.evidence, broken)
        self.assertEqual(result["status"], "INVALID_AUDIT")
        self.assertIn(result["status"], replay_verifier.REPLAY_STATUS_ALLOWED)

    def test_replay_status_allowed_covers_emitters(self):
        self.assertEqual(
            replay_verifier.REPLAY_STATUS_ALLOWED,
            frozenset(
                {"REPLAY_VERIFIED", "REPLAY_MISMATCH", "LINEAGE_MISMATCH", "INVALID_AUDIT"}
            ),
        )
        verified = replay_verifier.verify_replay(self.address, self.evidence, self.record)
        self.assertIn(verified["status"], replay_verifier.REPLAY_STATUS_ALLOWED)


if __name__ == "__main__":
    unittest.main()
