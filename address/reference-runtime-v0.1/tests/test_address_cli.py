import contextlib
import json
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}", "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z", "assertion_key": "target", "assertion_value": "verified",
    }


class AddressCliTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        self.bundle = [evidence(1), evidence(2)]

    def test_evaluate_generates_value_free_audit(self):
        result = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(result["resolution"]["value"])
        self.assertTrue(result["generated_audit"]["audit_id"].startswith("audit:"))

    def test_evaluate_replays_supplied_audit(self):
        first = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        second = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z", first["generated_audit"])
        self.assertEqual(second["replay"]["status"], "REPLAY_VERIFIED")

    def test_cli_loads_json_files(self):
        with tempfile.TemporaryDirectory() as directory:
            address_path = Path(directory) / "address.json"
            evidence_path = Path(directory) / "evidence.json"
            address_path.write_text(json.dumps(self.address), encoding="utf-8")
            evidence_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            result = address_cli.evaluate(json.loads(address_path.read_text()), json.loads(evidence_path.read_text()), "2026-09-06T00:00:00Z")
            self.assertEqual(result["resolution"]["decision"], "READY_FOR_VERIFICATION")

    def test_evaluate_non_list_evidence_does_not_crash(self):
        result = address_cli.evaluate(self.address, {"not": "a list"}, "2026-09-06T00:00:00Z")
        self.assertEqual(result["resolution"]["decision"], "ABSTAIN")
        self.assertIsNone(result["resolution"]["value"])
        self.assertIsInstance(result["generated_audit"], dict)
        self.assertEqual(result["generated_audit"]["evidence_digests"], [])

    def test_protocol_claim_design_allowed_for_frozen_manifest(self):
        manifest = json.loads((ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json").read_text(encoding="utf-8"))
        result = address_cli.evaluate(
            self.address, self.bundle, "2026-09-06T00:00:00Z",
            protocol_manifest=manifest, claim_type="DESIGN_DESCRIPTION",
        )
        self.assertEqual(result["protocol_claim"]["status"], "ALLOWED_AS_DESIGN")
        self.assertIsNone(result["resolution"]["value"])

    def test_protocol_claim_blocks_experiment_and_capability_for_frozen_manifest(self):
        manifest = json.loads((ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json").read_text(encoding="utf-8"))
        for claim_type in ("EXPERIMENT_RESULT", "CAPABILITY_CLAIM"):
            with self.subTest(claim_type=claim_type):
                result = address_cli.evaluate(
                    self.address, self.bundle, "2026-09-06T00:00:00Z",
                    protocol_manifest=manifest, claim_type=claim_type,
                )
                self.assertEqual(result["protocol_claim"]["status"], "BLOCKED")
                self.assertNotEqual(result["protocol_claim"].get("status"), "ALLOWED_AS_RESULT")
                self.assertIsNone(result["resolution"]["value"])

    def test_check_contract_only_accepts_valid_response(self):
        response = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps(response), encoding="utf-8")
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(buf.getvalue())["status"], "CONTRACT_OK")

    def test_check_contract_only_rejects_non_null_value(self):
        response = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        response["resolution"]["value"] = "invented"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_value.json"
            path.write_text(json.dumps(response), encoding="utf-8")
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertTrue(any("null" in err for err in payload["errors"]))

    def test_check_contract_only_rejects_nested_result_sha(self):
        response = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        response["lineage"] = {"result_sha": "sha256:" + "a" * 64}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad_sha.json"
            path.write_text(json.dumps(response), encoding="utf-8")
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "CONTRACT_INVALID")
            self.assertTrue(any("result_sha" in err for err in payload["errors"]))

    def test_check_contract_only_does_not_require_address_evidence(self):
        response = address_cli.evaluate(self.address, self.bundle, "2026-09-06T00:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps(response), encoding="utf-8")
            # Must succeed without address/evidence/--now positionals.
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                code = address_cli.main(["--check-contract-only", str(path)])
            self.assertEqual(code, 0)

    def test_check_contract_only_rejects_address_evidence_combo(self):
        fixture = ROOT / "fixtures" / "golden_contract_ok_response.json"
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main([
                "--check-contract-only", str(fixture),
                "address.json", "evidence.json",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        joined = " ".join(payload["errors"])
        self.assertIn("address", joined)
        self.assertIn("evidence", joined)

    def test_check_contract_only_rejects_now_and_resolve_flags(self):
        fixture = ROOT / "fixtures" / "golden_contract_ok_response.json"
        cases = [
            ["--now", "2026-09-06T00:00:00Z"],
            ["--audit", "audit.json"],
            ["--protocol-manifest", "manifest.json"],
            ["--claim-type", "DESIGN_DESCRIPTION"],
        ]
        for extra in cases:
            with self.subTest(extra=extra):
                buf = StringIO()
                with contextlib.redirect_stdout(buf):
                    code = address_cli.main(["--check-contract-only", str(fixture), *extra])
                self.assertEqual(code, 2)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload["status"], "INVALID_INPUT")
                self.assertTrue(payload["errors"])

    def test_evaluate_audited_with_valid_independence_audit_ready(self):
        import copy
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
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
        result = address_cli.evaluate(
            address, self.bundle, "2026-09-06T00:00:00Z", independence_audit=audit
        )
        self.assertEqual(result["resolution"]["decision"], "READY_FOR_VERIFICATION")
        self.assertEqual(result["resolution"]["reason"], "AUDITED_INDEPENDENCE")
        self.assertIsNone(result["resolution"]["value"])

    def test_evaluate_audited_without_independence_audit_abstains(self):
        import copy
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
        result = address_cli.evaluate(address, self.bundle, "2026-09-06T00:00:00Z")
        self.assertEqual(result["resolution"]["decision"], "ABSTAIN")
        self.assertEqual(result["resolution"]["reason"], "SEMANTIC_INDEPENDENCE_UNMET")
        self.assertIsNone(result["resolution"]["value"])

    def test_cli_independence_audit_flag_loads_json(self):
        import copy
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["semantic_independence"] = "AUDITED"
        address["address_id"] = address_runtime.canonical_id(address)
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
        with tempfile.TemporaryDirectory() as directory:
            address_path = Path(directory) / "address.json"
            evidence_path = Path(directory) / "evidence.json"
            audit_path = Path(directory) / "independence_audit.json"
            address_path.write_text(json.dumps(address), encoding="utf-8")
            evidence_path.write_text(json.dumps(self.bundle), encoding="utf-8")
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            buf = StringIO()
            with contextlib.redirect_stdout(buf):
                code = address_cli.main([
                    str(address_path), str(evidence_path),
                    "--now", "2026-09-06T00:00:00Z",
                    "--independence-audit", str(audit_path),
                ])
            self.assertEqual(code, 0)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["resolution"]["decision"], "READY_FOR_VERIFICATION")
            self.assertEqual(payload["resolution"]["reason"], "AUDITED_INDEPENDENCE")
            self.assertIsNone(payload["resolution"]["value"])

    def test_check_contract_only_rejects_independence_audit_combo(self):
        fixture = ROOT / "fixtures" / "golden_contract_ok_response.json"
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main([
                "--check-contract-only", str(fixture),
                "--independence-audit", "audit.json",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertTrue(any("independence-audit" in err for err in payload["errors"]))



if __name__ == "__main__":
    unittest.main()
