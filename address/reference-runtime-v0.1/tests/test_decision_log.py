import copy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import audit_log  # noqa: E402
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

    def test_decision_log_id_stable_for_same_inputs(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        first = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        second = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        self.assertEqual(first["decision_log_id"], second["decision_log_id"])
        self.assertTrue(first["decision_log_id"].startswith("decision_log:"))
        self.assertEqual(decision_log.verify(first), [])
        self.assertEqual(first, decision_log.create(self.manifest, "EXPERIMENT_RESULT", assessment))

    def test_decision_log_tampering_is_detected(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["unmet"] = list(log["unmet"]) + ["tampered_gate!=true"]
        errors = decision_log.verify(log)
        self.assertTrue(errors)
        self.assertTrue(any("decision_log_id does not match" in e for e in errors))

    def test_response_contract_requires_valid_decision_log_id(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        self.assertEqual(response_contract.validate(result), [])
        del result["decision_log"]["decision_log_id"]
        errors = response_contract.validate(result)
        self.assertTrue(
            any("missing required fields" in error or "decision_log_id" in error for error in errors)
        )

    def test_response_contract_rejects_tampered_decision_log_id(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["decision_log_id"] = "decision_log:" + ("0" * 64)
        errors = response_contract.validate(result)
        self.assertTrue(any("decision_log_id does not match" in error for error in errors))


    def test_verify_rejects_unknown_evidence_state_executed(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["evidence_state"] = "EXECUTED"
        payload = {key: value for key, value in log.items() if key != "decision_log_id"}
        log["decision_log_id"] = "decision_log:" + audit_log.content_digest(payload).removeprefix("sha256:")
        errors = decision_log.verify(log)
        self.assertTrue(any("evidence_state must be one of" in error for error in errors))
        self.assertFalse(any("decision_log_id" in error for error in errors))

    def test_response_contract_rejects_unknown_decision_log_evidence_state(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["evidence_state"] = "EXECUTED"
        errors = response_contract.validate(result)
        self.assertTrue(any("evidence_state must be one of" in error for error in errors))

    def test_verify_rejects_unknown_auditor_handoff_decision(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["auditor_handoff"] = {"decision": "FAIL", "primary_run_authorized": False}
        payload = {key: value for key, value in log.items() if key != "decision_log_id"}
        log["decision_log_id"] = "decision_log:" + audit_log.content_digest(payload).removeprefix("sha256:")
        errors = decision_log.verify(log)
        self.assertTrue(any("auditor_handoff.decision must be one of" in error for error in errors))

    def test_verify_allows_none_state_fields(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "DESIGN_DESCRIPTION")
        log = decision_log.build_decision_log({}, "DESIGN_DESCRIPTION", assessment)
        for field in (
            "evidence_state",
            "experiment_state",
            "implementation_state",
            "independent_replay_state",
        ):
            self.assertIsNone(log[field])
        self.assertEqual(decision_log.verify(log), [])

    def test_build_decision_log_from_valid_manifest_passes_verify(self):
        for claim_type in ("DESIGN_DESCRIPTION", "EXPERIMENT_RESULT", "CAPABILITY_CLAIM"):
            with self.subTest(claim_type=claim_type):
                assessment = protocol_claim_gate.assess_claim(self.manifest, claim_type)
                log = decision_log.build_decision_log(self.manifest, claim_type, assessment)
                self.assertEqual(decision_log.verify(log), [])

    def test_closed_enums_shared_from_protocol_claim_gate(self):
        self.assertIs(
            decision_log.protocol_claim_gate.EVIDENCE_STATE_ALLOWED,
            protocol_claim_gate.EVIDENCE_STATE_ALLOWED,
        )
        self.assertEqual(
            set(decision_log._HANDOFF_KEYS),
            protocol_claim_gate.AUDITOR_HANDOFF_KEYS,
        )
        self.assertEqual(
            response_contract.DECISION_LOG_HANDOFF_KEYS,
            protocol_claim_gate.AUDITOR_HANDOFF_KEYS,
        )


    def test_r6g_frozen_decision_log_verifies(self):
        fixture = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        self.assertEqual(decision_log.verify(fixture), [])
        self.assertTrue(fixture["decision_log_id"].startswith("decision_log:"))




    def test_verify_decision_log_cli_accepts_frozen_fixture(self):
        fixture = ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json"
        buf = StringIO()
        with redirect_stdout(buf):
            code = address_cli.main(["--verify-decision-log", str(fixture)])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "DECISION_LOG_OK")
        self.assertEqual(payload["errors"], [])

    def test_verify_decision_log_cli_rejects_tampered_id(self):
        fixture = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        fixture["decision_log_id"] = "decision_log:" + ("0" * 64)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tampered.json"
            path.write_text(json.dumps(fixture), encoding="utf-8")
            buf = StringIO()
            with redirect_stdout(buf):
                code = address_cli.main(["--verify-decision-log", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "DECISION_LOG_INVALID")
            self.assertTrue(any("decision_log_id" in err for err in payload["errors"]))

    def test_verify_decision_log_rejects_resolve_and_other_standalone_flags(self):
        fixture = str(ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json")
        cases = [
            ["address.json", "evidence.json"],
            ["--now", "2026-09-06T00:00:00Z"],
            ["--limitations"],
            ["--check-contract-only", str(ROOT / "fixtures" / "golden_contract_ok_response.json")],
            ["--validate-protocol-manifest", str(ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json")],
            ["--conformance"],
            ["--independence-audit", "audit.json"],
        ]
        for extra in cases:
            with self.subTest(extra=extra):
                buf = StringIO()
                with redirect_stdout(buf):
                    code = address_cli.main(["--verify-decision-log", fixture, *extra])
                self.assertEqual(code, 2)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload["status"], "INVALID_INPUT")
                self.assertTrue(payload["errors"])


    def test_verify_rejects_unknown_claim_type(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["claim_type"] = "UNKNOWN"
        # id no longer matches after mutation; either error is sufficient
        errors = decision_log.verify(log)
        self.assertTrue(any("claim_type must be one of" in e for e in errors))

    def test_verify_rejects_empty_claim_type(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["claim_type"] = ""
        errors = decision_log.verify(log)
        self.assertTrue(any("claim_type must be one of" in e for e in errors))

    def test_claim_type_allowed_shared_from_protocol_claim_gate(self):
        self.assertEqual(
            protocol_claim_gate.CLAIM_TYPE_ALLOWED,
            frozenset({"DESIGN_DESCRIPTION", "EXPERIMENT_RESULT", "CAPABILITY_CLAIM"}),
        )

    def test_verify_rejects_unknown_claim_reason(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["claim_reason"] = "OTHER_REASON"
        errors = decision_log.verify(log)
        self.assertTrue(any("claim_reason must be one of" in e for e in errors))

    def test_response_contract_rejects_unknown_claim_reason(self):
        result = address_cli.evaluate(
            self.address,
            self.bundle,
            "2026-09-06T00:00:00Z",
            protocol_manifest=self.manifest,
            claim_type="EXPERIMENT_RESULT",
        )
        result["decision_log"]["claim_reason"] = "OTHER_REASON"
        # Keep protocol_claim.reason in sync so contradiction is not the only failure.
        result["protocol_claim"]["reason"] = "OTHER_REASON"
        errors = response_contract.validate(result)
        self.assertTrue(
            any("claim_reason must be one of" in e for e in errors),
            errors,
        )

    def test_claim_reason_allowed_shared_from_protocol_claim_gate(self):
        self.assertEqual(
            protocol_claim_gate.CLAIM_REASON_ALLOWED,
            frozenset(
                {
                    "NO_RESULT_CLAIM",
                    "EVIDENCE_GATES_UNMET",
                    "MANIFEST_INVALID",
                    "CLAIM_TYPE_UNKNOWN",
                    "CAPABILITY_EVIDENCE_NOT_RESULT_BACKED",
                    "RECORDED_EVIDENCE_GATES_PASS",
                }
            ),
        )

    def test_happy_path_claim_reasons_verify(self):
        # DESIGN -> NO_RESULT_CLAIM; EXPERIMENT on R6-G -> EVIDENCE_GATES_UNMET
        for claim_type, expected_reason in (
            ("DESIGN_DESCRIPTION", "NO_RESULT_CLAIM"),
            ("EXPERIMENT_RESULT", "EVIDENCE_GATES_UNMET"),
            ("CAPABILITY_CLAIM", "EVIDENCE_GATES_UNMET"),
            ("UNKNOWN", "CLAIM_TYPE_UNKNOWN"),
        ):
            with self.subTest(claim_type=claim_type):
                assessment = protocol_claim_gate.assess_claim(self.manifest, claim_type)
                self.assertEqual(assessment.get("reason"), expected_reason)
                # UNKNOWN claim_type fails claim_type verify; use a valid type with same reason
                log_type = claim_type if claim_type in protocol_claim_gate.CLAIM_TYPE_ALLOWED else "EXPERIMENT_RESULT"
                if claim_type == "UNKNOWN":
                    log = decision_log.build_decision_log(self.manifest, log_type, assessment)
                    # assessment reason is CLAIM_TYPE_UNKNOWN which is allowed
                    self.assertEqual(log["claim_reason"], "CLAIM_TYPE_UNKNOWN")
                    self.assertEqual(decision_log.verify(log), [])
                else:
                    log = decision_log.build_decision_log(self.manifest, claim_type, assessment)
                    self.assertEqual(log["claim_reason"], expected_reason)
                    self.assertEqual(decision_log.verify(log), [])

    def test_r6g_frozen_fixture_claim_reason_still_valid(self):
        frozen = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        self.assertEqual(frozen["claim_reason"], "EVIDENCE_GATES_UNMET")
        self.assertIn(frozen["claim_reason"], protocol_claim_gate.CLAIM_REASON_ALLOWED)
        self.assertEqual(decision_log.verify(frozen), [])

    def test_verify_rejects_unknown_claim_status(self):
        assessment = protocol_claim_gate.assess_claim(self.manifest, "EXPERIMENT_RESULT")
        log = decision_log.build_decision_log(self.manifest, "EXPERIMENT_RESULT", assessment)
        log["claim_status"] = "FAKE_STATUS"
        errors = decision_log.verify(log)
        self.assertTrue(any("claim_status must be one of" in e for e in errors))

    def test_claim_status_allowed_shared_from_protocol_claim_gate(self):
        self.assertEqual(
            protocol_claim_gate.CLAIM_STATUS_ALLOWED,
            frozenset({"ALLOWED_AS_DESIGN", "ALLOWED_AS_RESULT", "BLOCKED"}),
        )
        self.assertEqual(
            response_contract.PROTOCOL_CLAIM_STATUSES,
            protocol_claim_gate.CLAIM_STATUS_ALLOWED,
        )

    def test_happy_path_claim_statuses_verify(self):
        for claim_type, expected_status in (
            ("DESIGN_DESCRIPTION", "ALLOWED_AS_DESIGN"),
            ("EXPERIMENT_RESULT", "BLOCKED"),
        ):
            with self.subTest(claim_type=claim_type):
                assessment = protocol_claim_gate.assess_claim(self.manifest, claim_type)
                self.assertEqual(assessment.get("status"), expected_status)
                log = decision_log.build_decision_log(self.manifest, claim_type, assessment)
                self.assertEqual(log["claim_status"], expected_status)
                self.assertEqual(decision_log.verify(log), [])

    def test_r6g_frozen_fixture_claim_status_still_valid(self):
        frozen = json.loads(
            (ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json").read_text(encoding="utf-8")
        )
        self.assertEqual(frozen["claim_status"], "BLOCKED")
        self.assertIn(frozen["claim_status"], protocol_claim_gate.CLAIM_STATUS_ALLOWED)
        self.assertEqual(decision_log.verify(frozen), [])



    def test_required_keys_single_source_frozenset(self):
        import response_contract
        self.assertIsInstance(decision_log.REQUIRED_KEYS, frozenset)
        self.assertIn("decision_log_id", decision_log.REQUIRED_KEYS)
        self.assertIn("schema_version", decision_log.REQUIRED_KEYS)
        self.assertIs(response_contract.DECISION_LOG_REQUIRED_KEYS, decision_log.REQUIRED_KEYS)
        self.assertEqual(response_contract.DECISION_LOG_REQUIRED_KEYS, decision_log.REQUIRED_KEYS)


if __name__ == "__main__":
    unittest.main()
