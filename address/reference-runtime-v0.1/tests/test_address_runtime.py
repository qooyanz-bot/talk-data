import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import address_runtime  # noqa: E402


class AddressRuntimeTests(unittest.TestCase):
    def setUp(self):
        fixture = ROOT / "fixtures" / "valid_synthetic_address.json"
        self.address = json.loads(fixture.read_text(encoding="utf-8"))
        self.address["address_id"] = address_runtime.canonical_id(self.address)

    def test_valid_synthetic_address(self):
        self.assertEqual(address_runtime.validate(self.address), [])

    def test_hash_tamper_is_rejected(self):
        self.address["goal"]["id"] = "goal:tampered"
        self.assertIn("address_id does not match canonical payload hash", address_runtime.validate(self.address))

    def test_real_secret_capability_is_rejected(self):
        self.address["world_id"] = "world:real:example"
        self.address["capability_scope"] = ["read:declared-public-data", "read:secret-vault"]
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        errors = address_runtime.validate(self.address)
        self.assertTrue(any("prohibited" in error for error in errors))
        self.assertTrue(any("real-world" in error for error in errors))

    def test_unknown_without_abstain_is_rejected(self):
        self.address["unknown"][0]["abstain_if_unresolved"] = False
        self.address["address_id"] = address_runtime.canonical_id(self.address)
        errors = address_runtime.validate(self.address)
        self.assertTrue(any("abstention when unresolved" in error for error in errors))

    def test_filled_target_value_is_rejected_without_raising(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["value"] = "discovered"
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(errors)
        self.assertTrue(any("target_value.value must be null" in error for error in errors))

    def test_missing_or_empty_target_value_type_is_rejected(self):
        for bad_type in ("", None, 12):
            with self.subTest(bad_type=bad_type):
                address = copy.deepcopy(self.address)
                if bad_type is None and "type" in address["target_value"]:
                    del address["target_value"]["type"]
                else:
                    address["target_value"]["type"] = bad_type
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)
                self.assertTrue(any("target_value.type" in error for error in errors))

    def test_non_null_lineage_result_sha_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["lineage"]["result_sha"] = "sha256:" + "b" * 64
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(errors)
        self.assertTrue(any("lineage.result_sha must be null" in error for error in errors))

    def test_valid_fixture_keeps_value_null_and_residual_unfilled(self):
        errors = address_runtime.validate(self.address)
        self.assertEqual(errors, [])
        self.assertIsNone(self.address["target_value"]["value"])
        residual = self.address["target_value"]["residual"]
        self.assertTrue(residual is None or residual == [])
        self.assertIsNone(self.address["lineage"]["result_sha"])

    def test_non_list_target_value_residual_is_rejected(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = "not-a-list"
        address["address_id"] = address_runtime.canonical_id(address)
        errors = address_runtime.validate(address)
        self.assertTrue(any("target_value.residual" in error for error in errors))

    def test_nonempty_residual_with_null_value_is_accepted(self):
        address = copy.deepcopy(self.address)
        address["target_value"]["residual"] = ["continuity"]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])



    def test_semantic_independence_closed_enum_accepts_allowed_values(self):
        for value in ("UNVERIFIED", "CONTRACTED", "AUDITED"):
            with self.subTest(value=value):
                address = copy.deepcopy(self.address)
                address["evidence_requirements"]["semantic_independence"] = value
                address["address_id"] = address_runtime.canonical_id(address)
                self.assertEqual(address_runtime.validate(address), [])

    def test_semantic_independence_rejects_invalid_enum_without_raising(self):
        for bad in ("INDEPENDENT", "independent", "audited", "", None, 1, True, ["AUDITED"]):
            with self.subTest(bad=bad):
                address = copy.deepcopy(self.address)
                if bad is None and "semantic_independence" in address["evidence_requirements"]:
                    del address["evidence_requirements"]["semantic_independence"]
                else:
                    address["evidence_requirements"]["semantic_independence"] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)
                self.assertTrue(
                    any(
                        "evidence_requirements.semantic_independence must be one of"
                        in error
                        for error in errors
                    )
                )

    def test_unverified_fixture_remains_valid(self):
        self.assertEqual(
            self.address["evidence_requirements"]["semantic_independence"],
            "UNVERIFIED",
        )
        self.assertEqual(address_runtime.validate(self.address), [])



    def test_entity_requires_nonempty_id_and_type(self):
        for field, bad in (("id", ""), ("id", None), ("type", ""), ("type", 3)):
            with self.subTest(field=field, bad=bad):
                address = copy.deepcopy(self.address)
                if bad is None:
                    del address["entities"][0][field]
                else:
                    address["entities"][0][field] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)
                self.assertTrue(any(f"entities[0].{field}" in error for error in errors))

    def test_entity_optional_binding_must_be_nonempty_string_when_present(self):
        for bad in ("", None, 1):
            with self.subTest(bad=bad):
                address = copy.deepcopy(self.address)
                address["entities"][0]["binding"] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(any("entities[0].binding" in error for error in errors))
        address = copy.deepcopy(self.address)
        address["entities"][0]["binding"] = "typed-reference"
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])

    def test_relation_requires_nonempty_predicate_subject_object(self):
        for field in ("predicate", "subject", "object"):
            for bad in ("", None, 0):
                with self.subTest(field=field, bad=bad):
                    address = copy.deepcopy(self.address)
                    if bad is None:
                        del address["relations"][0][field]
                    else:
                        address["relations"][0][field] = bad
                    address["address_id"] = address_runtime.canonical_id(address)
                    errors = address_runtime.validate(address)
                    self.assertTrue(any(f"relations[0].{field}" in error for error in errors))

    def test_unknown_requires_nonempty_slot_and_closed_status(self):
        address = copy.deepcopy(self.address)
        address["unknown"][0]["slot"] = ""
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(any("unknown[0].slot" in error for error in address_runtime.validate(address)))
        for bad in ("DERIVED", "resolved", "", None, 1):
            with self.subTest(bad=bad):
                address = copy.deepcopy(self.address)
                if bad is None:
                    del address["unknown"][0]["status"]
                else:
                    address["unknown"][0]["status"] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("unknown[0].status must be one of" in error for error in errors)
                )
        for value in ("NOT_DERIVABLE", "UNRESOLVED", "RESIDUAL", "OPEN"):
            with self.subTest(value=value):
                address = copy.deepcopy(self.address)
                address["unknown"][0]["status"] = value
                address["address_id"] = address_runtime.canonical_id(address)
                self.assertEqual(address_runtime.validate(address), [])

    def test_lineage_protocol_schema_runtime_sha_null_or_nonempty(self):
        for key in ("protocol_sha", "schema_sha", "runtime_sha"):
            with self.subTest(key=key, value=None):
                address = copy.deepcopy(self.address)
                address["lineage"][key] = None
                address["address_id"] = address_runtime.canonical_id(address)
                self.assertEqual(address_runtime.validate(address), [])
            with self.subTest(key=key, value="ok"):
                address = copy.deepcopy(self.address)
                address["lineage"][key] = "ok"
                address["address_id"] = address_runtime.canonical_id(address)
                self.assertEqual(address_runtime.validate(address), [])
            for bad in ("", 12, True, []):
                with self.subTest(key=key, bad=bad):
                    address = copy.deepcopy(self.address)
                    address["lineage"][key] = bad
                    address["address_id"] = address_runtime.canonical_id(address)
                    errors = address_runtime.validate(address)
                    self.assertTrue(any(f"lineage.{key}" in error for error in errors))

    def test_minimum_sources_must_be_int_ge_one_when_present(self):
        for bad in (0, -1, 1.5, True, False, "2", None):
            with self.subTest(bad=bad):
                address = copy.deepcopy(self.address)
                address["evidence_requirements"]["minimum_sources"] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("evidence_requirements.minimum_sources" in error for error in errors)
                )
        address = copy.deepcopy(self.address)
        del address["evidence_requirements"]["minimum_sources"]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])
        address = copy.deepcopy(self.address)
        address["evidence_requirements"]["minimum_sources"] = 2
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])

    def test_canonical_id_stable_under_key_order_and_whitespace(self):
        """canonical_id uses sort_keys + compact separators; source layout must not matter."""
        compact = json.dumps(self.address, ensure_ascii=False, separators=(",", ":"))
        pretty = json.dumps(self.address, ensure_ascii=False, indent=2, sort_keys=False)
        reordered = json.loads(pretty)
        # Force a different insertion order than the fixture's natural order.
        reordered = {k: reordered[k] for k in reversed(list(reordered.keys()))}
        id_compact = address_runtime.canonical_id(json.loads(compact))
        id_pretty = address_runtime.canonical_id(json.loads(pretty))
        id_reordered = address_runtime.canonical_id(reordered)
        self.assertEqual(id_compact, id_pretty)
        self.assertEqual(id_compact, id_reordered)
        self.assertEqual(id_compact, self.address["address_id"])
        self.assertEqual(
            address_runtime.canonical_dumps({"b": 1, "a": 2}),
            '{"a":2,"b":1}',
        )
        self.assertEqual(address_runtime.validate(self.address), [])


    def test_goal_id_must_be_nonempty_string(self):
        for bad in ("", None, 1, True, []):
            with self.subTest(bad=bad):
                address = copy.deepcopy(self.address)
                if bad is None:
                    del address["goal"]["id"]
                else:
                    address["goal"]["id"] = bad
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(errors)
                self.assertTrue(any("goal.id" in error for error in errors))

    def test_goal_success_criteria_must_be_list_of_nonempty_strings(self):
        for bad in ("", None, 1, True):
            with self.subTest(item=bad):
                address = copy.deepcopy(self.address)
                address["goal"]["success_criteria"] = [bad]
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("goal.success_criteria" in error for error in errors)
                )
        for bad_list in ("not-a-list", None, 3, {"a": 1}):
            with self.subTest(list=bad_list):
                address = copy.deepcopy(self.address)
                address["goal"]["success_criteria"] = bad_list
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("goal.success_criteria" in error for error in errors)
                )
        # empty list is allowed (no empty-string items); mixed empty rejected
        address = copy.deepcopy(self.address)
        address["goal"]["success_criteria"] = []
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])
        address = copy.deepcopy(self.address)
        address["goal"]["success_criteria"] = ["ok", ""]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(
            any("goal.success_criteria" in error for error in address_runtime.validate(address))
        )

    def test_state_constraints_must_be_list_of_nonempty_strings(self):
        for bad in ("", None, 1, True):
            with self.subTest(item=bad):
                address = copy.deepcopy(self.address)
                address["state_constraints"] = [bad]
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("state_constraints must be a list of non-empty strings" in error for error in errors)
                )
        for bad_list in ("x", None, 2):
            with self.subTest(list=bad_list):
                address = copy.deepcopy(self.address)
                address["state_constraints"] = bad_list
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("state_constraints must be a list of non-empty strings" in error for error in errors)
                )
        address = copy.deepcopy(self.address)
        address["state_constraints"] = []
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])
        address = copy.deepcopy(self.address)
        address["state_constraints"] = ["schema-valid", ""]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(
            any("state_constraints" in error for error in address_runtime.validate(address))
        )

    def test_capability_scope_items_must_be_nonempty_strings(self):
        for bad in ("", None, 1, True):
            with self.subTest(item=bad):
                address = copy.deepcopy(self.address)
                address["capability_scope"] = [bad]
                address["address_id"] = address_runtime.canonical_id(address)
                errors = address_runtime.validate(address)
                self.assertTrue(
                    any("capability_scope must be a list of non-empty strings" in error for error in errors)
                )
        address = copy.deepcopy(self.address)
        address["capability_scope"] = ["read:declared-public-data", ""]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertTrue(
            any("capability_scope must be a list of non-empty strings" in error for error in address_runtime.validate(address))
        )
        # existing forbid-token + real-world subset path still works with non-empty items
        address = copy.deepcopy(self.address)
        address["capability_scope"] = ["read:declared-public-data", "verify:declared-schema"]
        address["address_id"] = address_runtime.canonical_id(address)
        self.assertEqual(address_runtime.validate(address), [])




if __name__ == "__main__":
    unittest.main()
