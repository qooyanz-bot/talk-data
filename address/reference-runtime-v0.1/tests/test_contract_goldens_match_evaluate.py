"""Assert frozen contract goldens match fresh evaluate() output (no hand-edit drift)."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import regenerate_contract_goldens as regen  # noqa: E402


class ContractGoldensMatchEvaluateTests(unittest.TestCase):
    def test_ready_abstain_contradiction_goldens_match_fresh_evaluate(self):
        built = regen.build_goldens()
        for filename, fresh in built.items():
            path = ROOT / "fixtures" / filename
            frozen = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(
                frozen,
                fresh,
                msg=f"{filename} drifted from evaluate(); re-run tools/regenerate_contract_goldens.py",
            )


if __name__ == "__main__":
    unittest.main()
