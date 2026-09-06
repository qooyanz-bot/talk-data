import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import protocol_claim_gate  # noqa: E402


R6G_FROZEN = {
    "protocol_id": "R6-G", "evidence_state": "SPEC_ONLY", "implementation_state": "NOT_IMPLEMENTED",
    "experiment_state": "NOT_RUN", "independent_replay_state": "NOT_RUN",
    "auditor_handoff": {"decision": "PENDING", "primary_run_authorized": False},
}


class ProtocolClaimGateTests(unittest.TestCase):
    def test_frozen_not_run_protocol_allows_description_only(self):
        self.assertEqual(protocol_claim_gate.assess_claim(R6G_FROZEN, "DESIGN_DESCRIPTION")["status"], "ALLOWED_AS_DESIGN")
        result = protocol_claim_gate.assess_claim(R6G_FROZEN, "EXPERIMENT_RESULT")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("experiment_state!=COMPLETED", result["unmet"])

    def test_capability_claim_requires_stronger_result_evidence(self):
        manifest = {
            "protocol_id": "synthetic", "evidence_state": "DIAGNOSTIC_ONLY", "implementation_state": "IMPLEMENTED",
            "experiment_state": "COMPLETED", "independent_replay_state": "REPLICATED",
            "auditor_handoff": {"decision": "PASS", "primary_run_authorized": True},
        }
        self.assertEqual(protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")["status"], "ALLOWED_AS_RESULT")
        self.assertEqual(protocol_claim_gate.assess_claim(manifest, "CAPABILITY_CLAIM")["reason"], "CAPABILITY_EVIDENCE_NOT_RESULT_BACKED")

    def test_result_backed_capability_claim_passes_gate(self):
        manifest = {
            "protocol_id": "synthetic", "evidence_state": "RESULT_BACKED", "implementation_state": "IMPLEMENTED",
            "experiment_state": "COMPLETED", "independent_replay_state": "REPLICATED",
            "auditor_handoff": {"decision": "PASS", "primary_run_authorized": True},
        }
        self.assertEqual(protocol_claim_gate.assess_claim(manifest, "CAPABILITY_CLAIM")["status"], "ALLOWED_AS_RESULT")
