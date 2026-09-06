import copy
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
        self.assertEqual(result["reason"], "EVIDENCE_GATES_UNMET")
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

    def test_validate_manifest_accepts_frozen_r6g(self):
        self.assertEqual(protocol_claim_gate.validate_manifest(R6G_FROZEN), [])

    def test_unknown_evidence_state_manifest_invalid(self):
        manifest = copy.deepcopy(R6G_FROZEN)
        manifest["evidence_state"] = "UNKNOWN_EVIDENCE"
        errors = protocol_claim_gate.validate_manifest(manifest)
        self.assertTrue(any("evidence_state must be one of" in e for e in errors))
        result = protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason"], "MANIFEST_INVALID")
        self.assertEqual(result["unmet"], errors)

    def test_typo_experiment_state_manifest_invalid(self):
        manifest = copy.deepcopy(R6G_FROZEN)
        manifest["experiment_state"] = "COMPLETTED"  # typo
        errors = protocol_claim_gate.validate_manifest(manifest)
        self.assertTrue(any("experiment_state must be one of" in e for e in errors))
        result = protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")
        self.assertEqual(result["reason"], "MANIFEST_INVALID")
        self.assertIn(errors[0], result["unmet"])

    def test_extra_handoff_secret_key_rejected(self):
        manifest = copy.deepcopy(R6G_FROZEN)
        manifest["auditor_handoff"] = {
            "decision": "PENDING",
            "primary_run_authorized": False,
            "api_token": "secret",
        }
        errors = protocol_claim_gate.validate_manifest(manifest)
        self.assertTrue(any("auditor_handoff keys must be only" in e for e in errors))
        result = protocol_claim_gate.assess_claim(manifest, "DESIGN_DESCRIPTION")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason"], "MANIFEST_INVALID")

    def test_empty_protocol_id_rejected(self):
        manifest = copy.deepcopy(R6G_FROZEN)
        manifest["protocol_id"] = ""
        errors = protocol_claim_gate.validate_manifest(manifest)
        self.assertIn("protocol_id must be a non-empty string", errors)
        result = protocol_claim_gate.assess_claim(manifest, "DESIGN_DESCRIPTION")
        self.assertEqual(result["reason"], "MANIFEST_INVALID")
        self.assertEqual(result["unmet"], errors)

    def test_design_description_blocked_on_invalid_enum(self):
        manifest = copy.deepcopy(R6G_FROZEN)
        manifest["implementation_state"] = "HALF_DONE"
        result = protocol_claim_gate.assess_claim(manifest, "DESIGN_DESCRIPTION")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["reason"], "MANIFEST_INVALID")
        self.assertTrue(any("implementation_state must be one of" in e for e in result["unmet"]))
