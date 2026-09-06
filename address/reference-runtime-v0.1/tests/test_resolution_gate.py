import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402
import audit_log  # noqa: E402
import evidence_contract  # noqa: E402
import resolution_gate  # noqa: E402


def evidence(index: int, observed_at: str = "2026-09-05T00:00:00Z") -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": observed_at,
        "assertion_key": "target:sample", "assertion_value": "verified",
    }


class ResolutionGateTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.bundle = [evidence(1), evidence(2)]

    def test_contracted_fresh_evidence_is_ready_but_value_is_null(self):
        # Fixture semantic_independence is UNVERIFIED; CONTRACTED evidence still READY.
        self.assertEqual(self.address["evidence_requirements"]["semantic_independence"], "UNVERIFIED")
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertEqual(result["reason"], "CONTRACTED_EVIDENCE")
        self.assertIsNone(result["value"])
        contract = evidence_contract.assess(self.bundle, self.address["evidence_requirements"]["minimum_sources"])
        self.assertEqual(contract["independence"], "CONTRACTED")

    def test_stale_evidence_abstains(self):
        result = resolution_gate.resolve(self.address, self.bundle, "2026-10-07T00:00:00Z")
        self.assertEqual(result["reason"], "EVIDENCE_STALE")

    def test_contradictory_assertion_abstains(self):
        self.bundle[1]["assertion_value"] = "rejected"
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["reason"], "CONTRADICTION")

    def test_shared_law_abstains_before_verification(self):
        self.bundle[1]["semantic_law_id"] = self.bundle[0]["semantic_law_id"]
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["reason"], "EVIDENCE_REJECTED")
        contract = evidence_contract.assess(self.bundle, self.address["evidence_requirements"]["minimum_sources"])
        self.assertEqual(contract["independence"], "COMMON_CAUSE_SUSPECT")

    def test_ready_requires_contracted_independence_not_common_cause(self):
        self.bundle[1]["generator_id"] = self.bundle[0]["generator_id"]
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "EVIDENCE_REJECTED")
        self.assertIsNone(result["value"])

    def test_audited_requirement_with_only_contracted_evidence_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])
        self.assertTrue(any("AUDITED" in str(item) for item in result["details"]))
        self.assertTrue(any("CONTRACTED" in str(item) for item in result["details"]))
        # Must not silently upgrade to READY or claim independence beyond CONTRACTED.
        self.assertNotEqual(result["decision"], "READY_FOR_VERIFICATION")

    def test_contracted_requirement_with_contracted_evidence_is_ready(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "CONTRACTED"
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertEqual(result["reason"], "CONTRACTED_EVIDENCE")
        self.assertIsNone(result["value"])

    def test_ready_keeps_unknown_slots_as_residual_and_value_null(self):
        result = resolution_gate.resolve(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])
        # Typed binding must not invent a filled slot payload.
        self.assertNotIn("filled", result)

    def test_ready_exposes_unknown_when_target_value_residual_is_null(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = None
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])

    def test_target_value_residual_labels_appear_in_resolution_residual(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["extra-slot", "continuity"]
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        # Union: unknown slots plus target_value.residual labels; never invent a filled value.
        self.assertIn("continuity", result["residual"])
        self.assertIn("extra-slot", result["residual"])
        for label in address["target_value"]["residual"]:
            self.assertIn(label, result["residual"])
        self.assertNotIn("filled", result)
        self.assertNotIn("value_filled", result)

    def test_target_value_residual_never_fills_value(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["open-slot"]
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertIsNone(result["value"])
        self.assertIn("open-slot", result["residual"])
        # Residual labels must not be treated as resolved payloads.
        self.assertNotEqual(result.get("value"), "open-slot")


    def test_target_value_residual_skips_invalid_labels(self):
        """Empty / non-string residual items are skipped; valid labels still appear."""
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["kept-slot", "", None, 3, "another-slot"]
        # Empty string / None / int must not raise and must not enter residual.
        address["address_id"] = address_runtime.canonical_id(address)
        # Invalid residual makes validate fail; resolve must still build residual safely.
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertIsNone(result["value"])
        self.assertIn("kept-slot", result["residual"])
        self.assertIn("another-slot", result["residual"])
        self.assertNotIn("", result["residual"])
        self.assertNotIn(None, result["residual"])
        self.assertNotIn(3, result["residual"])
        self.assertTrue(all(isinstance(item, str) and item for item in result["residual"]))

    def test_assertion_key_collision_with_unknown_slot_does_not_fill_residual(self):
        """assertion_key matching unknown.slot must not clear residual or bind value."""
        address = copy.deepcopy(self.address)
        # Fixture unknown.slot is "continuity"; collide assertion_key with that label.
        for item in self.bundle:
            item["assertion_key"] = "continuity"
            item["assertion_value"] = "supposedly-resolved"
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])
        self.assertNotEqual(result["value"], "supposedly-resolved")
        self.assertNotIn("filled", result)
        # Collision set is detectable but must not remove the residual label.
        colliding = evidence_contract.assertion_key_set(self.bundle) & set(result["residual"])
        self.assertIn("continuity", colliding)

    def test_audited_requirement_without_independence_audit_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        result = resolution_gate.resolve(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])
        self.assertTrue(any("independence_audit" in str(item) or "missing" in str(item) for item in result["details"]))

    def test_audited_requirement_with_incomplete_audit_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        incomplete = {"auditor_id": "auditor:x", "decision": "PASS"}
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=incomplete
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])

    def test_audited_requirement_with_forged_audit_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        forged = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "FAIL",
            "method": "synthetic-pairwise-review",
            "evidence_digests": [{"evidence_id": "e-1", "digest": "sha256:aaa"}],
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=forged
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])

    def test_audited_requirement_with_valid_audit_is_ready_value_null(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        audit = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "PASS",
            "method": "synthetic-pairwise-review",
            "evidence_digests": audit_log.evidence_digest_entries(self.bundle),
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["decision"], "READY_FOR_VERIFICATION")
        self.assertEqual(result["reason"], "AUDITED_INDEPENDENCE")
        self.assertIsNone(result["value"])
        self.assertIn("continuity", result["residual"])
        # assess() alone still CONTRACTED; READY here is verification gate only.
        contract = evidence_contract.assess(self.bundle, address["evidence_requirements"]["minimum_sources"])
        self.assertEqual(contract["independence"], "CONTRACTED")

    def test_audited_requirement_with_mismatched_digests_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        # Checklist-valid PASS whose digests do not match the supplied bundle.
        audit = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "PASS",
            "method": "synthetic-pairwise-review",
            "evidence_digests": [
                {"evidence_id": "e-1", "digest": "sha256:aaa"},
                {"evidence_id": "e-2", "digest": "sha256:bbb"},
            ],
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])
        self.assertTrue(
            any("do not match" in str(item) or "different set" in str(item) for item in result["details"])
        )

    def test_audited_requirement_with_bare_string_digests_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        expected = audit_log.evidence_digest_entries(self.bundle)
        audit = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "PASS",
            "method": "synthetic-pairwise-review",
            # Shape-invalid: bare strings even if digest values match content.
            "evidence_digests": [entry["digest"] for entry in expected],
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])
        self.assertTrue(
            any(
                "bare digest strings" in str(item) or "{evidence_id, digest}" in str(item)
                for item in result["details"]
            )
        )

    def test_audited_requirement_with_wrong_evidence_id_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        expected = audit_log.evidence_digest_entries(self.bundle)
        audit = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "PASS",
            "method": "synthetic-pairwise-review",
            "evidence_digests": [
                {"evidence_id": "e-wrong", "digest": expected[0]["digest"]},
                dict(expected[1]),
            ],
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])

    def test_audited_requirement_with_wrong_digest_value_abstains(self):
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        expected = audit_log.evidence_digest_entries(self.bundle)
        audit = {
            "auditor_id": "auditor:synthetic-1",
            "decision": "PASS",
            "method": "synthetic-pairwise-review",
            "evidence_digests": [
                {"evidence_id": expected[0]["evidence_id"], "digest": "sha256:deadbeef"},
                dict(expected[1]),
            ],
            "audited_at": "2026-09-06T00:00:00Z",
        }
        result = resolution_gate.resolve(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["decision"], "ABSTAIN")
        self.assertEqual(result["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["value"])


if __name__ == "__main__":
    unittest.main()
