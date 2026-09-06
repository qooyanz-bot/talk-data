import contextlib
import json
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import conformance  # noqa: E402
import limitations  # noqa: E402


REQUIRED_TOP_KEYS = {"schema_version", "status", "checks"}


class ConformanceTests(unittest.TestCase):
    def test_report_shape_stable(self):
        report = conformance.run_conformance()
        self.assertEqual(set(report), REQUIRED_TOP_KEYS)
        self.assertEqual(report["schema_version"], conformance.SCHEMA_VERSION)
        self.assertIn(report["status"], {"CONFORMANT", "FAIL"})
        self.assertIsInstance(report["checks"], list)
        ids = [c["id"] for c in report["checks"]]
        self.assertEqual(set(ids), conformance.CHECK_IDS_ALLOWED)
        for check in report["checks"]:
            with self.subTest(check_id=check["id"]):
                self.assertEqual(set(check), {"id", "status", "detail"})
                self.assertIn(check["status"], conformance.CHECK_STATUSES_ALLOWED)

    def test_check_ids_and_statuses_exported_as_frozensets(self):
        self.assertIsInstance(conformance.CHECK_IDS_ALLOWED, frozenset)
        self.assertIsInstance(conformance.CHECK_STATUSES_ALLOWED, frozenset)
        self.assertIn("limitations_document", conformance.CHECK_IDS_ALLOWED)
        self.assertIn("r6g_experiment_result_claim", conformance.CHECK_IDS_ALLOWED)
        self.assertIn("PASS", conformance.CHECK_STATUSES_ALLOWED)
        self.assertIn("LIMITATIONS", conformance.CHECK_STATUSES_ALLOWED)

    def test_fixture_matches_module_output(self):
        fixture = json.loads((ROOT / "fixtures" / "conformance_report.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture, conformance.run_conformance())

    def test_limitations_section_never_pass(self):
        report = conformance.run_conformance()
        lim = next(c for c in report["checks"] if c["id"] == "limitations_document")
        self.assertEqual(lim["status"], "LIMITATIONS")
        self.assertNotEqual(lim["status"], "PASS")
        self.assertEqual(lim["detail"]["status"], "LIMITATIONS")
        self.assertEqual(lim["detail"]["document"], limitations.limitations())

    def test_synthetic_validate_valid(self):
        report = conformance.run_conformance()
        check = next(c for c in report["checks"] if c["id"] == "synthetic_address_validate")
        self.assertEqual(check["status"], "PASS")
        self.assertEqual(check["detail"]["validate_status"], "VALID")
        self.assertEqual(check["detail"]["errors"], [])

    def test_synthetic_ready_value_null(self):
        report = conformance.run_conformance()
        check = next(c for c in report["checks"] if c["id"] == "synthetic_evaluate_ready")
        self.assertEqual(check["status"], "PASS")
        self.assertEqual(check["detail"]["decision"], "READY_FOR_VERIFICATION")
        self.assertIsNone(check["detail"]["value"])

    def test_synthetic_abstain_value_null(self):
        report = conformance.run_conformance()
        check = next(c for c in report["checks"] if c["id"] == "synthetic_evaluate_abstain")
        self.assertEqual(check["status"], "PASS")
        self.assertEqual(check["detail"]["decision"], "ABSTAIN")
        self.assertIsNone(check["detail"]["value"])
        self.assertIn(check["detail"]["path"], {"shared_law", "contradiction"})

    def test_r6g_manifest_valid_and_experiment_not_executed(self):
        report = conformance.run_conformance()
        manifest = next(c for c in report["checks"] if c["id"] == "r6g_protocol_manifest")
        self.assertEqual(manifest["status"], "PASS")
        self.assertEqual(manifest["detail"]["manifest_status"], "MANIFEST_VALID")
        claim = next(c for c in report["checks"] if c["id"] == "r6g_experiment_result_claim")
        self.assertIn(claim["status"], {"NOT_RUN", "BLOCKED"})
        self.assertNotEqual(claim["status"], "PASS")
        self.assertFalse(claim["detail"]["executed"])
        self.assertEqual(claim["detail"]["claim_status"], "BLOCKED")
        self.assertEqual(claim["detail"]["limitations_r6g_experiment"], "NOT_RUN")
        # Never claim R6-G executed / result-backed capability.
        self.assertNotIn(claim["status"], {"COMPLETED", "EXECUTED", "RUN", "ALLOWED_AS_RESULT"})

    def test_overall_conformant_embeds_limitations(self):
        report = conformance.run_conformance()
        self.assertEqual(report["status"], "CONFORMANT")
        lim = next(c for c in report["checks"] if c["id"] == "limitations_document")
        self.assertEqual(lim["status"], "LIMITATIONS")
        self.assertFalse(any(c["status"] == "FAIL" for c in report["checks"]))

    def test_cli_conformance_exit_zero(self):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--conformance"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "CONFORMANT")
        self.assertEqual(payload["schema_version"], conformance.SCHEMA_VERSION)

    def test_cli_conformance_rejects_other_modes(self):
        cases = [
            ["address.json", "evidence.json"],
            ["--now", "2026-09-06T00:00:00Z"],
            ["--limitations"],
            ["--runtime-manifest"],
            ["--check-contract-only", str(ROOT / "fixtures" / "golden_contract_ok_response.json")],
            ["--verify-decision-log", str(ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json")],
            ["--verify-audit-log", "audit.json"],
            ["--validate-protocol-manifest", str(ROOT / "fixtures" / "r6g_frozen_protocol_manifest.json")],
            ["--protocol-manifest", "manifest.json"],
            ["--claim-type", "DESIGN_DESCRIPTION"],
            ["--independence-audit", "audit.json"],
            ["--audit", "audit.json"],
        ]
        for extra in cases:
            with self.subTest(extra=extra):
                buf = StringIO()
                with contextlib.redirect_stdout(buf):
                    code = address_cli.main(["--conformance", *extra])
                self.assertEqual(code, 2)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload["status"], "INVALID_INPUT")
                self.assertTrue(payload["errors"])

    def test_limitations_rejects_conformance_combo(self):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--limitations", "--conformance"])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertTrue(any("conformance" in err for err in payload["errors"]))

    def test_cli_nonzero_when_check_fails(self):
        failing = {
            "schema_version": conformance.SCHEMA_VERSION,
            "status": "FAIL",
            "checks": [
                {"id": "limitations_document", "status": "LIMITATIONS", "detail": {}},
                {"id": "synthetic_address_validate", "status": "FAIL", "detail": {}},
            ],
        }
        buf = StringIO()
        with mock.patch.object(conformance, "run_conformance", return_value=failing):
            with contextlib.redirect_stdout(buf):
                code = address_cli.main(["--conformance"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(buf.getvalue())["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
