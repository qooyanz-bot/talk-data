import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import decision_log  # noqa: E402
import protocol_claim_gate  # noqa: E402
import response_contract  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}", "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z", "assertion_key": "target", "assertion_value": "verified",
    }


class DecisionLogTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json").read_text(encoding="utf-8")
        )
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.bundle = [evidence(1), evidence(2)]

    def test_r6g_frozen_experiment_result_blocked_log_matches_fixture(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        fixture = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        self.assertEqual(log, fixture)
        self.assertEqual(log["claim_status"], "BLOCKED")
        self.assertEqual(log["claim_reason"], "EVIDENCE_GATES_UNMET")
        self.assertEqual(log["evidence_state"], "SPEC_ONLY")
        self.assertEqual(log["experiment_state"], "NOT_RUN")
        self.assertIsNone(log["value"])
        self.assertEqual(
            set(log["auditor_handoff"]),
            {"decision", "primary_run_authorized"},
        )

    def test_design_description_allowed_as_design_log(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "DESIGN_DESCRIPTION")
        log = decision_log.build_decision_log(self.manifest, "DESIGN_DESCRIPTION", assessment)
        self.assertEqual(log["claim_status"], "ALLOWED_AS_DESIGN")
        self.assertEqual(log["claim_reason"], "NO_RESULT_CLAIM")
        self.assertEqual(log["unmet"], [])
        self.assertIsNone(log["value"])
        self.assertEqual(log["protocol_id"], "R6-G")
        self.assertEqual(log["schema_version"], decision_log.SCHEMA_VERSION)

    def test_incomplete_handoff_still_blocked(self):
        manifest = copy.deepcopy(self.manifest)
        # Near-complete gates but incomplete handoff must remain BLOCKED.
        manifest["implementation_state"] = "IMPLEMENTED"
        manifest["experiment_state"] = "COMPLETED"
        manifest["independent_replay_state"] = "REPLICATED"
        manifest["auditor_handoff"] = {"decision": "PENDING", "primary_run_authorized": False}
        assessment = protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")
        self.assertEqual(assessment["status"], "BLOCKED")
        log = decision_log.build_decision_log(manifest, "EXPERIMENT_RESULT", assessment)
        self.assertEqual(log["claim_status"], "BLOCKED")
        self.assertIn("auditor_handoff.decision!=PASS", log["unmet"])
        self.assertIn("primary_run_authorized!=true", log["unmet"])
        self.assertIsNone(log["value"])
        self.assertEqual(log["auditor_handoff"]["decision"], "PENDING")
        self.assertIs(log["auditor_handoff"]["primary_run_authorized"], False)

    def test_handoff_snapshot_strips_extra_keys(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["auditor_handoff"] = {
            "decision": "PENDING",
            "primary_run_authorized": False,
            "secret_token": "must-not-leak",
            "notes": "extra",
        }
        assessment = protocol_claim_gate.assess_claim(manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(manifest, "EXPERIMENT_RESULT", assessment)
        self.assertEqual(set(log["auditor_handoff"]), {"decision", "primary_run_authorized"})
        dumped = json.dumps(log)
        self.assertNotIn("secret_token", dumped)
        self.assertNotIn("must-not-leak", dumped)

    def test_never_fills_value(self):
        for claim_type in ("DESIGN_DESCRIPTION", "EXPERIMENT_RESULT", "CAPABILITY_CLAIM", "UNKNOWN"):
            with self.subTest(claim_type=claim_type):
                assessment = protocol_claim_gate.assess_claim(self.manifest, claim_type)
                log = decision_log.build_decision_log(self.manifest, claim_type, assessment)
                self.assertIsNone(log["value"])
                self.assertIn("value", log)

    def test_cli_evaluate_attaches_decision_log_with_protocol_claim(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        self.assertIn("decision_log", result)
        self.assertIn("protocol_claim", result)
        self.assertEqual(result["decision_log"]["claim_status"], result["protocol_claim"]["status"])
        self.assertEqual(result["decision_log"]["claim_status"], "BLOCKED")
        self.assertIsNone(result["decision_log"]["value"])
        self.assertIsNone(result["protocol_claim"]["value"])
        self.assertIsNone(result["resolution"]["value"])
        self.assertEqual(response_contract.validate(result), [])
        fixture = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        self.assertEqual(result["decision_log"], fixture)

    def test_cli_design_description_decision_log_allowed(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="DESIGN_DESCRIPTION",
        )
        self.assertEqual(result["decision_log"]["claim_status"], "ALLOWED_AS_DESIGN")
        self.assertEqual(result["protocol_claim"]["status"], "ALLOWED_AS_DESIGN")
        self.assertIsNone(result["decision_log"]["value"])
        self.assertEqual(response_contract.validate(result), [])

    def test_response_contract_rejects_filled_decision_log_value(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["value"] = "invented"
        self.assertIn("public decision_log value must be null", response_contract.validate(result))

    def test_response_contract_rejects_claim_status_contradiction(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["claim_status"] = "ALLOWED_AS_RESULT"
        errors = response_contract.validate(result)
        self.assertTrue(any("contradict" in error for error in errors))

    def test_response_contract_rejects_unknown_decision_log_claim_status(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["claim_status"] = "FAKE_STATUS"
        self.assertIn("decision_log claim_status is invalid", response_contract.validate(result))


    def test_response_contract_rejects_missing_decision_log_schema_version(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        del result["decision_log"]["schema_version"]
        errors = response_contract.validate(result)
        self.assertTrue(
            any("missing required fields" in error or "schema_version" in error for error in errors)
        )

    def test_response_contract_rejects_wrong_decision_log_handoff_keys(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["auditor_handoff"] = {
            "decision": "PENDING",
            "primary_run_authorized": False,
            "secret_token": "must-not-pass-contract",
        }
        errors = response_contract.validate(result)
        self.assertIn("decision_log auditor_handoff keys are invalid", errors)

    def test_response_contract_rejects_wrong_decision_log_schema_version(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["schema_version"] = "address-decision-log-v0-fake"
        self.assertIn("decision_log schema_version is invalid", response_contract.validate(result))


    def test_response_contract_rejects_claim_reason_mismatch(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["claim_reason"] = "OTHER_REASON"
        errors = response_contract.validate(result)
        self.assertIn("decision_log claim_reason contradicts protocol_claim.reason", errors)

    def test_response_contract_rejects_unmet_non_list(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["unmet"] = "not-a-list"
        errors = response_contract.validate(result)
        self.assertIn("decision_log unmet must be null or a list of strings", errors)

    def test_response_contract_rejects_unmet_mismatch(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["unmet"] = list(result["decision_log"]["unmet"]) + ["extra_gate!=true"]
        errors = response_contract.validate(result)
        self.assertIn("decision_log unmet contradicts protocol_claim.unmet", errors)

    def test_decision_log_always_emits_unmet_list(self):
        for claim_type in ("DESIGN_DESCRIPTION", "EXPERIMENT_RESULT", "CAPABILITY_CLAIM", "UNKNOWN"):
            with self.subTest(claim_type=claim_type):
                assessment = protocol_claim_gate.assess_claim(self.manifest, claim_type)
                log = decision_log.build_decision_log(self.manifest, claim_type, assessment)
                self.assertIsInstance(log["unmet"], list)
                self.assertTrue(all(isinstance(item, str) for item in log["unmet"]))


if __name__ == "__main__":
    unittest.main()
