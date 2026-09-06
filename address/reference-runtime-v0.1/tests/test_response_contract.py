import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import replay_verifier  # noqa: E402
import resolution_gate  # noqa: E402
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

    def test_ready_response_exposes_unfilled_residual(self):
        self.assertEqual(self.response["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(self.response["resolution"]["value"])
        self.assertIn("continuity", self.response["resolution"]["residual"])

    def test_filled_value_with_residual_is_rejected(self):
        self.response["resolution"]["value"] = "invented"
        # value non-null alone fails; residual present also forbids fill
        errors = response_contract.validate(self.response)
        self.assertTrue(any("null" in error or "residual" in error for error in errors))

    def test_nested_lineage_result_sha_is_rejected(self):
        # Public response must never stamp a non-null lineage.result_sha.
        self.response["lineage"] = {"result_sha": "sha256:" + "c" * 64}
        errors = response_contract.validate(self.response)
        self.assertTrue(any("result_sha" in error for error in errors))

    def test_nested_lineage_result_sha_under_audit_is_rejected(self):
        self.response["generated_audit"]["lineage"] = {"result_sha": "sha256:" + "d" * 64}
        errors = response_contract.validate(self.response)
        self.assertTrue(any("result_sha" in error for error in errors))

    def test_null_lineage_result_sha_is_allowed_when_present(self):
        self.response["lineage"] = {"result_sha": None, "input_hashes": []}
        self.assertEqual(response_contract.validate(self.response), [])

    def test_cli_evaluate_never_returns_result_sha(self):
        # Audit/CLI paths must not attach a stamped result_sha.
        dumped = str(self.response)
        self.assertNotIn("result_sha", dumped)
        self.assertIsNone(self.response["resolution"]["value"])

    def test_ready_with_null_target_residual_still_lists_unknown(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = None
        address["address_id"] = address_runtime.canonical_id(address)
        response = address_cli.evaluate(address, [evidence(1), evidence(2)], "2026-09-06T00:00:00Z")
        self.assertEqual(response["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIn("continuity", response["resolution"]["residual"])
        self.assertIsNone(response["resolution"]["value"])
        self.assertEqual(response_contract.validate(response), [])

    def test_residual_empty_string_item_is_rejected(self):
        self.response["resolution"]["residual"] = ["continuity", ""]
        errors = response_contract.validate(self.response)
        self.assertIn("resolution residual must be a list of non-empty strings", errors)

    def test_residual_non_string_item_is_rejected(self):
        self.response["resolution"]["residual"] = ["continuity", 1]
        errors = response_contract.validate(self.response)
        self.assertIn("resolution residual must be a list of non-empty strings", errors)

    def test_residual_none_item_is_rejected(self):
        self.response["resolution"]["residual"] = ["continuity", None]
        errors = response_contract.validate(self.response)
        self.assertIn("resolution residual must be a list of non-empty strings", errors)

    def test_abstain_response_with_valid_residual_passes_contract(self):
        # ABSTAIN happy path still requires residual to be list of non-empty strings.
        response = address_cli.evaluate(
            self.address,
            [
                {
                    "evidence_id": "e-1", "claim_hash": "claim-1", "path_id": "path-1",
                    "authority_id": "authority-1", "generator_id": "generator-1",
                    "semantic_law_id": "shared-law", "observed_at": "2026-09-05T00:00:00Z",
                    "assertion_key": "target", "assertion_value": "verified",
                },
                {
                    "evidence_id": "e-2", "claim_hash": "claim-2", "path_id": "path-2",
                    "authority_id": "authority-2", "generator_id": "generator-2",
                    "semantic_law_id": "shared-law", "observed_at": "2026-09-05T00:00:00Z",
                    "assertion_key": "target", "assertion_value": "verified",
                },
            ],
            "2026-09-06T00:00:00Z",
        )
        self.assertEqual(response["resolution"]["decision"], "ABSTAIN")
        self.assertIsNone(response["resolution"]["value"])
        residual = response["resolution"]["residual"]
        self.assertIsInstance(residual, list)
        self.assertTrue(all(isinstance(item, str) and item for item in residual))
        self.assertEqual(response_contract.validate(response), [])

    def test_unknown_resolution_decision_is_rejected(self):
        self.response["resolution"]["decision"] = "FAKE_DECISION"
        # Keep audit in sync so the failure is the unknown-decision rule, not audit mismatch.
        self.response["generated_audit"]["decision"] = "FAKE_DECISION"
        self.assertIn("resolution decision is unknown", response_contract.validate(self.response))

    def test_unknown_replay_status_is_rejected(self):
        self.response["replay"] = {"status": "FAKE_REPLAY", "errors": [], "value": None}
        self.assertIn("replay status is invalid", response_contract.validate(self.response))

    def test_decisions_and_replay_statuses_shared_from_emitters(self):
        self.assertEqual(
            resolution_gate.DECISION_ALLOWED,
            frozenset({"ABSTAIN", "READY_FOR_VERIFICATION"}),
        )
        self.assertIs(response_contract.DECISIONS, resolution_gate.DECISION_ALLOWED)
        self.assertEqual(
            replay_verifier.REPLAY_STATUS_ALLOWED,
            frozenset(
                {"REPLAY_VERIFIED", "REPLAY_MISMATCH", "LINEAGE_MISMATCH", "INVALID_AUDIT"}
            ),
        )
        self.assertIs(response_contract.REPLAY_STATUSES, replay_verifier.REPLAY_STATUS_ALLOWED)

    def test_ready_and_abstain_decisions_in_allowed(self):
        self.assertIn(self.response["resolution"]["decision"], resolution_gate.DECISION_ALLOWED)
        self.assertEqual(response_contract.validate(self.response), [])
