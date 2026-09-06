import contextlib
import json
import sys
import unittest
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_cli  # noqa: E402
import address_runtime  # noqa: E402
import limitations  # noqa: E402


REQUIRED_KEYS = {
    "schema_version",
    "status",
    "world_scope",
    "value_discovery",
    "r6g_experiment",
    "r6g_reference",
    "real_domain_extrapolation",
    "secret_access",
    "crypto_bypass",
    "future_direct",
    "audited_independence",
    "protocol_result_claims",
}

FORBIDDEN_STATUSES = {
    "value_discovery": {"NOT_IMPLEMENTED", "FORBIDDEN"},
    "r6g_experiment": {"NOT_RUN"},
    "real_domain_extrapolation": {"FORBIDDEN"},
    "secret_access": {"FORBIDDEN"},
    "crypto_bypass": {"FORBIDDEN"},
    "future_direct": {"FORBIDDEN"},
}


def evidence(index: int) -> dict:
    return {
        "evidence_id": f"e-{index}", "claim_hash": f"claim-{index}", "path_id": f"path-{index}",
        "authority_id": f"authority-{index}", "generator_id": f"generator-{index}", "semantic_law_id": f"law-{index}",
        "observed_at": "2026-09-05T00:00:00Z", "assertion_key": "target", "assertion_value": "verified",
    }


class LimitationsTests(unittest.TestCase):
    def test_shape_stable(self):
        doc = limitations.limitations()
        self.assertIsInstance(doc, dict)
        self.assertEqual(set(doc), REQUIRED_KEYS)
        self.assertEqual(doc["schema_version"], limitations.SCHEMA_VERSION)
        self.assertEqual(doc["status"], "LIMITATIONS")
        self.assertEqual(doc["world_scope"], "SYNTHETIC_ONLY")
        self.assertEqual(doc["r6g_reference"], "SPEC_ONLY")

    def test_forbidden_capabilities_remain_forbidden(self):
        doc = limitations.limitations()
        for key in limitations.forbidden_capability_keys():
            with self.subTest(key=key):
                status = doc[key]
                self.assertIn(status, FORBIDDEN_STATUSES[key])
                self.assertFalse(limitations.is_claiming_status(status))

    def test_fixture_matches_module_output(self):
        fixture = json.loads((ROOT / "fixtures" / "limitations.json").read_text(encoding="utf-8"))
        self.assertEqual(fixture, limitations.limitations())

    def test_cli_limitations_exit_zero(self):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--limitations"])
        self.assertEqual(code, 0)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload, limitations.limitations())

    def test_cli_limitations_rejects_resolve_and_contract_flags(self):
        cases = [
            ["address.json", "evidence.json"],
            ["--now", "2026-09-06T00:00:00Z"],
            ["--audit", "audit.json"],
            ["--protocol-manifest", "manifest.json"],
            ["--claim-type", "DESIGN_DESCRIPTION"],
            ["--check-contract-only", str(ROOT / "fixtures" / "golden_contract_ok_response.json")],
            ["--verify-decision-log", str(ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json")],
        ]
        for extra in cases:
            with self.subTest(extra=extra):
                buf = StringIO()
                with contextlib.redirect_stdout(buf):
                    code = address_cli.main(["--limitations", *extra])
                self.assertEqual(code, 2)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload["status"], "INVALID_INPUT")
                self.assertTrue(payload["errors"])

    def test_check_contract_only_rejects_limitations_combo(self):
        fixture = ROOT / "fixtures" / "golden_contract_ok_response.json"
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--check-contract-only", str(fixture), "--limitations"])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertTrue(any("limitations" in err for err in payload["errors"]))

    def test_evaluate_never_contradicts_value_discovery_limitation(self):
        # limitations.value_discovery is NOT_IMPLEMENTED; public responses must keep value=null.
        self.assertEqual(limitations.limitations()["value_discovery"], "NOT_IMPLEMENTED")
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        address = json.loads(fixture.read_text(encoding="utf-8"))
        address["address_id"] = address_runtime.canonical_id(address)
        result = address_cli.evaluate(address, [evidence(1), evidence(2)], "2026-09-06T00:00:00Z")
        self.assertIsNone(result["resolution"]["value"])

    def test_limitations_do_not_claim_r6g_ran(self):
        doc = limitations.limitations()
        self.assertEqual(doc["r6g_experiment"], "NOT_RUN")
        self.assertEqual(doc["r6g_reference"], "SPEC_ONLY")
        self.assertNotEqual(doc["r6g_experiment"], "COMPLETED")
        self.assertFalse(limitations.is_claiming_status(doc["r6g_experiment"]))

    def test_audited_independence_requires_external_record(self):
        doc = limitations.limitations()
        self.assertEqual(doc["audited_independence"], "EXTERNAL_RECORD_REQUIRED")
        self.assertFalse(limitations.is_claiming_status(doc["audited_independence"]))

    def test_cli_limitations_rejects_independence_audit_flag(self):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--limitations", "--independence-audit", "audit.json"])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertTrue(any("independence-audit" in err for err in payload["errors"]))


    def test_validate_enforces_synthetic_only_world_scope(self):
        """LIMITATIONS world_scope=SYNTHETIC_ONLY is enforced by address_runtime.validate."""
        self.assertEqual(limitations.limitations()["world_scope"], "SYNTHETIC_ONLY")
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        address = json.loads(fixture.read_text(encoding="utf-8"))
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])
        address["world_id"] = "world:real:example"
        address["capability_scope"] = sorted(address_runtime.REAL_CAPABILITIES)
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(any("SYNTHETIC_ONLY" in error for error in errors))

    def test_protocol_result_claims_remain_gated(self):
        doc = limitations.limitations()
        self.assertEqual(doc["protocol_result_claims"], "GATED")
        self.assertFalse(limitations.is_claiming_status(doc["protocol_result_claims"]))


    def test_limitations_rejects_verify_decision_log_combo(self):
        fixture = ROOT / "fixtures" / "r6g_frozen_decision_log_blocked.json"
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            code = address_cli.main(["--limitations", "--verify-decision-log", str(fixture)])
        self.assertEqual(code, 2)
        payload = json.loads(buf.getvalue())
        self.assertEqual(payload["status"], "INVALID_INPUT")
        self.assertTrue(any("verify-decision-log" in err for err in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
