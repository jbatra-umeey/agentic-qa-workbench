from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from app import ROOT, approve, build_plan, digest, execute, save, validate_plan
from model import ModelError


class QATests(unittest.TestCase):
    def setUp(self):
        self.requirements = json.loads((ROOT / "data/requirements.json").read_text())
        self.state = build_plan(self.requirements)

    def test_unreviewed_plan_cannot_execute(self):
        with self.assertRaises(ValueError):
            execute(self.state)

    def test_wrong_digest_cannot_approve(self):
        with self.assertRaises(ValueError):
            approve(self.state, "bad-digest")

    def test_injected_bug_detected_at_exact_boundary(self):
        approved = approve(self.state, self.state["plan_digest"])
        result = execute(approved, inject_bug=True)
        failures = [r for r in result["results"] if not r["passed"]]
        self.assertEqual([r["id"] for r in failures], ["TITLE-01-4"])
        self.assertEqual(execute(approved)["summary"]["failed"], 0)

    def test_change_after_review_is_rejected(self):
        approved = approve(self.state, self.state["plan_digest"])
        approved["plan"]["tests"][0]["input"]["title"] = "changed"
        with self.assertRaises(ValueError):
            execute(approved)

    def test_disallowed_tool_is_rejected(self):
        plan = deepcopy(self.state["plan"])
        plan["tests"][0]["tool"] = "shell"
        with self.assertRaises(ModelError):
            validate_plan(plan, self.requirements)

    def test_requirement_coverage_is_required(self):
        plan = {"tests": [self.state["plan"]["tests"][0]]}
        with self.assertRaises(ModelError):
            validate_plan(plan, self.requirements)

    def test_model_retries_are_bounded(self):
        class BadModel:
            calls = 0
            def json(self, *args, **kwargs):
                self.calls += 1
                return {"tests": []}
        model = BadModel()
        with self.assertRaises(ModelError):
            build_plan(self.requirements, model)
        self.assertEqual(model.calls, 2)

    def test_checkpoint_round_trip_preserves_approval(self):
        state = approve(self.state, self.state["plan_digest"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            save(state, path)
            loaded = json.loads(path.read_text())
            self.assertEqual(execute(loaded)["summary"]["failed"], 0)

    def test_requirement_changes_invalidate_checkpoint(self):
        self.state["requirements"][0]["description"] = "Altered requirement"
        with self.assertRaises(ValueError):
            approve(self.state, self.state["plan_digest"])


if __name__ == "__main__":
    unittest.main()
