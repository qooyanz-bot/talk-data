import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import audit_log  # noqa: E402
import evidence_contract  # noqa: E402


def record(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}",
        "semantic_law_id": f"law-{index}", "observed_at": "2026-09-06T00:00:00Z",
    }


def valid_independence_audit(evidence=None) -> dict:
    """Build a checklist-valid audit; digests match evidence when provided."""
    if evidence is None:
        digests = [
            {"evidence_id": "e-1", "digest": "sha256:aaa"},
            {"evidence_id": "e-2", "digest": "sha256:bbb"},
        ]
    else:
        digests = audit_log.evidence_digest_entries(evidence)
    return {
        "auditor_id": "auditor:synthetic-1",
        "decision": "PASS",
        "method": "synthetic-pairwise-review",
        "evidence_digests": digests,
        "audited_at": "2026-09-06T00:00:00Z",
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

    def test_path_diversity_alone_never_audited(self):
        # Distinct path_ids with full metadata separation still stop at CONTRACTED.
        result = evidence_contract.assess([record(1), record(2)])
        self.assertEqual(result["independence"], "CONTRACTED")
        self.assertNotEqual(result["independence"], "AUDITED")

    def test_assertion_key_set_extracts_keys_without_implying_fill(self):
        records = [record(1), record(2)]
        records[0]["assertion_key"] = "continuity"
        records[1]["assertion_key"] = "other"
        keys = evidence_contract.assertion_key_set(records)
        self.assertEqual(keys, {"continuity", "other"})
        # Helper documents keys for contradiction only; does not resolve slots.
        self.assertNotIn("filled", evidence_contract.assess(records))

    def test_audited_checklist_documents_required_fields(self):
        checklist = evidence_contract.audited_independence_checklist()
        self.assertEqual(
            set(checklist["required_fields"]),
            evidence_contract.AUDITED_INDEPENDENCE_REQUIRED_FIELDS,
        )
        self.assertEqual(checklist["decision_must_be"], "PASS")
        self.assertTrue(checklist["notes"])
        notes = " ".join(checklist["notes"])
        self.assertIn("{evidence_id, digest}", notes)
        self.assertIn("bare strings rejected", notes)
        self.assertNotIn("nonempty digest strings or", notes)

    def test_assess_audited_independence_valid_shape_is_audited(self):
        result = evidence_contract.assess_audited_independence(valid_independence_audit())
        self.assertTrue(result["accepted"])
        self.assertEqual(result["independence"], "AUDITED")
        self.assertEqual(result["status"], "AUDITED")

    def test_assess_audited_independence_missing_record_is_unmet(self):
        result = evidence_contract.assess_audited_independence(None)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("missing" in reason for reason in result["reasons"]))

    def test_assess_audited_independence_incomplete_is_unmet(self):
        incomplete = {"auditor_id": "auditor:x", "decision": "PASS"}
        result = evidence_contract.assess_audited_independence(incomplete)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("missing required fields" in reason for reason in result["reasons"]))

    def test_assess_audited_independence_forged_decision_is_unmet(self):
        forged = valid_independence_audit()
        forged["decision"] = "FAIL"
        result = evidence_contract.assess_audited_independence(forged)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("PASS" in reason for reason in result["reasons"]))

    def test_assess_alone_never_returns_audited_even_with_valid_audit_nearby(self):
        # Regression: assess() must not silently promote via any side channel.
        result = evidence_contract.assess([record(1), record(2)])
        self.assertEqual(result["independence"], "CONTRACTED")
        self.assertNotEqual(result["independence"], "AUDITED")
        # Only the dedicated assessor may return AUDITED.
        evidence = [record(1), record(2)]
        audit = evidence_contract.assess_audited_independence(
            valid_independence_audit(evidence), evidence=evidence
        )
        self.assertEqual(audit["independence"], "AUDITED")

    def test_assess_audited_matching_digests_is_audited(self):
        evidence = [record(1), record(2)]
        audit = valid_independence_audit(evidence)
        result = evidence_contract.assess_audited_independence(audit, evidence=evidence)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["independence"], "AUDITED")
        self.assertTrue(any("match" in reason for reason in result["reasons"]))

    def test_assess_audited_mismatched_digests_is_unmet(self):
        evidence = [record(1), record(2)]
        # Checklist-valid PASS audit whose digests belong to a different set.
        audit = valid_independence_audit()  # placeholder digests, not content-addressed
        result = evidence_contract.assess_audited_independence(audit, evidence=evidence)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("do not match" in reason for reason in result["reasons"]))

    def test_assess_audited_pass_for_other_bundle_cannot_satisfy(self):
        evidence_a = [record(1), record(2)]
        evidence_b = [record(3), record(4)]
        audit_for_b = valid_independence_audit(evidence_b)
        # Valid PASS for B must not AUDITED when evidence is A.
        result = evidence_contract.assess_audited_independence(audit_for_b, evidence=evidence_a)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("different set" in reason or "do not match" in reason for reason in result["reasons"]))

    def test_assess_audited_bare_string_digests_are_unmet(self):
        # Typed objects required always; bare strings fail even without evidence binding.
        audit = valid_independence_audit()
        audit["evidence_digests"] = ["sha256:aaa", "sha256:bbb"]
        result = evidence_contract.assess_audited_independence(audit)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(
            any("bare digest strings" in reason or "{evidence_id, digest}" in reason for reason in result["reasons"])
        )

    def test_assess_audited_bare_string_digests_with_evidence_are_unmet(self):
        evidence = [record(1), record(2)]
        expected = audit_log.evidence_digest_entries(evidence)
        # Even if string values equal content digests, shape must be objects.
        audit = valid_independence_audit(evidence)
        audit["evidence_digests"] = [entry["digest"] for entry in expected]
        result = evidence_contract.assess_audited_independence(audit, evidence=evidence)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(
            any("bare digest strings" in reason or "{evidence_id, digest}" in reason for reason in result["reasons"])
        )

    def test_assess_audited_mismatched_evidence_id_is_unmet(self):
        evidence = [record(1), record(2)]
        audit = valid_independence_audit(evidence)
        # Same digests, wrong evidence_id on first entry.
        audit["evidence_digests"] = [
            {"evidence_id": "e-wrong", "digest": audit["evidence_digests"][0]["digest"]},
            dict(audit["evidence_digests"][1]),
        ]
        result = evidence_contract.assess_audited_independence(audit, evidence=evidence)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(
            any("do not match" in reason or "evidence_id" in reason for reason in result["reasons"])
        )

    def test_assess_audited_mismatched_digest_value_is_unmet(self):
        evidence = [record(1), record(2)]
        audit = valid_independence_audit(evidence)
        # Correct evidence_id, wrong digest on first entry.
        audit["evidence_digests"] = [
            {"evidence_id": audit["evidence_digests"][0]["evidence_id"], "digest": "sha256:deadbeef"},
            dict(audit["evidence_digests"][1]),
        ]
        result = evidence_contract.assess_audited_independence(audit, evidence=evidence)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")
        self.assertTrue(any("do not match" in reason for reason in result["reasons"]))

    def test_assess_audited_extra_keys_on_digest_entry_are_unmet(self):
        audit = valid_independence_audit()
        audit["evidence_digests"] = [
            {"evidence_id": "e-1", "digest": "sha256:aaa", "extra": "nope"},
            {"evidence_id": "e-2", "digest": "sha256:bbb"},
        ]
        result = evidence_contract.assess_audited_independence(audit)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["independence"], "UNMET")

    def test_assess_never_audited_even_when_digests_would_match(self):
        evidence = [record(1), record(2)]
        _ = valid_independence_audit(evidence)
        result = evidence_contract.assess(evidence)
        self.assertEqual(result["independence"], "CONTRACTED")
        self.assertNotEqual(result["independence"], "AUDITED")
