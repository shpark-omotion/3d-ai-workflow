import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from doctor import inspect


class DoctorTest(unittest.TestCase):
    def test_missing_path_is_not_runtime_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            report = inspect(Path(folder), which=lambda _: None)
        self.assertEqual(set(report["path_checks"].values()), {"NOT_FOUND_ON_PATH"})
        self.assertEqual(set(report["runtime_checks"].values()), {"NOT_RUN"})
        self.assertEqual(set(report["kit_files"].values()), {"MISSING"})

    def test_found_path_never_claims_connection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").touch()
            report = inspect(root, which=lambda _: "/test/private/path")
        self.assertEqual(set(report["path_checks"].values()), {"FOUND_ON_PATH"})
        self.assertEqual(report["kit_files"]["README.md"], "PRESENT")
        self.assertEqual(report["runtime_checks"]["blender_mcp_scene_read"], "NOT_RUN")
        self.assertNotIn("/test/private/path", str(report))

    def test_missing_required_guide_is_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").touch()
            report = inspect(root, which=lambda _: None)
        self.assertEqual(report["kit_files"]["docs/START-HERE.md"], "MISSING")
        self.assertEqual(report["kit_files"]["templates/run-state.md"], "MISSING")

    def test_skill_present_is_not_loaded(self):
        report = inspect(Path(__file__).resolve().parents[1], which=lambda _: None)
        self.assertTrue(all(v == "PRESENT" for v in report["kit_files"].values()))
        self.assertEqual(report["runtime_checks"]["skill_loaded"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
